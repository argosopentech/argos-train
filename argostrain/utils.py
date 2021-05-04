import os

def info(*args):
    if 'DEBUG' in os.environ and \
            os.environ['DEBUG'] in ['1', 'TRUE', 'True', 'true']:
        print(args)

def warning(*args):
    print(args)

def error(*args):
    print(args)

