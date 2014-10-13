# Test grade entry acceleration
# Tom Postler, 2014-10-07

import argparse
import csv
import os
import stat
from sys import exit



# Globals
SECTIONS = False        # If we have sections to work with
PROBLEMS = 0            # Numbers of problems we're grading
POINTS   = None         # Maximum points for each problem
POINTS_T = None         # Maximum total points for the exam
GR_FILEN = "grades.csv" # File to save the grades in
LOG_FILE = None         # File object for the log file
LOG_CSVW = None         # csv.writer for the log file
LOG_SAFE = True         # Determines if .flush is used after every .writerow
STUDENTS = None         # The dictionary of student data
SM_PRINT = False        # If --fast is passed in



def main():
    # Get and handle the args
    args = ParseArgs()
    HandleArgs(args)

    # Get the grades
    # Format is a dict with key=ID, value=[scores]
    grades = InputGrades()

    # Make sure there aren't any issues with grade==None
    VerifyGrades(grades)

    # Write the grades
    OutputGrades(grades)



def VerifyGrades(grades):
    print()
    print(format("GRADING ISSUES", "-^80"))
    print("If there are any grading issues, would you like to replace the");
    choice = input("errors with -1 (y/n)? ")
    for sid in grades.keys():
        if None in grades[sid]:
            PrintInfo(sid, grades[sid], thin=True)
            if choice == 'y':
                for i in range(len(grades[sid])):
                    if grades[sid][i] == None:
                        grades[sid][i] = -1
            else:
                EditAGrade(grades, sid, force=True)
            
    print('-'*80 + '\n')



def InputGrades():
    grades = {}

    # Random catches and questions
    if not SM_PRINT:
        print("Enter an empty value for ID when you wish to finish")
    numgraded = 0

    # Main grading loop
    # Kill loop by [sid=='', sid==0]
    while True:
        # ID
        sid = EnterAValidId(grades)
        # Check if wanting to be done
        if sid == -1:
            return grades
        
        # If graded, offer to edit
        elif sid in grades.keys():
            PrintInfo(sid, grades[sid])
            if not SM_PRINT:
                if input("Would you like to edit (y/n)? ") == 'y':
                    EditAGrade(grades, sid)
            else:
                if input("e ") == 'y':
                    EditAGrade(grades, sid)
        # Not graded, so entering a grade mode
        elif sid in STUDENTS.keys():
            PrintInfo(sid)
            if numgraded < 10:
                newgrades = EnterAGrade()
            else:
                newgrades = EnterAGrade(False)
            while not newgrades:
                newgrades = EnterAGrade(False)
            if newgrades == -1:
                if not SM_PRINT:
                    print("Aborting entering grades for ID {}.".format(sid))
                else:
                    print("Bad grades, not stored.")
                continue
            grades[sid] = newgrades
            LogGrade(sid, newgrades)
            PrintInfo(sid, grades[sid], fresh=True)



def EnterAValidId(grades):
    sid = -1
    while sid == -1:
        sid = input('ID: ')
        if sid == '':
            return -1
        try:
            sid = int(sid)
        except ValueError:
            if not SM_PRINT:
                print("Try an integer.")
            sid = -1
            continue
        if (sid not in grades.keys()) and (sid not in STUDENTS.keys()):
            if not SM_PRINT:
                print("ID not found.")
            sid = -1
    return sid



