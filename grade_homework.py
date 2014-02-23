#!/usr/bin/python3
import os, importlib, sys, fnmatch, subprocess

# TODO :
# Add comment about how python subprocess gets module
# Change format of CSV

IGNORE = "__MACOSX"

def main():

    print("""
               _____               _                  
              / ____|             | |                 
             | |  __ _ __ __ _  __| | ___             
             | | |_ | '__/ _` |/ _` |/ _ \            
  _    _     | |__| | | | (_| | (_| |  __/       _    
 | |  | |     \_____|_|  \__,_|\__,_|\___|      | |   
 | |__| | ___  _ __ ___   _____      _____  _ __| | __
 |  __  |/ _ \| '_ ` _ \ / _ \ \ /\ / / _ \| '__| |/ /
 | |  | | (_) | | | | | |  __/\ V  V / (_) | |  |   < 
 |_|  |_|\___/|_| |_| |_|\___| \_/\_/ \___/|_|  |_|\_\
                                                      
""")
    print("Please enter one or more UNIX file name patterns\nto identify the scripts which need grading.\nSeparate patterns with a comma.")
    patterns = str(input("> ")).replace(' ','').split(',')

    print("Please enter paths to all testing scripts you would\nlike to run against the homework,\nseparated by commas.")
    tests = str(input("> ")).replace(' ','').split(',')

    student_files = []
    for pattern in patterns:
        files = find(pattern,'.',IGNORE)
        for f in files:
            if f not in student_files:
                student_files.append(f)

    # For each homework file, grade it
    for file in student_files:
        not_skipped = gradeHomework(file,tests)
        if not_skipped:
            if student_files.index(file) != len(student_files)-1:
                cont = str(input("Grade another? "))
                if cont.lower() != 'y':
                    break
            else:
                print("No more homework to grade.\n")

    consolidate = str(input("Would you like to consolidate all grade files now? "))
    if consolidate.lower() == 'y':
        valid_file = False
        while not valid_file:
            f_name = str(input("Save as: "))
            valid_file = consolidateGrades(f_name)

    print("Grading session complete.")

# Walks the directory and returns a list of full path names, 
# like the unix 'find' command
def find(pattern, directory, ignore=""):
    matches = []
    for root, dirs, files in os.walk(directory):
        for f in files:
            if fnmatch.fnmatch(f,pattern):
                path = os.path.join(root,f)
                if ignore:
                    if not ignore in path:
                        matches.append(path)
                else:
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

def callTest(test_path, student_module):
    test = open(test_path).read()
    exec(test)

# Grade a students homework
def gradeHomework(file_path,tests):
    mod_load_msg = '''
-----------------------------------------
Loading module and calling supplied tests
-----------------------------------------
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

        # We can pipe the lines of a script to a subprocess
        # running their script.
        if sending_input:
            pass
        else:
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
                for test in tests:
                    print('\nRunning test:',test,': ')
                    print('----Output----')
                    try:
                        callTest(test,stud_mod)
                    except:
                        print('Failed to call',test)
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

        edit_file = 'y'
        while edit_file.lower() == 'y':
            # Offer to drop into a python shell in the student directory
            drop_in = str(input("Enter a python shell (y/n) ? "))
            if drop_in.lower() == 'y':
                current_dir = os.getcwd()
                os.chdir(file_dir)
                subprocess.call(['python3','-i',file_name])
                # TODO: Automatically load in student module
                os.chdir(current_dir)

            # Offer to edit student submission for testing
            edit_file = str(input("Edit the file (y/n) ? "))
            if edit_file.lower() == 'y':
                current_dir = os.getcwd()
                os.chdir(file_dir)

                # TODO: Bad editor sends back to 'use python?' prompt.
                valid_editor = False
                while not valid_editor:
                    editor = str(input("Which editor to use? "))
                    try:
                        subprocess.call([editor,file_name])
                        valid_editor = True
                    except:
                        try_again = input("Error calling editor. Try again? ")
                        if try_again.lower != 'y':
                            valid_editor = True


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

main()
