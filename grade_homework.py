#!/usr/bin/python3
import os, imp, importlib, sys, subprocess, json, csv, stat

import lib.rfind as rfind, lib.sub_parser as sub_parser, lib.art as art, lib.stdin_pipe.run_with_input as run_with_input, lib.get_input as get_input, lib.version as version

# TODO :
# Add comment about how python subprocess gets module

IGNORE = "__MACOSX"

def main():

    # Change umask to allow group read/write files
    os.umask(0o007)
    
    # Print welcome art and version
    print(art.art)
    print("Version: {}\n".format(version.get_version()).rjust(55))

    # Remember sessions
    session_name = input("Enter session name: ")
    session = getSession(session_name) 
    if not session:
        print("Enter one or more UNIX file name patterns\nto identify the scripts which need grading.\nSeparate patterns with a comma.")
        patterns = str(input("> ")).replace(' ','').split(',')

        print("Enter paths to all testing scripts you would\nlike to run against the homework,\nseparated by commas.")
        tests = str(input("> "))
        tests = tests.replace(' ','').split(',') if tests != '' else None

        print("Enter the maximum point value for the assignment to verify that students are not given extra credit.")
        maxpoints = input("> ")
        maxpoints = float(maxpoints) if maxpoints != '' else -1

        writeSession(session_name, patterns, tests, maxpoints)
    else:
        patterns = session['patterns']
        tests = session['tests']
        maxpoints = session['maxpoints']

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
    last_file = len(student_files)
    for file in student_files:
        file_dir = getJoinStr().join(file.split(getJoinStr())[:-1])
        file_list = os.listdir(file_dir)
        if grade_file_name not in file_list:
            idx = student_files.index(file) 
            remaining = last_file - idx
            if idx != last_file:
                cont = get_input.yes_or_no(str(remaining) + " files remaining... Grade another?")
                if cont:
                    break
                else:
                    gradeHomework(file,tests,maxpoints,grade_file_name)
            else:
                print("No more homework to grade.\n")
        else:
            print('Skipping',file, 'because "'+grade_file_name+'" already exists.')

    incomplete_check = get_input.yes_or_no("Check for incomplete grade files?")
    if incomplete_check:
        files_found = cleanupIncompletes(grade_file_name)
        if len(files_found) > 0:
            print("Found and removed the following unfinished files:")
            for fn in files_found:
                print(fn)
            print("Rerun the grading script to grade these again before consolidating.")

    print("Grading session complete.")

def getSession(name):
    file_name = name+'.session'
    if os.path.isfile(file_name):
        fin = open(file_name)
        patterns = json.loads(fin.readline())
        tests = json.loads(fin.readline())
        maxpoints = float(json.loads(fin.readline()))
        fin.close()
        return {"patterns": patterns, "tests": tests, "maxpoints": maxpoints}
    else:
        return False

def writeSession(name, patterns, tests, maxpoints):
    fn = name+'.session'
    fout = open(fn, 'w')
    fout.write(json.dumps(patterns)+'\n')
    fout.write(json.dumps(tests)+'\n')
    fout.write(json.dumps(maxpoints)+'\n')
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

    need_reload = False
    if mod_name in sys.modules:
        need_reload = True
        del sys.modules[mod_name]

    return importlib.import_module(file_name.split('.')[0])

# HERE
    # if need_reload:
    #     importlib.reload(mod)
    # else:
    #     mod = importlib.import_module(file_name.split('.')[0])

    # return mod
# TO HERE

# Calls a function in a module using a string
def callFunction(foo, mod):
    method = getattr(mod,foo)
    return method()

def callTest(test_path, student_module):
    test = open(test_path).read()
    exec(test)

# Grade a students homework
def gradeHomework(file_path,tests,maxpoints,grade_file_name='grade.csv'):
    file_load_msg = '''
--------------
File contents:
--------------
'''
    file_dir = getJoinStr().join(file_path.split(getJoinStr())[:-1])
    file_list = os.listdir(file_dir)

    fn = file_dir+'/'+grade_file_name
    fout = open(fn,'w')
    fout.write('Grading unfinished for: ' + file_path)
    fout.close()

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