def EnterAGrade(verbose=True):
    if verbose and not SM_PRINT:
        print("Enter grades, one per line, for all problems, or in num-val")
        print("format for select problems (e.g.\n> 1-5\n> 3-8\n> 4-0)")
        print("May also set all problems with one value (e.g. 0).")
        print("Pushing enter with no text (typing nothing) signals you do not")
        print("wish to enter a grade.")
        print("Pushing enter after typing in some values signals you wish to")
        print("finish entering input.")
    newgrades = []
    newgrade = input("> ")
    while newgrade != '':
        newgrades.append(newgrade.strip())
        newgrade = input("> ")
    # If one grade entered, attempt to apply to all problems
    if (len(newgrades) == 1) and ('-' not in newgrades[0]):
        # Signal not caring
        if newgrades[0] == '':
            return -1
        # Try for conversion
        try:
            newgrade = int(newgrades[0])
        except ValueError:
            if not SM_PRINT:
                print("Invalid grade entry: value not an integer: {}"
                      .format(newgrades[0]))
            return None
        if ValidGrades([newgrade]*PROBLEMS):
            return [newgrade]*PROBLEMS
    # If (0,PROBLEMS] entered, attempt to split by '-' for custom entering
    if 0 < len(newgrades) <= PROBLEMS:
        # If entered grades == PROBLEMS and none have '-', then atempt direct map
        if all('-' not in p for p in newgrades) and (len(newgrades) == PROBLEMS):
            try:
                newgrades = [int(g) for g in newgrades]
            except ValueError:
                if not SM_PRINT:
                    print("Invlaid grade entry; not an integer found: {}"
                          .format(newgrades))
                return None
            if ValidGrades(newgrades):
                return newgrades
            else:
                if not SM_PRINT:
                    print("Invalid grade entry; some grade OOB: {}"
                          .format(newgrades))
                    print("Max value(s):", POINTS)
                return None
        # Something doesn't have a '-' delimiter
        elif any('-' not in p for p in newgrades):
            if not SM_PRINT:
                print("Fewer than the total number of problems was specified")
                print("without using the num-val format.")
            return None
        # Everything has a '-' delimiter
        else:
            grades = [None]*PROBLEMS
            for newgrade in newgrades:
                newgrade = newgrade.split('-')
                # Verify #-# vs #-#-#
                if len(newgrade) != 2:
                    if not SM_PRINT:
                        print("Invalid number of items, must be =2: {} in {}"
                              .format(len(newgrade), newgrade))
                    return None
                # Verify #-# vs a-a
                try:
                    newgrade = [int(x) for x in newgrade]
                except ValueError:
                    if not SM_PRINT:
                        print("Invalid grade entry; something is not an integer: {}"
                              .format(newgrade))
                    return None
                # Verify problem number is in bounds
                if (newgrade[0] <= 0) or (newgrade[0] > PROBLEMS):
                    if not SM_PRINT:
                        print("Invalid grade entry; problem number OOB: {}"
                              .format(newgrade[0]))
                    return None
                # Verify grade value is in bounds
                if not ValidGrade(newgrade[1], newgrade[0]):
                    if not SM_PRINT:
                        print("Invalide grade entry; grade value OOB: {}"
                              .format(newgrade[1]))
                    return None
                # It should be okay by now
                grades[newgrade[0]-1] = newgrade[1]
            return grades
    # Too many grades entered
    if len(newgrades) > PROBLEMS:
        if not SM_PRINT:
            print("Invalid grade entry; too many grades >{}: {}"
                  .format(PROBLEMS, len(newgrades)))
        return None
    # No grades entered, so assume cancellation
    if len(newgrades) == 0:
        if not SM_PRINT:
            print("No grades entered. Assuming you wish to cancel this entry.")
        return -1
    # Default
    return None



def EditAGrade(grades, sid, force=False):
    if not SM_PRINT:
        print(format("EDIT GRADE", "-^40"))
        print("Current grades for {} are {}."
              .format(sid, ', '.join([str(g) for g in grades[sid]])))
    else:
        print("{0:8} old: {1}"
              .format(sid, ', '.join([str(g) for g in grades[sid]])))
    newgrades = EnterAGrade(False)
    if force:
        while not newgrades or (None in newgrades):
            print("Try again.")
            newgrades = EnterAGrade(False)
    else:
        while not newgrades:
            newgrades = EnterAGrade(False)

    if newgrades == -1:
        print("Grades not updated.")
    else:
        # Only update grades that are not None
        for i in range(PROBLEMS):
            if newgrades[i]:
                grades[sid][i] = newgrades[i]
        LogGrade(sid,grades[sid])
        if not SM_PRINT:
            print("New grades for {} are {}."
                  .format(sid, ', '.join([str(g) for g in grades[sid]])))
        else:
            print("{0:8} new: {1}"
                  .format(sid, ', '.join([str(g) for g in grades[sid]])))
    if not SM_PRINT:
        print('-'*40 + '\n')



def PrintInfo(sid, grades=None, fresh=False, thin=False):
    if (thin or SM_PRINT) and grades:
        student = STUDENTS[sid]
        print("{}, {} {}, sec {}, grades: {}, tot: {}\n"
              .format(sid, student[0], student[1], student[3],
                      ' '.join([str(g) for g in grades]),
                      sum([g for g in grades if g != None])))
        return

    print()
    if not SM_PRINT:
        if fresh:
            print(format("UPDATED GRADES", "-^40"))
        else:
            print(format("STUDENT INFO", "-^40"))
        student = STUDENTS[sid]
        print("ID:    ", sid)
        print("FName: ", student[0])
        print("LName: ", student[1])
        if SECTIONS:
            print("Sect:  ", student[3])
        if grades:
            print("Grades:", ', '.join([str(g) for g in grades]))
            tot = sum([g for g in grades if g != None])
            per = ''
            if POINTS:
                per = "{0:04.1f}%".format(tot/POINTS_T*100)
            print("Total: ", tot, per)
        print('-'*40 + '\n')
    else:
        student = STUDENTS[sid]
        print("{}, {} {}, sec {}\n"
              .format(sid, student[0], student[1], student[3]))



