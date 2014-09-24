#!/usr/bin/python3
import os, imp, importlib, sys, subprocess, json
import lib.rfind as rfind, lib.sub_parser as sub_parser

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
    # Remember sessions
    session_name = input("Enter session name: ")
    session = getSession(session_name) 
    if not session:
        print("Enter one or more UNIX file name patterns\nto identify the scripts which need grading.\nSeparate patterns with a comma.")
        patterns = str(input("> ")).replace(' ','').split(',')

        print("Enter paths to all testing scripts you would\nlike to run against the homework,\nseparated by commas.")
        tests = str(input("> ")).replace(' ','').split(',')

        writeSession(session_name, patterns, tests)
    else:
        patterns = session['patterns']
        tests = session['tests']

    # Allow for multiple grading sessions at once
    if session_name:
        grade_file_name = session_name + '_grade.csv'
    else:
        grade_file_name = 'grade.csv'

    student_files = []
    for pattern in patterns:
        files = rfind.find(pattern,'.',IGNORE)
        for f in files:
            if f not in student_files:
                student_files.append(f)

    # For each homework file, grade it
    last_file = len(student_files)-1
    for file in student_files:
        not_skipped = gradeHomework(file,tests,grade_file_name)
        if not_skipped:
            idx = student_files.index(file) 
            remaining = last_file - idx
            if idx != last_file:
                cont = str(input(str(remaining) + " files remaining... Grade another? "))
                if cont.lower() != 'y':
                    break
            else:
                print("No more homework to grade.\n")

    #consolidate = str(input("Would you like to consolidate all grade files now? "))
    #if consolidate.lower() == 'y':
    #    valid_file = False
    #    while not valid_file:
    #        f_name = str(input("Save as: "))
    #        valid_file = consolidateGrades(f_name, grade_file_name)

    print("Grading session complete.")

def getSession(name):
    file_name = name+'.session'
    if os.path.isfile(file_name):
        fin = open(file_name)
        patterns = json.loads(fin.readline())
        tests = json.loads(fin.readline())
        fin.close()
        return {"patterns": patterns, "tests": tests}
    else:
        return False

def writeSession(name, patterns, tests):
    fout = open(name+'.session', 'w')
    fout.write(json.dumps(patterns)+'\n')
    fout.write(json.dumps(tests)+'\n')
    fout.close()

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
    mod_name = file_name.replace('.py','')
    if mod_name in sys.modules:
        del sys.modules[mod_name]
    return importlib.import_module(file_name.split('.')[0])
    
# Calls a function in a module using a string
def callFunction(foo, mod):
    method = getattr(mod,foo)
    return method()

def callTest(test_path, student_module):
    test = open(test_path).read()
    exec(test)

# Grade a students homework
def gradeHomework(file_path,tests,grade_file_name='grade.csv'):
    file_load_msg = '''
--------------
File contents:
--------------
'''
    file_dir = getJoinStr().join(file_path.split(getJoinStr())[:-1])
    if grade_file_name not in os.listdir(file_dir):
        fout = open(file_dir+'/'+grade_file_name,'w')

        # Load student homework module and try to run the 
        # functions that were supplied by the grader.
        file_name = file_path.split(getJoinStr())[-1]

        # We can pipe the lines of a script to a subprocess
        # running their script.
        sending_input = False
        if sending_input:
            pass
        else:
            runTests(tests, file_path)

        # Display the contents of the student's homework file
        # for manual inspection and partial credit. Displays 
        # with line numbers for easy reference.
        print(file_load_msg)

        fin = open(file_path,'r')
        contents = fin.readlines()
        fin.close()

        for i in range(len(contents)):
            print(str(i+1).rjust(4,'_'),': ', contents[i], end='')
        print('\n')

        edit_file = 'y'
        while edit_file.lower() == 'y':
            # Offer to drop into a python shell in the student directory
            drop_in = str(input("Enter a python shell (y/n) ? "))
            if drop_in.lower() == 'y':
                current_dir = os.getcwd()
                os.chdir(file_dir)
                subprocess.call(['python3','-i',file_name])
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

                run_tests_again = input("Run tests again? ")
                if run_tests_again:
                    runTests(tests, file_path)

        print('\nFile: ',file_path)

        # Attempt to get student info from file path
        stud_info = getStudentInfo(file_path)
        
        print('\nStudent info\n------------')
        print('First name: ', stud_info['firstname'])
        print('Last name : ', stud_info['lastname'])
        print('Moodle id : ', stud_info['moodleid'])
        print('------------')
        change_info = input('Change? ')

        if change_info.lower() == 'y':
            print('\n----------------------------------')
            stud_info['firstname'] = input('Enter first name: ')
            stud_info['lastname'] = input('Enter last name: ')
            stud_info['moodleid'] = input('Enter moodle id: ')
            print('----------------------------------')
            
        print('\n----------------------------------')
        grade = str(input('Enter grade: '))
        comments = str(input('Enter comments: ')).replace(',',';')
        print('----------------------------------')

        print('Writing to file...',end='')
        #fout = open(file_dir+'/'+grade_file_name,'w')
        fout.write(stud_info['moodleid']+','+
                stud_info['firstname']+','+
                stud_info['lastname']+','+
                grade+','+comments)
        fout.close()
        print('Done')
        return True

    else:
        print('\nSkipping',file_path, 'because "'+grade_file_name+'" already exists.\n')
        return False

def getStudentInfo(file_path):
    return sub_parser.parse(file_path)

def runTests(tests, file_path):
    mod_load_msg = '''
-----------------------------------------
Loading module and calling supplied tests
-----------------------------------------
----Module Load Output----
'''
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
            print('----Test Output----')
            try:
                callTest(test,stud_mod)
            except:
                print('Failed to call',test)
                print('Error info:')
                for err in sys.exc_info():
                    print(err)
            print('-------------------\n')

def consolidateGrades(file_name, grade_file_name):
    print('Consolidating grades into',file_name)
    if file_name not in os.listdir(os.getcwd()):
        fout = open(file_name,'a')
        fout.write('Moodle id,First name,Last name,Grade,Comments\n')

        # Get all student records that have been generated
        files = rfind.find(grade_file_name,'.')

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

if __name__ == "__main__":
    main()
