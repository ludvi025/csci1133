# csci1133

## unzip.py

Recursively unzip all zip files in the directory from which this is run.

## subcheck.py

Checks an unzipped submissions directory as downloaded from moodle. 

### Things to change before using subcheck.py:
    submission_directory_format = "HW0"
    submission_files = ["{x500}_0A.py", "{x500}_0B.py"]

### To run script:
`python subcheck.py <grades csv file> <unzipped submissions folder> -o <output filename>`

### Current labels:
* `bad_directory` - if the name of the top level directory is incorrect
* `no_sub` - if there is no submission associated with the student
* `extra_files` - doesn't indicate a problem with their submission, just lets us know they have extra files in their zip that they submitted
* `missing_file` - flag if one of the `submission_files` was not found in student directory.  This could mean that they named their file incorrectly or that they do not have the file
* `nested_folder` - indicates that the student directory contains a folder/file with the same name as `submission_directory_format`
