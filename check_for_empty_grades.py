import os
import lib.rfind as rfind

def main():
	files = rfind.find('*.py', '.')

	hw_files = []
	empty_files = []

	for f in files:
		print(f)
		if f[-3:] == '.py':
			hw_files.append(f)

	for f in hw_files:
		print(f)
		s = open(f).read().strip().replace('\n','')
		if s == '':
			empty_files.append(f)

	print('Printing empty files:')
	print('---------------------')
	for f in empty_files:
		print(f)
	print('---------------------')

if __name__ == '__main__':
	main()