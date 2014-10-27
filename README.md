# CSCI 1133 Grading Scripts

*See WALKTHROUGH.md for a basic usage walkthrough.*

## unpack.py

Unpacks a submission directory into a standard format.

### Usage:
    python unpack.py submission_download.zip

`submission_download_file.zip` must be the file downloaded from Moodle. Unzips `submission_download_file.zip` and any zip files contained within it and sorts the files into folders based on their Moodle ID. The folders are named with the Moodle ID as well. This should be run before `sub_check.py` and the resulting directory passed to `sub_check.py`.

## sub_check.py

Checks an unpacked submissions directory as downloaded from moodle. 

### Synopsis:
    python student_info_file submissions_dir [options]

    student_info_file : CSV file containing student information. Downloadable from Moodle.
    submissions_dir   : The directory that was created by `unpack.py` from the Moodle submission download.

    Options
    -------
    --config (-c) file : Uses file as the options file as specified below. 
    --send_email (-e)  : If specified, actually sends emails. Otherwise just dumps the emails that would be sent to "email_dump.txt".
    --output (-o) file : If specified, dumps info about each submission to file.

### Config File
The "--config" flag is used to specify an ini file which contains options for sub\_check.py. See "sub\_check\_opts.cfg" for an example.

The following options are available:
* email : The email of the TA using the script.
* course : The course the script is being used for.
* subject : The subject line of the email to be sent.
* files : A python list of filename templates to be matched. 

### Tags:
Currently, sub\_check.py tags submissions in the following cases:
* No submission. Students will not receive an email for this tag.
* Correct submission. Students will not receive an email for this tag.
* Extra/missing files.
* Nested directories.
* Extra directories.
* Incorrectly named files.

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
paths to python scripts that should be run against the submission. A separate
instance of python will be created in interpretive mode and the student's code 
imported into the global namespace. The lines from the test script will be piped
into the new instance of python, allowing you to both call functions and pass
input into them.

For example, if students' were to define a function such as:

    def foo(a,b):
        return a+b

An example test script would be:

    print('Calling `foo(5,4)`. Expecting `9`')
    print(foo(5, 4))

For another example, if students' were to take input from the user such as:
    
    def getInput():
        s = input('> ')
        print(s)

An example test script would be:

    print('Calling `getInput()` and piping in `Apple`')
    getInput()
    Apple

This is acceptable because the script is piped one line at a time into the new
interpreter. Because of this, testing scripts can also be written for scripts
that do not have functions or ask for input immediately upon import. For example, 
if the student's code looks like:

    s = input('Enter a number: ')
    print(int(s) + 1)

An example test script would be:

    5
    print('Entered `5`. Expected `6`')
     
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

## consolidate_grade_files.py

Consolidates invididual student grade files for a single problem into one gradebook.

### Usage:

    python consolidate_grade_files.py [output_file_name] [options]

    Options:
    --session (-s) : The session used in `grade_homework.py`

    Eg:
    python consolidate_grade_files.py hw2_grades.csv -s hw2

## consolidate_problems.py

Consolidates [input-files] grading files from individual files into a single file. 

### Usage:

    python consolidate_problems.py [input-files] [options]

    Options:
    --output (-o) : File to write consolidated gradebook to.
    --key (-k)    : Key used to identify students. Defaults to "Moodle id".
