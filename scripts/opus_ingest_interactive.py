import opus_ingest

import pathlib

if __name__ == "__main__":
    print("This script will download and package OPUS data as a .argosdata file")
    print("See https://opus.nlpl.eu/ for more information about OPUS")

    source_code = input("Enter source language code: ")
    target_code = input("Enter target language code: ")

    slug = input("Enter package slug: ")

    opus_url = input("Enter OPUS download URL (moses format) (https://opus.nlpl.eu/): ")

    path = pathlib.Path.cwd()

    output_dir = path / slug

    logger = opus_ingest.setup_logger(slug)

    opus_ingest.download_opus(output_dir, slug, opus_url, source_code, target_code, logger)

