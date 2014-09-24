#!/usr/bin/python3

# Unzips all files in the directory its run and then unzips all zipped
# files in files just unzipped.

import zipfile as z, os, argparse
import rfind

def main():
    zfile = getZipArg()
    # unzipAll(zfile)
    unzip(zfile)

def getOutputDir(file_name):
    return '.'.join(file_name.split('.')[0:-1])

# def unzipAll(path=os.getcwd()):
#     for f in os.listdir(path):
#         full_name = os.path.join(path,f)
#         if z.is_zipfile(full_name):
#             z.ZipFile(full_name).extractall(getOutputDir(full_name))

#     if path != os.getcwd():
#         for f in os.listdir(path):
#             full_name = os.path.join(path,f)
#             if z.is_zipfile(full_name):
#                 os.remove(full_name)

#     for f in os.listdir(path):
#         if os.path.isdir(f):
#             unzipAll(os.path.join(path,f))

def unzip(file_name, path=""):
    full_path = os.path.join(path, file_name) if path != ""  else file_name
    print(full_path)

    if os.path.isdir(full_path):
        for fn in os.listdir(full_path):
            unzip(fn, full_path)
    elif z.is_zipfile(full_path):
        print('\tiszip')
        unzipped_name = getOutputDir(full_path)
        z.ZipFile(full_path).extractall(unzipped_name)
        if path != "":
            os.remove(full_path)

        for fn in os.listdir(unzipped_name):
            unzip(fn, unzipped_name)

def getZipArg():
    parser = argparse.ArgumentParser()
    parser.add_argument("zip_file")
    return (parser.parse_args()).zip_file

def test():
    zfile = getZipArg()
    z.ZipFile(zfile).extractall()

if __name__ == "__main__":
    main()
    # test()