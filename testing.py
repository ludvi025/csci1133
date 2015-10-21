from lib.syntaxhi import color_line
import os
def printCode(file_path):
    # Display the contents of the student's homework file
    # for manual inspection and partial credit. Displays 
    # with line numbers for easy reference.

    file_load_msg = '''
    --------------
    File contents:
    --------------
    '''
    # Check to see if we're running linux (syntax highlighting only supports Linux terminals)
    linux = (os.name == "posix")
        
    print(file_load_msg)

    fin = open(file_path,'r')
    contents = fin.readlines()
    fin.close()
    
    # Print out the code line-by-line
    for i in range(len(contents)):
        if linux:
            print(str(i+1).rjust(4,'_'),': ', color_line(contents[i]), end = '')
        else:
            print(str(i+1).rjust(4,'_'),': ', contents[i], end = '')
        
    print('\n')
    print('\nFile: ',file_path)

if __name__ == "__main__":
    printCode("grade_homework.py")
