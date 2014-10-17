# CSCI 1133 Grading Scripts Walkthrough

This walkthrough explains step-by-step how to use the grading scripts provided in
this repository for one batch of homework files, from downloading and unpacking the
files to uploading the grades to moodle, with multiple users running the grading
script at once.

*Make sure python >= 3.2 is used with all grading scripts*

# 1. Setup the working directory

First, we need to setup the working directory. Start by creating a new directory
`hw_grading` and downloading the homework submissions as a single zip file from 
the class moodle site and placing it in this new directory. Rename it 
`hw_files.zip`.

Next, we need to fetch the grading scripts from github. From within `hw_grading`, 
run:

    git clone https://github.com/ludvi025/csci1133; 
    mv csci1133 scripts;

Next we need to "unpack" the grading submissions. Run the following command from
within `hw_grading`:

    python scripts/unpack.py hw_files.zip

This will recursively unzip `hw_files.zip` and place individual submissions into 
folders named with their moodle submission id.

# 2. Setup the grading session

Now we need to setup the grading session so the appropriate files are selected
and multiple users can grade at once.

Enter the newly created `hw_files` directory and run:

    python ../scripts/grade_homework.py

You will be prompted to enter a name for the session. This is what allows multiple
users to grade at the same time and we will distribute this name once we have setup
the session. For this walkthrough, use `hw`.

Next you will be asked to enter a list of "UNIX file name patterns". This is how 
the grading script will identify which files need grading. For example, if all 
python files in `hw_files` need to be graded, enter `*.py`. Or if there is a 
specific naming, something more detailed can be used.

The next prompt asks for a list of paths to tests to run against the scripts. See
the "Test scripts" section of README.md for more info on how to write tests.

Last, enter in the max number of points for the assignment. This will be used to
verify grades input during the session.

# 3. Running the grading script

After entering the points in the assignment, the script will find all homework 
files and begin the process of grading them. At this point, all graders should
enter the `hw_files` directory and run:

    python ../scripts/grade_homework.py

and enter the session name used in (2), in this case `hw`. All users can now begin
grading by following the prompts in the grading script and the script will keep
track of who is grading what.

In the event that the script crashes, or a student's code enters an infinite loop
and the grader has to Ctrl+C out of the script, simply rerun the grading script and
enter the same session name to resume grading.

When there are no more files to grade, the script will ask if you'd like to "Check
for incomplete grade files?". Once everyone reaches this screen, one person should
enter "y". The script will then check for any files that did not get graded
correctly because of a crash and reset them to be graded again. If any files are
found, rerun the grading script to grade them.

# 4. Consolidating grading files

Once all files have been graded, it is time to consolidate them into a single
CSV gradebook file. If you would like to append the student's id to each record,
skip to (ii) below.

(i) To consolidate grades run the following command from within `hw`:

    python ../scripts/consolidate_grade_files.py hw_grades.csv --session hw

When prompted to delete the individual grading files, enter 'n' unless you know
what you're doing.

All student grades will now be consolidated into `hw_grades.csv`.

(ii) To consolidate grads and append the student's id to each record, we first
need to download from moodle a csv file with all students' first and last names
and their student ids. Eg:

    Id number,First name,Last name
    1111111,Aarty,Aardvark
    2222222,Billy,Bob

Place this file in `hw` and call it `stud_info.csv`. **Make sure the first row is either exactly like the row in the example, or that there is no header row**.

Now run the following command from within `hw`:

    python ../scripts/consolidate_grade_files.py grades.csv -u stud_info.csv -s hw

All student grades will now be consolidated into `hw_grades.csv` with their user
ids in the first column. If a user id was not found for a person, `#######` will 
appear instead and will have to be filled in manually.

Hooray! This file can now be uploaded directly to moodle!
