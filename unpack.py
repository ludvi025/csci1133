#!/usr/bin/python3

# Unzips all files in the directory its run and then unzips all zipped
# files in files just unzipped.

import zipfile as z, os, argparse, sub_parser, runzip

def main():
    args = parseArgs()
    # root_dir = runzip.unzipAll(args.input)
    # runzip.unzipAll()
    # root_dir = getOutputDir(args.input)
    root_dir = args.input
    file_map = mapMoodleIdsToFiles(root_dir)
    normalizeDirectory(root_dir, file_map)

def getOutputDir(file_name):
    return '.'.join(file_name.split('.')[0:-1])

# Unzip 'zip_file' and any zip files nested within it
# def runzip(zip_file, delete=False, depth=0):
    # if z.is_zipfile(zip_file):
    #     output_dir = getOutputDir(zip_file)
    #     z.ZipFile(zip_file).extractall(output_dir)
    #     for file_name in os.listdir(output_dir):
    #         runzip(os.path.join(output_dir, file_name), True, depth+1)
    #     if delete:
    #         os.remove(zip_file)
    #     return output_dir
    # elif os.path.isdir(zip_file):
    #     for file_name in os.listdir(zip_file):
    #         runzip(os.path.join(zip_file, file_name), True, depth+1)

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
            os.renames(file_path, os.path.join(root, moodle_id, file_path.split(getJoinStr())[-1]))

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