def ValidGrades(grades):
    """Requires a list argument the same length as POINTS"""
    if len(grades) != PROBLEMS:
        return False
    for i in range(PROBLEMS):
        if not ValidGrade(grades[i], i+1):
            return False
    return True



def ValidGrade(grade, problem):
    if (problem <= 0) or (problem > PROBLEMS) or (grade < 0):
        return False
    if not POINTS:
        return True
    if isinstance(POINTS, int) and (grade <= POINTS):
        return True
    if isinstance(POINTS, list) and (grade <= POINTS[problem]):
        return True
    return False



def OutputGrades(grades):
    LOG_FILE.close()
    append = 'y'
    if os.path.isfile(GR_FILEN):
        append = input("Append to existing grade file (y/n, default y)? ")
    if append == 'n':
        fout = open(GR_FILEN, 'w', newline='')
    else:
        fout = open(GR_FILEN, 'a', newline='')
    writer = csv.writer(fout)
    firstrow = []
    if SECTIONS:
        firstrow = ['ID number','First name','Last name','Username','Section']
    else:
        firstrow = ['ID number','First name','Last name','Username']
    firstrow += [str(n) for n in list(range(1,PROBLEMS+1))]
    firstrow.append('Total')
    if append == 'n':
        writer.writerow(firstrow)
    for sid, grade in grades.items():
        row = []
        row.append(sid)
        row += STUDENTS[sid]
        row += grade
        row.append(sum([g for g in grade if g >= 0]))
        writer.writerow(row)
    fout.close()
    os.chmod(GR_FILEN, (os.stat(GR_FILEN).st_mode & (stat.S_IRWXU | stat.S_IRWXG))
             | stat.S_IRGRP | stat.S_IWGRP)
    os.remove(LOG_FILE.name)



def LogGrade(sid, grade):
    row = []
    row.append(sid)
    row += STUDENTS[sid]
    row += grade
    LOG_CSVW.writerow(row)
    if LOG_SAFE:
        LOG_FILE.flush()



def HandleArgs(args):
    # Handle sections
    global SECTIONS
    SECTIONS = args.sections

    # Handle num_problems
    if args.num_problems <= 0:
        exit("Invalid number of problems: " + str(args.num_problems))
    global PROBLEMS
    PROBLEMS = args.num_problems

    # Figure out points
    global POINTS
    global POINTS_T
    if args.points:
        if len(args.points) == args.num_problems:
            POINTS = list(args.points)
            POINTS_T = sum(POINTS)
            print("Point values for your {} problems are:".format(PROBLEMS))
            print("    " + str(POINTS))
        elif len(args.points) == 1:
            POINTS = args.points[0]
            POINTS_T = POINTS*PROBLEMS
            print("Point value for each of the {} problems is {}.".format(PROBLEMS, POINTS))
        else:
            errorstr = "Incorect number of points arguments specified.\n"
            errotstr = "    1 or {} expected, got {}.".format(PROBLEMS, len(args.points))
            exit(errorstr)
    else:
        print("Point value not specified. Point max is infinite for each problem.")

    # Grading file name
    global GR_FILEN
    GR_FILEN = args.name + '_grades_' + os.getlogin() + '.csv'
    exists = os.path.isfile(GR_FILEN)
    print("Grade file name:", GR_FILEN)
    try:
        f = open(GR_FILEN, 'a', newline='')
    except OSError as e:
        exit("Unable to open grading file: {}".format(e.strerror))
    else:
        f.close()
        if not exists:
            os.remove(GR_FILEN)

    # Log file
    global LOG_FILE
    log_filen = GR_FILEN + '.log'
    print("Log file name:", log_filen)
    try:
        LOG_FILE = open(log_filen, 'w', newline='')
    except OSError as e:
        exit("Unable to open log file: {}".format(e.strerror))
    global LOG_CSVW
    LOG_CSVW = csv.writer(LOG_FILE)
    firstrow = []
    if SECTIONS:
        firstrow = ['ID number','First name','Last name','Username','Section']
    else:
        firstrow = ['ID number','First name','Last name','Username']
    firstrow += [str(n) for n in list(range(1,PROBLEMS+1))]
    LOG_CSVW.writerow(firstrow)

    # Safe logging
    global LOG_SAFE
    LOG_SAFE = not args.unsafe_logging
    if not LOG_SAFE:
        print("You have chosen to use the faster, but unsafe, logging.")

    # Get the student file csv
    global STUDENTS
    STUDENTS = GetStudents(args.s_info_file)

    # Get the fast print setting
    global SM_PRINT
    SM_PRINT = args.fast
    if args.fast:
        print("You have elected to use minimalistic printing.")



