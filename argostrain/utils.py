import os
import subprocess

def info(*args):
    if 'DEBUG' in os.environ and \
            os.environ['DEBUG'] in ['1', 'TRUE', 'True', 'true']:
        print(args)

def warning(*args):
    print(args)

def error(*args):
    print(args)

def download(url, path):
    url = str(url)
    path = str(path)
    res = subprocess.run(['curl', '--retry', '25', '-o', path, url])
    return res.returncode

