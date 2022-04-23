import glob
from argparse import ArgumentParser
from os import listdir
from os.path import abspath, isfile, join

import ffmpeg
import pandas as pd
from watchfiles import watch

import watcher

parser = ArgumentParser(
    description="Watch a directory and construct an XML file",
    add_help=True,
    usage="[options] directory")
parser.add_argument("--output", dest="output", default="video.xml")
parser.add_argument("--extension", "-e", nargs="*", default=["mp4"])
parser.add_argument("directory", metavar="directory")

args = parser.parse_args()

extensions = args.extension
directory = abspath(args.directory)

# First read the files in the directory
existing_files = []
for ext in extensions:
    existing_files.extend(glob.glob("{}/*.{}".format(directory, ext)))

df = pd.DataFrame()

for f in existing_files:
    file_df = watcher.process_file(f)
    df = pd.concat([df, file_df])

print(df)

for changes in watch(directory):
    print(changes)
