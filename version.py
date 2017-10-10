from json import load as loadJSON
from os import path
from sys import argv

BASEDIR = path.realpath(path.dirname(argv[0]))
PACKAGE_FILE_NAME = path.join(BASEDIR, 'package.json')

with open(PACKAGE_FILE_NAME, 'r') as package_json_file:
    VERSION = loadJSON(package_json_file)['version']
