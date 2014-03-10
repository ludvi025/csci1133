#!/usr/bin/env python

import argparse, os, csv

def main():
    args = parseArgs()
    #unique_keys = ['Moodle id', 'First name', 'Last name']
    unique_keys = ['First name', 'Last name']

    grade_files = parseFiles(args.inputs)
    
    problem_keys = getProblemKeys(grade_files.keys())
    problem_keys.sort()

    key_order = unique_keys + problem_keys

    if args.key not in unique_keys:
      print('Invalid key: ' + str(args.key))
      return

    grades = mergeGrades(grade_files, args.key, unique_keys)

    writeGradesToFile(grades.values(), key_order, args.output)

def writeGradesToFile(entries, order, filename):
    print(order)
    fout = open(filename, 'w')

    fout.write(order[0])
    for column in order[1:]:
        fout.write(','+column)
    fout.write('\n')

    writer = csv.DictWriter(fout, order)
    for e in entries:
        writer.writerow(e)

def mergeGrades(grade_files, key, unique_keys):
    grades = {}

    for name, contents in grade_files.items():
      for student_problem in contents:
          if student_problem[key] in grades:
              grade_info = grades[student_problem[key]]
              grade_info[name+' grade'] = student_problem['Grade']
              grade_info[name+' comments'] = student_problem['Comments']
          else:
              grade_info = {}
              for key in unique_keys:
                  grade_info[key] = student_problem[key]
              grade_info[name+' grade'] = student_problem['Grade']
              grade_info[name+' comments'] = student_problem['Comments']

              grades[student_problem[key]] = grade_info
    return grades

def getProblemKeys(problems):
    keys = []
    for p in problems:
        keys.append(p+' grade')
        keys.append(p+' comments')
    return keys

def getDictFromCSV(source_filename):
  return csv.DictReader(open(source_filename))

def getProblemLabel(filename):
    return filename.split('.')[0]

def parseFiles(filenames):
  source_files = {}
  for src_file in filenames:
    source_files[getProblemLabel(src_file)] = getDictFromCSV(src_file)
  return source_files

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('inputs', nargs='+')
  parser.add_argument('-k', '--key')
  parser.add_argument('-o', '--output')
  args = parser.parse_args()
  if args.key == None:
      args.key = 'Moodle id'
  return args

main()
