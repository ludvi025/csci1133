# Cleaning up grade files

from os import remove
import lib.rfind as rfind

def RemoveUnfinished(grade_file_name):
    files_found = _cleanupIncompletes(grade_file_name, False)
    if len(files_found) > 0:
        print("Found and removed the following unfinished files:")
        for fn in files_found:
            print(fn)


def RemoveInProgress(grade_file_name):
    files_found = _cleanupIncompletes(grade_file_name, True)
    if len(files_found) > 0:
        print("Found and removed the following in progress files:")
        for fn in files_found:
            print(fn)


def _cleanupIncompletes(grade_file_name, inprogress_check):
    files = rfind.find(grade_file_name, '.')
    found_files = []
    for fn in files:
        with open(fn, 'r') as f:
            filetext = f.read()
        if ((not inprogress_check and "Grading unfinished for" in filetext) or
            (inprogress_check and "Grading in progress for" in filetext)):
            found_files.append(fn)
            remove(fn)
    return found_files