#!/usr/bin/env python3

import json
import shutil
import subprocess
import sys
from pathlib import Path

import stanza

import argostrain
import argostrain.opennmtutils
from argostrain import data, settings
from argostrain.dataset import *


def train(
    from_code,
    to_code,
    from_name,
    to_name,
    version,
    package_version,
    argos_version,
    data_exists,
):
    settings.RUN_PATH.mkdir(exist_ok=True)
    settings.CACHE_PATH.mkdir(exist_ok=True)

    # Check for existing checkpoints
    checkpoints = argostrain.opennmtutils.get_checkpoints()
    if len(checkpoints) > 0:
        input("Warning: Checkpoints exist (enter to continue)")

    if not data_exists:
        # Delete training data if it exists
        if settings.SOURCE_PATH.exists() or settings.TARGET_PATH.exists():
            print("Data already exists and will be deleted if you continue")
            input("Press enter to continue (Ctrl-C to cancel)")
            settings.SOURCE_PATH.unlink(missing_ok=True)
            settings.TARGET_PATH.unlink(missing_ok=True)

        available_datasets = get_available_datasets()

        from_and_to_codes = [from_code, to_code]
        available_datasets = list(
            filter(
                lambda x: x.from_code in from_and_to_codes
                and x.to_code in from_and_to_codes,
                available_datasets,
            )
        )

        datasets = list(
            filter(
                lambda x: x.from_code == from_code and x.to_code == to_code,
                available_datasets,
            )
        )

        # Try to use reverse data
        reverse_datasets = list(
            filter(
                lambda x: x.to_code == from_code and x.from_code == to_code,
                available_datasets,
            )
        )

        for reverse_dataset in reverse_datasets:
            reverse_dataset_data = reverse_dataset.data()
            dataset = Dataset(reverse_dataset_data[1], reverse_dataset_data[0])

            # Hack to preserve reference metadata
            dataset.reference = reverse_dataset.reference
            dataset.size = reverse_dataset.size

            datasets.append(dataset)

        if len(datasets) == 0:
            print(
                f"No data available for this language pair ({from_code}-{to_code}), check data-index.json"
            )
            sys.exit(1)
        assert len(datasets) > 0

        # Download and write data source and target
        while len(datasets) > 0:
            dataset = datasets.pop()
            print(str(dataset))
            source, target = dataset.data()

            with open(settings.SOURCE_PATH, "a") as s:
                s.writelines(source)

            with open(settings.TARGET_PATH, "a") as t:
                t.writelines(target)

            del dataset

        # Generate README.md
        # This is broken somehow, the template is written but the credits are not added
        # Maybe there's an issue with an end of file token in the template?
        readme = f"# {from_name}-{to_name}"
        with open(Path("MODEL_README.md")) as readme_template_file:
            readme_template = readme_template_file.readlines()
            print(readme_template)
            readme_template = readme_template[0:-1]
            readme += "".join(readme_template)
            for dataset in datasets:
                readme += dataset.reference + "\n\n"
        with open(settings.RUN_PATH / "README.md", "w") as readme_file:
            readme_file.write(readme)

    # Generate metadata.json
    metadata = {
        "package_version": package_version,
        "argos_version": argos_version,
        "from_code": from_code,
        "from_name": from_name,
        "to_code": to_code,
        "to_name": to_name,
    }
    metadata_json = json.dumps(metadata, indent=4)
    with open(settings.RUN_PATH / "metadata.json", "w") as metadata_file:
        metadata_file.write(metadata_json)

    argostrain.data.prepare_data(settings.SOURCE_PATH, settings.TARGET_PATH)

    with open(Path("run/split_data/all.txt"), "w") as combined:
        with open(Path("run/split_data/src-train.txt")) as src:
            for line in src:
                combined.write(line)
        with open(Path("run/split_data/tgt-train.txt")) as tgt:
            for line in tgt:
                combined.write(line)

    # TODO: Don't hardcode vocab_size and set user_defined_symbols
    subprocess.run(
        [
            "spm_train",
            "--input=run/split_data/all.txt",
            "--model_prefix=run/sentencepiece",
            "--vocab_size=50000",
            "--character_coverage=0.9995",
            "--input_sentence_size=1000000",
            "--shuffle_input_sentence=true",
        ]
    )

    subprocess.run(["rm", "run/split_data/all.txt"])

    # NOTE:
    # OpenNMT interprets the *fullwidth pipe* character `￨` (U+FF5C) as a token feature
    # separator. If your data contains it but your config does not expect features,
    # onmt_build_vocab will crash with:
    # "Found 1 features in the data but 0 were expected." in build_vocab.py
    #
    # The following code removes all `￨` from src-train.txt and tgt-train.txt
    # and then rebuilds the vocab.
    files = [
        "run/split_data/src-train.txt",
        "run/split_data/tgt-train.txt",
    ]
    for f in files:
        clean_file = f + ".clean"
        # Run `tr` to remove the fullwidth pipe and write to .clean file
        with open(f, "rb") as infile, open(clean_file, "wb") as outfile:
            subprocess.run(
                ["tr", "-d", "￨"],
                stdin=infile,
                stdout=outfile,
                check=True,
            )
        # Replace the original file with the cleaned one
        subprocess.run(["mv", clean_file, f], check=True)

    # onmt_build_vocab
    subprocess.run(["onmt_build_vocab", "-config", "config.yml", "-n_sample", "-1"])

    # Run Training
    subprocess.run(["onmt_train", "-config", "config.yml"])

    # Average checkpoints
    opennmt_checkpoints = argostrain.opennmtutils.get_checkpoints()
    opennmt_checkpoints.sort()
    subprocess.run(
        [
            "./../OpenNMT-py/tools/average_models.py",
            "-m",
            str(opennmt_checkpoints[-2].f),
            str(opennmt_checkpoints[-1].f),
            "-o",
            "run/averaged.pt",
        ]
    )

    subprocess.run(
        [
            "ct2-opennmt-py-converter",
            "--model_path",
            "run/averaged.pt",
            "--output_dir",
            "run/model",
            "--quantization",
            "int8",
        ]
    )

    package_version_code = package_version.replace(".", "_")
    model_dir = f"translate-{from_code}_{to_code}-{package_version_code}"
    model_path = Path("run") / model_dir

    subprocess.run(["mkdir", model_path])

    subprocess.run(["cp", "-r", "run/model", model_path])

    subprocess.run(["cp", "run/sentencepiece.model", model_path])

    # Include a Stanza sentence boundary detection model
    stanza_model_located = False
    stanza_lang_code = from_code
    while not stanza_model_located:
        try:
            stanza.download(stanza_lang_code, dir="run/stanza", processors="tokenize")
            stanza_model_located = True
        except:
            print(f"Could not locate stanza model for lang {stanza_lang_code}")
            print(
                "Enter the code of a different language to attempt to use its stanza model."
            )
            print(
                "This will work best for with a similar language to the one you are attempting to translate."
            )
            print(
                "This will require manually editing the Stanza package in the finished model to change its code"
            )
            stanza_lang_code = input("Stanza language code (ISO 639): ")

    subprocess.run(["cp", "-r", "run/stanza", model_path])

    subprocess.run(["cp", "run/metadata.json", model_path])
    subprocess.run(["cp", "run/README.md", model_path])

    package_path = (
        Path("run")
        / f"translate-{from_code}_{to_code}-{package_version_code}.argosmodel"
    )

    shutil.make_archive(model_dir, "zip", root_dir="run", base_dir=model_dir)
    subprocess.run(["mv", model_dir + ".zip", package_path])

    print(f"Package saved to {str(package_path.resolve())}")
