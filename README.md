# CSCI 1133 Scripts

## runzip.py

Recursively unzip all zip files in the directory from which this is run.

## sub_parser.py

    import sub_parser
    student_info = sub_parser.parse(path)

Given a filepath, get the students first name, last name, and moodle id.  

## sub_check.py

Checks an unzipped submissions directory as downloaded from moodle. 

### Things to change before using subcheck.py:
    submission_directory_format = "HW0"
    submission_files = ["{x500}_0A.py", "{x500}_0B.py"]
    SENDMAIL = "/usr/sbin/sendmail"
    TA_email = "yourx500@umn.edu"
    course_name = " DEPT XXXX "
    email_subject = "DEPT XXXX - Submission Error"

### To run script
`python subcheck.py <grades csv file> <unzipped submissions folder> -o <output filename>`

### Current labels
* `bad_directory` - if the name of the top level directory is incorrect
* `no_sub` - if there is no submission associated with the student
* `extra_files` - doesn't indicate a problem with their submission, just lets us know they have extra files in their zip that they submitted
* `missing_file` - flag if one of the `submission_files` was not found in student directory.  This could mean that they named their file incorrectly or that they do not have the file
* `nested_folder` - indicates that the student directory contains a folder/file with the same name as `submission_directory_format`

## grade_homework.py

* Builds a list of homework files by walking the directory tree from the current directory
and matching files based on unix filename patterns.
* Outputs the file contents and runs one or more tests against each student submission,
outputting the result.
* Offers to drop into a python shell with the student submission loaded as a model for
flexible testing.
* Offers to enter a text editor to fix a typo in the script and see how the script would
have worked otherwise.
* Creates individual grade files for each submission.
* Consolidates all grades into a single CSV file

### To run script

Run the script in the unzipped submissions folder using:

    python grade_homework.py 

### Sessions
The script uses the session name to label the individual grade files it creates
for each student before they are consolidated so that multiple graders can work
in a single submission directory at once. It also saves the list of filename 
patterns and test scripts so they do not have to be reentered. If you would like
to change the filename patterns or test scripts, either modify the .session file 
that is created or delete it and it will prompt you again.

### Filename patterns
When prompted for filename patterns, enter one or more Unix filename patterns 
that should be used to identify homework files. For example, if all valid 
submissions end with "4a.py", you could enter `*4a.py` or `*4a.py, *4A.py` to
allow for either case of the last letter.

### Test scripts
When prompted to enter tests to run against student homework, enter one or more
paths to python scripts that should be run against the submission. Student code
is contained in a python module named `student_module` so to call a function 
name `unittest()` that should have been defined by the student would look like:

    student_module.unittest()

or something more flexible:

    try:
        student_module.unittest()
    except:
        try:
            student_module.unitTest()
        except:
            pass

### 'Enter python shell?'
After running the test scripts and dumping the file contents, the script asks if
you would like to 'Enter a python shell (y/n)?'. Entering 'y' will open an interactive
subprocess of python with the student's script loaded in the global namespace. 
The actual command used is `python -i student_script.py`. This allows you to 
try custom commands quickly.

### 'Edit the file?'
The script will also offer to open the script in an editor subprocess, so you can
quickly fix typos and see how the script would have run otherwise. After editing,
the script offers to drop back into a shell or run the tests again.
