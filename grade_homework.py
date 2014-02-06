#!/usr/bin/python3
import os, importlib, sys, fnmatch, subprocess

# Returns a list of full path names, like the unix 'find' command
def find(pattern, directory):
    matches = []
    for root, dirs, files in os.walk(directory):
        for f in files:
            if fnmatch.fnmatch(f,pattern):
                path = os.path.join(root,f)
                matches.append(path)
    return matches

def getJoinStr():
    return os.path.join('.','.')[1:-1]

# Returns a module object for the filename passed
def importScript(rel_path):
    root = os.getcwd()
    join_str = getJoinStr()
    rel_dir = join_str.join(rel_path.split(join_str)[1:-1])
    full_path = os.path.join(root,rel_dir)
    sys.path.append(full_path)
    file_name = rel_path.split(join_str)[-1]
    return importlib.import_module(file_name.split('.')[0])
    
# Calls a function in a module using a string
def callFunction(foo, mod):
    method = getattr(mod,foo)
    return method()

# Grade a students homework
def gradeHomework(file_path,functions):
    mod_load_msg = '''
---------------------------------------------
Loading module and calling supplied functions
---------------------------------------------
----Output----
'''
    file_load_msg = '''
--------------
File contents:
--------------
'''
    file_dir = getJoinStr().join(file_path.split(getJoinStr())[:-1])
    if 'grade.csv' not in os.listdir(file_dir):

        # Load student homework module and try to run the 
        # functions that were supplied by the grader.
        file_name = file_path.split(getJoinStr())[-1]

        print(mod_load_msg)
        mod_load_error = False
        try:
            stud_mod = importScript(file_path)
        except:
            mod_load_error = True
            print('Failed to load module',file_path)
            print('Error info:')
            for err in sys.exc_info():
                print(err)

        if not mod_load_error:
            for fn in functions:
                print('\nTrying to call',fn+'(): ')
                print('----Output----')
                try:
                    callFunction(fn,stud_mod)
                except:
                    print('Failed to call',fn+'()')
                    print('Error info:')
                    for err in sys.exc_info():
                        print(err)
                print('--------------\n')

        # Display the contents of the student's homework file
        # for manual inspection and partial credit. Displays 
        # with line numbers for easy reference.
        print(file_load_msg)

        fin = open(file_path,'r')
        contents = fin.readlines()
        fin.close()

        for i in range(len(contents)):
            print(str(i+1).rjust(4,'_'),': ', contents[i], end='')
        print('\n\nFile: ',file_path,'\n')

        # Offer to drop into a python shell in the student directory
        drop_in = str(input("Would you like to enter a python shell? "))
        if drop_in.lower() == 'y':
            current_dir = os.getcwd()
            os.chdir(file_dir)
            subprocess.call(['python3','-i',file_name])
            os.chdir(current_dir)

        # Offer to edit student submission for testing
        edit_file = str(input("Would you like to edit the file? "))
        if edit_file.lower() == 'y':
            editor = str(input("What program to use? "))
            current_dir = os.getcwd()
            os.chdir(file_dir)
            subprocess.call([editor,file_name])
            os.chdir(current_dir)

        # Get student name, grade, and comments from the grader,
        # and write to file.
        print('\n----------------------------------')
        name = str(input('Enter student name: '))
        grade = str(input('Enter grade: '))
        comments = str(input('Enter comments: ')).replace(',',';')
        print('----------------------------------')

        print('Writing to file...',end='')
        fout = open(file_dir+'/grade.csv','w')
        fout.write(name+','+grade+','+comments)
        fout.close()
        print('Done')
        return True

    else:
        print('\nSkipping',file_path, 'because "grade.csv" already exists.\n')
        return False

def consolidateGrades(file_name):
    print('Consolidating grades into',file_name)
    if file_name not in os.listdir(os.getcwd()):
        fout = open(file_name,'a')
        fout.write('Student,Grade,Comments\n')

        # Get all student records that have been generated
        files = find('grade.csv','.')

        # Combine into a single file
        for f in files:
            fin = open(f,'r')
            record = fin.read()
            fin.close()

            fout.write(record+'\n')
            print('.',end='')

        fout.close()
        print('\nFinished. See \''+file_name+'\' for output.\n')

        # Offer to delete individual grade.csv files
        ans = str(input('Would you like to clean up individual grading files? '))
        if ans.lower() == 'y':
            print('Deleting files.',end='')
            for f in files:
                os.remove(f)
                print('.',end='')
            print('Done')
        return True
    else:
        print('Error, the file',file_name,'already exists.\n')
        return False

print("""
**********************************************************************
*                                                                    *
*  Welcome to the CSCI 1133 Superduperawesomepossum Grading Program  *
*                                                                    *
**********************************************************************
""")
print("Please enter one or more UNIX file name patterns to identify the scripts which need grading. Separate patters with a comma.")
patterns = str(input("> ")).replace(' ','').split(',')

print("Please enter the names of all the functions you would like\nto try calling within the scripts, using commas to separate the names.")
function_list = str(input("> ")).replace(' ','').split(',')

student_files = []
for pattern in patterns:
    files = find(pattern,'.')
    for f in files:
        if f not in student_files:
            student_files.append(f)

for f in student_files:
    not_skipped = gradeHomework(f,function_list)
    if not_skipped:
        if student_files.index(f) != len(student_files)-1:
            cont = str(input("Grade another? "))
            if cont.lower() != 'y':
                break
        else:
            print("No more homework to grade.\n")

cons = str(input("Would you like to consolidate all grade files now? "))
if cons.lower() == 'y':
    valid_file = False
    while not valid_file:
        f_name = str(input("Save as: "))
        valid_file = consolidateGrades(f_name)

print("Grading session complete.")