def GetStudents(filename):
    """Takes in a csv file and returns a dictionary of students where key=ID and
    value=[First name, Last name, Username, Section(optional)]"""
    # Open the file
    if not os.path.isfile(filename):
        exit(filename + " does not exist.")
    file = open(filename, newline='')

    # Get the first row and check for headers and section nums
    reader = csv.reader(file)
    firstline = next(reader)
    explen = 5 if SECTIONS else 4
    length = len(firstline)
    if length != explen:
        errorstr =  "Incorrect number of columns in " + filename + ':\n'
        errorstr += "    Expected {}, but got {}.".format(explen, length)
        exit(errorstr)
    if firstline == ['ID number','First name','Last name','Username','Section']:
        print("Header row detected in csv file. Skipping first line.")
        firstline = next(reader)
    else:
        print("Header row not detected in csv file. Using first row as data:")
        print("    " + str(firstline))

    # Accumulate the students    
    students = {int(firstline[0]): firstline[1:]}
    for row in reader:
        students[int(row[0])] = row[1:]
    print("   Found {} students.".format(len(students)))

    #Cleanup and return
    file.close()
    return students
    


def ParseArgs():
    desc = \
"""A simple console-based program to input grades using students' ID numbers and
the individual problem totals as fast as possible.

The program will prompt you, but the gist of it is that all you need to do is
enter the student ID and the point values for each problem. This program will
then tell you if any of the values you entered are invalid and allow you to
correct them, it will tell you the sum for the scores you entered, and it will
let you know how many are remaining.

This script will maintain a log file of every grade entered or edited. This is
not to be used for submission, but moreso as a way of handling any errors that
may arise, such as a user of this program pushing Ctrl-C. This log file will be
deleted upon a successful write of the grade file.

Note: If you attempt to do something stupid (like specify a grade for the same
      problem 5 times) then your result will most likely match that stupidity.
      This script can catch and handle typos, but not stupidity.

Note: If you enter nothing at a (y/n) prompt, then it will be assumed you wanted
      to enter an 'n' unless otherwise stated."""
    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument('num_problems', type=int,
                        help="The number of problems available on the test")
    
    parser.add_argument('name', help="The name of the graded item (e.g. mt1)")
    
    parser.add_argument('--points', '-p', metavar='N', nargs='+', type=int, help=
"""If only one specified, then that value will be used
as a maximum amount of points possible for num_problems
(e.g. if each problem was worth 10 points). Otherwise,
you may specify as many point values as you like
(ideally as many as there are num_problems) to specify a
point value for each problem. This is used as error
checking for your input as well as some rudimentary
statistics."""
    )
    
    parser.add_argument('s_info_file', help=
"""A csv file exported from Moodle with the student's
first name, last name, ID number, UMN email address
(username), and section number in that order.

Column headings that this script can recognize are the
ones that are used in a Moodle export. If the following
line is not the first line in the csv (EXACTLY as it is
shown), then this script will assume there is no header
row:

ID number,First name,Last name,Username,Section"""
    )
    
    parser.add_argument('--sections', '-s', action='store_true', help=
"""Specify this flag if there are section numbers
specified in the s_info_file."""
    )

    parser.add_argument('--fast', '-f', action='store_true', help=
"""Specify this flag if you want the output to be
dramatically reduced. This flag will set the I/O scheme
to be very minimalistic, so this flag is NOT recommended
if you have not run the program before."""
    )

    parser.add_argument('--unsafe-logging', action='store_true', help=
"""Specify this flag if you want the log file to not
flush itself after every entry. Otherwise, the log file
will flush after every successful grade entry or
modification."""
    )
    
    return parser.parse_args()



if __name__ == '__main__':
    main()

# Can use a parameter in a function print=print to override print command
# If want no printing, then use print=lambda *args: None
# Wonderful awful python hack :)
