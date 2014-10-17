import os, argparse, csv
import lib.rfind as rfind

def main():
    args = parseArgs()

    if args.output not in os.listdir():

        if args.session:
            grade_file_name = args.session + '_grade.csv'
        else:
            grade_file_name = 'grade.csv'

        if args.student_info_file:
            user_ids = getUserIds(args.student_info_file)
            consolidateGrades(args.output, grade_file_name, user_ids)
        else:
            consolidateGrades(args.output, grade_file_name)

    else:
        print('Invalid output file specified, already exists.')


def consolidateGrades(file_name, grade_file_name, user_ids=None):
    print('Consolidating grades into',file_name)
    fout = open(file_name,'a', newline='')
    cout = csv.writer(fout)
    cout.writerow(['User id','Moodle id','First name','Last name','Grade','Comments','Grader ID'])

    # Get all student records that have been generated
    files = rfind.find(grade_file_name,'.')

    # Combine into a single file
    for f in files:
        with open(f, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for record in reader:
                if user_ids != None:
                    key = getNameKey(record[1], record[2])
                    if key in user_ids:
                        uid = user_ids[key]
                    else:
                        uid = "#######"
                    record = [uid] + record

                cout.writerow(record)
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

def getNameKey(first, last):
    key = (last+first)
    for c in ' \'\"':
        key = key.replace(c, '')
    key = key.lower()
    return key

def getUserIds(filename):
    # Open the file
    if not os.path.isfile(filename):
        exit(filename + " does not exist.")
    file = open(filename, newline='')

    # Get the first row and check for headers and section nums
    reader = csv.reader(file)
    firstline = next(reader)
    explen = 3
    length = len(firstline)
    if length != explen:
        errorstr =  "Incorrect number of columns in " + filename + ':\n'
        errorstr += "    Expected {}, but got {}.".format(explen, length)
        exit(errorstr)
    if firstline == ['ID number','First name','Last name']:
        print("Header row detected in csv file. Skipping first line.")
        firstline = next(reader)
    else:
        print("Header row not detected in csv file. Using first row as data:")
        print("    " + str(firstline))

    # Accumulate the students    
    students = {getNameKey(firstline[1], firstline[2]): firstline[0]}
    for row in reader:
        students[getNameKey(row[1], row[2])] = row[0]
    print("   Found {} students.".format(len(students)))

    #Cleanup and return
    file.close()
    return students

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('output')
    parser.add_argument('-s', '--session')
    parser.add_argument('-u', '--student_info_file', help=
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
    return parser.parse_args()

if __name__ == '__main__':
    main()