#    edit_file = 'y'
#    while edit_file.lower() == 'y':
#        # Offer to drop into a python shell in the student directory
#        drop_in = str(input("Enter a python shell (y/n) ? "))
#        if drop_in.lower() == 'y':
#            current_dir = os.getcwd()
#            os.chdir(file_dir)
#            subprocess.call(['python3','-i',file_name])
#            os.chdir(current_dir)
#
#        # Offer to edit student submission for testing
#        edit_file = str(input("Edit the file (y/n) ? "))
#        if edit_file.lower() == 'y':
#            current_dir = os.getcwd()
#            os.chdir(file_dir)
#
#            # TODO: Bad editor sends back to 'use python?' prompt.
#            valid_editor = False
#            while not valid_editor:
#                editor = str(input("Which editor to use? "))
#                try:
#                    subprocess.call([editor,file_name])
#                    valid_editor = True
#                except:
#                    try_again = input("Error calling editor. Try again? ")
#                    if try_again.lower != 'y':
#                        valid_editor = True
#
#            os.chdir(current_dir)
#
#            run_tests_again = input("Run tests again? ")
#            if run_tests_again:
#                runTests(tests, file_path)

    print('\nFile: ',file_path)

    # Attempt to get student info from file path
    stud_info = getStudentInfo(file_path)
        
    print('\nStudent info\n------------')
    print('First name: ', stud_info['firstname'])
    print('Last name : ', stud_info['lastname'])
    print('Moodle id : ', stud_info['moodleid'])
    print('------------')
    change_info = get_input.yes_or_no('Change?')

    if change_info:
        print('\n----------------------------------')
        stud_info['firstname'] = input('Enter first name: ')
        stud_info['lastname'] = input('Enter last name: ')
        stud_info['moodleid'] = input('Enter moodle id: ')
        print('----------------------------------')
            
    print('\n----------------------------------')
    grade = get_input.grade(maxpoints)
    comments = str(input('Enter comments: '))
    print('----------------------------------')

    print('Writing to file...',end='')
    fn = file_dir+'/'+grade_file_name
    with open(fn, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([stud_info['moodleid'], stud_info['firstname'],
                            stud_info['lastname'], grade, comments, os.getlogin()])

    print('Done')

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
    if tests:
        for test in tests:
            out, err = run_with_input.runInteractive(file_path, open(test).read())
            out = out.replace('>>>','\n').replace('...','\n')
            err = err.replace('>>>','\n').replace('...','\n')
            print('Output from', test, '\n------')
            print(out)
            if not err.replace('\n','').replace(' ','')=='':
                print('Errors from', test, '\n------')
                print(err)
            print()

        play_again = get_input.yes_or_no('Load interactive python shell?')

    else:
        play_again = True

    if play_again:
        print('\n-----')
        print('Loading student module in separate instance of python.')
        print('Press Ctrl+D to return to grading script when finished.')
        print('Hint: If the student does not call their function, type')
        print('run the function dir() at the python prompt to see what')
        print('it\'s called.')
        print('-----\n')

    while play_again: 
        loadShell(file_path)
        play_again = get_input.yes_or_no('Reload module?')

def loadShell(file_path):
    current_dir = os.getcwd()
    file_dir = getJoinStr().join(file_path.split(getJoinStr())[:-1])
    file_name = file_path.split(getJoinStr())[-1]
    print(file_dir, file_name)
    os.chdir(file_dir)
    subprocess.call([sys.executable,'-i',file_name])
    os.chdir(current_dir)

def cleanupIncompletes(grade_file_name):
    files = rfind.find(grade_file_name, '.')
    found_files = []
    for fn in files:
        with open(fn, 'r') as f:
            if "Grading unfinished for" in f.read():
                found_files.append(fn)
                f.close()
                os.remove(fn)
    return found_files

def ctrlc_handler(signal, frame):
     print('You forced the grading script to quit...\nCleaning up and deleting any temporary grade files.')


if __name__ == "__main__":
    main()
