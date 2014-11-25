#!/usr/bin/python3
import os, imp, importlib, sys, subprocess, json, csv, signal

import lib.rfind as rfind, lib.sub_parser as sub_parser, lib.art as art, lib.get_input as get_input, lib.version as version
import lib.stdin_pipe.run_with_input as run_with_input
import lib.menu.main_menu as menu_main, lib.menu.grade_homeworks as menu_grade, lib.menu.check_grade_files as menu_cleanup
import lib.grade_files.cleanup as grade_file_cleanup

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

    # Get the list of student files to grade
    student_files = []
    for pattern in patterns:
        files = rfind.find(pattern,'.',IGNORE)
        for f in files:
            if f not in student_files:
                student_files.append(f)

    # Main menu
    menu_main.print_menu()
    opt = menu_main.get_option()
    while opt != menu_main.options.TerminateProgram:

        if opt == menu_main.options.GradeHomeworks:
            gradeHomeworks(grade_file_name, student_files, tests, maxpoints)
            menu_main.print_menu()

        elif opt == menu_main.options.CheckGradeFiles:
            checkGradeFiles(grade_file_name)
            menu_main.print_menu()

        elif opt == menu_main.options.GradingStatistics:
            #printStatistics()
            print("Not yet implemented")

        elif opt == menu_main.options.ConsolidateGrades:
            #consolidateGradeFiles()
            print("Not yet implemented")

        else:
            print("You somehow got an impossible option:", opt)

        opt = menu_main.get_option()

    print("Grading session complete.")


def checkGradeFiles(grade_file_name):
    menu_cleanup.print_menu()
    opt = menu_cleanup.get_option()

    while opt != menu_cleanup.options.GoToMain:

        if opt == menu_cleanup.options.UnfinishedOnly:
            grade_file_cleanup.RemoveUnfinished(grade_file_name)

        elif opt == menu_cleanup.options.InProgressOnly:
            grade_file_cleanup.RemoveInProgress(grade_file_name)

        else:
            print("You somehow got an impossible option.")

        opt = menu_cleanup.get_option()


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


def gradeHomeworks(grade_file_name, student_files, tests, maxpoints):
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
                    gradeHomework(file,tests,maxpoints,grade_file_name)
                else:
                    break
            else:
                print("No more homework to grade.\n")
        else:
            print('Skipping',file, 'because "'+grade_file_name+'" already exists.')


# Grade a students homework
def gradeHomework(file_path,tests,maxpoints,grade_file_name='grade.csv'):
    file_load_msg = '''
--------------
File contents:
--------------
'''
    file_dir = getJoinStr().join(file_path.split(getJoinStr())[:-1])
    file_list = os.listdir(file_dir)

    # --- writeFlag() ---
    fn = file_dir+'/'+grade_file_name

    # Check if grade file exists (will happen when the grader dawdles too long
    # on the Grade another? prompt)
    if os.path.isfile(fn):
        print("Looks like you dawdled too long on wanting to grade another.")
        return

    fout = open(fn,'w')
    fout.write('Grading in progress for: ' + file_path)
    fout.close()
    # ---

    # Register a signal handler to wrap around the grading for the in progress
    # race condition
    original_sigint = signal.getsignal(signal.SIGINT)
    def handler(signum, frame):
        with open(fn,'w') as fout:
            fout.write('Grading unfinished for: ' + file_path)
        print("\n\033[91mLooks like you pushed Ctrl-C.\033[0m\nGrading file {} marked as unfinished, and terminating grading script.".format(fn))
        sys.exit()
    signal.signal(signal.SIGINT, handler)

    # Load student homework module and try to run the 
    # functions that were supplied by the grader.
    file_name = file_path.split(getJoinStr())[-1]

    ## -- Menu Option #1 and #2 -- ##
    ## #1 - Run supplied tests (checks to see if any)
    ## #2 - Enter interactive shell

    # We can pipe the lines of a script to a subprocess
    # running their script.
    sending_input = False
    if sending_input:
        pass
    else:
        runTests(tests, file_path)
    ## -- End #1 and #2 -- ##

    ## -- Menu Option #3 -- ##

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
    print('\nFile: ',file_path)
    ## -- End #3 -- ##

    ## -- Menu Option #4 -- ##
    ## Enter Grade ##

    # Attempt to get student info from file path
    stud_info = getStudentInfo(file_path)
        
    printStudentInfo(stud_info)
            
    print('\n----------------------------------')
    grade = get_input.grade(maxpoints)
    comments = str(input('Enter comments: ')).strip('\\')
    print('----------------------------------')

    print('Writing to file...',end='')
    fn = file_dir+'/'+grade_file_name
    with open(fn, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([stud_info['moodleid'], stud_info['firstname'],
                            stud_info['lastname'], grade, comments, os.getlogin()])
    signal.signal(signal.SIGINT, original_sigint)
    print('Done')
    ## -- End #4 -- ##
    
def printStudentInfo(info):
     print('\nStudent info\n------------')
     print(info)
     print('First name: ', info['firstname'])
     print('Last name : ', info['lastname'])
     print('Moodle id : ', info['moodleid'])
     print('------------')

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
            if out:
                out = out.replace('>>>','\n').replace('...','\n')
            if err:
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
    # Store the original handler and set a new one
    original_sigint = signal.getsignal(signal.SIGINT)
    def handler(signum, frame):
        print("\n\033[91mLooks like you pushed Ctrl-C. Handler removed.\033[0m")
        signal.signal(signal.SIGINT, original_sigint)
    signal.signal(signal.SIGINT, handler)
    # Call the student code
    subprocess.call([sys.executable,'-i',file_name])
    # Restore the handler
    signal.signal(signal.SIGINT, original_sigint)
    os.chdir(current_dir)


if __name__ == "__main__":
    main()
