# Cleaning up grade files

from os import remove
import lib.rfind as rfind

def RemoveUnfinished(grade_file_name):
    _cleanupIncompletes(grade_file_name, False)


def RemoveInProgress(grade_file_name):
    _cleanupIncompletes(grade_file_name, True)



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
    if len(found_files) > 0:
        if inprogress_check:
            print("Found and removed the following in progress files:")
        else:
            print("Found and removed the following unfinished files:")
        for fn in found_files:
            print(fn)
    else:
        print("No files to remove.")
