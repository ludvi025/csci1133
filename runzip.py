#!/usr/bin/python3

# Unzips all files in the directory its run and then unzips all zipped
# files in files just unzipped.

import zipfile as z, os, argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("zip_file")
    zipfile = (parser.parse_args()).zip_file
    unzip(zipfile)

def getOutputDir(file_name):
    return '.'.join(file_name.split('.')[0:-1])

def unzipAll(path=os.getcwd()):
    for f in os.listdir(path):
        full_name = os.path.join(path,f)
        if z.is_zipfile(full_name):
            z.ZipFile(full_name).extractall(getOutputDir(full_name))

    if path != os.getcwd():
        for f in os.listdir(path):
            full_name = os.path.join(path,f)
            if z.is_zipfile(full_name):
                os.remove(full_name)

    for f in os.listdir(path):
        if os.path.isdir(f):
            unzipAll(os.path.join(path,f))

def unzip(path):
    if z.is_zipfile(path):
        unzipped_name = getOutputDir(path)
        z.ZipFile(path).extractall(unzipped_name)
        os.remove(path)

        for filename in os.listdir(unzipped_name):
            unzip(filename)

if __name__ == "__main__":
    main()
