import os
import subprocess

from networking import get


def info(*args):
    if "DEBUG" in os.environ and os.environ["DEBUG"] in ["1", "TRUE", "True", "true"]:
        print(args)


def warning(*args):
    print(args)


def error(*args):
    print(args)


def download(url, path):
    info(f"Downloading {url} to {path}")
    data = get(url)
    if data is None:
        error(f"Could not download {url}")
    with open(path, "wb") as f:
        f.write(data)
