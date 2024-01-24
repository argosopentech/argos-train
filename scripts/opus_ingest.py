# Download and package OPUS data as a .argosdata file
import os
import argparse
import shutil
import zipfile
import logging
import logging.handlers
import json
import subprocess
import urllib.request
import urllib.parse
import urllib.error

import zipfile

def setup_logger(slug):
    # Set up logging
    logger = logging.getLogger(slug)
    logger.setLevel(logging.DEBUG)
    # Create a rotating file handler
    logHandler = logging.handlers.RotatingFileHandler(f'{slug}.log', maxBytes=1000000, backupCount=5)
    logHandler.setLevel(logging.DEBUG)
    # Create a logging format
    logFormatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logHandler.setFormatter(logFormatter)
    # Add the handlers to the logger
    logger.addHandler(logHandler)
    # Create a console handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.INFO)
    consoleHandler.setFormatter(logFormatter)
    # Add the handlers to the logger
    logger.addHandler(consoleHandler)
    return logger

def download_opus(output_dir, slug, opus_url, source_code, target_code, logger):
    # Make sure the output directory exists
    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    # Download the OPUS data from the given URL
    # Use the Python standard library to download the data
    # If that fails, use wget

    def download(url, output_dir):
        logger.info('Downloading %s to %s', url, output_dir)
        try:
            # Use the Python standard library to download the data
            urllib.request.urlretrieve(url, output_dir)
        except:
            # If that fails, use wget
            subprocess.call(['wget', '-O', output_dir, url])

    # Download the OPUS data from the given URL
    DOWNLOAD_FILENAME = f"{source_code}-{target_code}.txt.zip"

    download(opus_url, output_dir / DOWNLOAD_FILENAME)

    # Unzip the downloaded file
    with zipfile.ZipFile(output_dir / DOWNLOAD_FILENAME, 'r') as zip_ref:
        zip_ref.extractall(output_dir)

    # Move NLLB.en-et.en to source.txt
    shutil.move(output_dir / 'NLLB.en-et.en', output_dir / 'source.txt')
    
    # Move NLLB.en-et.et to target.txt
    shutil.move(output_dir / 'NLLB.en-et.et', output_dir / 'target.txt')
    
    # Delete NLLB.en-et.scores
    os.remove(output_dir / 'NLLB.en-et.scores')
    
    # Make package directory
    package_dir = output_dir / f"data-{slug}-{source_code}-{target_code}"
    package_dir.mkdir(parents=True)
    
    # Move source.txt to package directory
    shutil.move(output_dir / 'source.txt', package_dir / 'source.txt')
    
    # Move target.txt to package directory
    shutil.move(output_dir / 'target.txt', package_dir / 'target.txt')

    """
    # Example metadata.json
    ```
    {
        "name": "NLLU",
        "type": "data",
        "from_code": "en",
        "to_code": "it",
        "size": 14025542,
        "reference": "The source text comes from Paracrawl (https://paracrawl.eu/). We do not own any of the source text from which this data has been translated. We license the translated text and packaging of this parallel data under the Creative Commons Attribution 4.0 International (CC BY 4.0). Please cite \"LibreTranslate\" if you use the translated data.",
        "links": [
            "http://data.argosopentech.com/data-nllu-en_it.argosdata"
        ]
    }
    ```
    
    """
    
    # Create metadata.json
    metadata = {
        "name": slug,
        "type": "data",
        "from_code": source_code,
        "to_code": target_code,
        "size": os.path.getsize(package_dir / 'source.txt'),
        "reference": "The source text comes from OPUS (https://opus.nlpl.eu/). We do not own any of the source text from which this data has been translated. We license the translated text and packaging of this parallel data under the Creative Commons Attribution 4.0 International (CC BY 4.0). Please cite \"LibreTranslate\" if you use the translated data.",
        "links": [
            f"http://data.argosopentech.com/data-{slug}-{source_code}_{target_code}.argosdata"
        ]
    }
    
    # Write metadata.json
    with open(package_dir / 'metadata.json', 'w') as f:
        json.dump(metadata, f)
        
    # Create package
    shutil.make_archive(package_dir, 'zip', package_dir)
    
    # Move package to current directory
    shutil.move(f"{package_dir}.zip", f"data-{slug}-{source_code}_{target_code}.argosdata")

    
    
if __name__ == '__main__':
    # Parse args
    parser = argparse.ArgumentParser(description='Download and package OPUS data as a .argosdata file')
    parser.add_argument('-o', '--output', help='Output directory', required=True)
    parser.add_argument('-p', '--slug', help='Package slug', required=True)
    parser.add_argument('-u', '--url', help='Opus download URL (moses format) (https://opus.nlpl.eu/)', required=True)
    parser.add_argument('-s', '--source', help='Source language code', required=True)
    parser.add_argument('-t', '--target', help='Target language code', required=True)
    args = parser.parse_args()

    # Set up logging
    logger = setup_logger(args.slug)

    download_opus(args)


