import os
import os

files = [(x, os.listdir(x) for x in os.listdir() if os.path.isdir(x)]

hw_files = []
empty_files = []

for d in files:
	for f in d[1]:
		if f[-3:] == '.py':
			hw_files.append(d[0]+'/'+f)

for f in hw_files:
	s = open(f).read().strip().replace('\n','')
	if s == '':
		empty_files.append(f)

for f in empty_files:
	print(f)