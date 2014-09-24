#!/usr/bin/python3

# Unzips all files in the directory its run and then unzips all zipped
# files in files just unzipped.

import zipfile as z, os, argparse
import lib.rfind as rfind, lib.sub_parser as sub_parser, lib.runzip as runzip

def main():
    args = parseArgs()
    runzip.unzip(args.input)
    root_dir = runzip.getOutputDir(args.input)
    file_map = mapMoodleIdsToFiles(root_dir)
    # print(file_map)
    normalizeDirectory(root_dir, file_map)

# Rearrange the files so all files are placed directly under
# a directory with the students moodle id as its name
def normalizeDirectory(root, file_map):
    # For each moodle id, create a new directory and move all 
    # the items in the list into that new directory, removing
    # any residual directories.

    for moodle_id in file_map:
        d = os.path.join(root, moodle_id)
        if not os.path.isdir(d):
            os.mkdir(d)
        for file_path in file_map[moodle_id]:
            f = file_path.split(getJoinStr())[-1]
            print(f)
            os.renames(file_path, os.path.join(root, moodle_id, f))

def getJoinStr():
    return os.path.join('.','.')[1:-1]

def mapMoodleIdsToFiles(directory):
    file_map = {}
    # Walk the directory
    for root, dirs, files in os.walk(directory):
    # For everything in the directory that has a moodleid in the 
    # name, add it to the list for that moodleid
        for f in files:
            info = sub_parser.parse(f)
            if info:
                moodle_id = info["moodleid"]
                if moodle_id not in file_map:
                    file_map[moodle_id] = []
                file_map[moodle_id].append(os.path.join(root, f))
        for d in dirs:
            info = sub_parser.parse(d)
            if info:
                moodle_id = info["moodleid"]
                if moodle_id not in file_map:
                    file_map[moodle_id] = []
                file_map[moodle_id].append(os.path.join(root, d))
    return file_map

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    return parser.parse_args()

if __name__ == "__main__":
    main()
