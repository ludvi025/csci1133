import os

def main():
	args = parseArgs()

	if args.output not in os.listdir():

	    if args.session:
	        grade_file_name = args.session + '_grade.csv'
	    else:
	        grade_file_name = 'grade.csv'

	    consolidateGrades(args.output, grade_file_name)

	else:
		print('Invalid output file specified, already exists.')


def consolidateGrades(file_name, grade_file_name):
    print('Consolidating grades into',file_name)
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

def parseArgs():
	parser = argparse.ArgumentParser()
	parser.add_argument('output')
	parser.add_argument('-s', '--session')
	return parser.parse_args()

if __name__ == '__main__':
	main()