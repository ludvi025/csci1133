#!/usr/bin/env python

# Call unzip.py script before running this
# to recursively unzip all folders.

import argparse, os, csv

submission_directory_format = "HW0"
submission_files = ["{x500}_0A.py", "{x500}_0B.py"]

def main():
    # Command line options
    args = parseArgs() 
    # Read csv file with student info into a python dictionary
    user_data = getDictsFromCSV(args.student_info_file)
    # Add a "submission" field to user_data and return a dictionary with who submitted and who didn't
    subStatus = getSubmissionStatus(user_data,args.submissions_dir)
    # Determine invalid submissions and the reason why
    invalidSubmissions = getInvalidSubmissions(user_data, \
            subStatus["has_sub"], \
            submission_directory_format, \
            submission_files, \
            args.submissions_dir)
    # Create a dictionary with all the students in an array whose key is their submission status
    #result = merge(invalidSubmissions, subStatus)
    result = merge(invalidSubmissions, {"no_sub":subStatus["no_sub"]})
    # Write to file
    writeToFile(result, args.output)

def writeToFile(Dict, filename):
# Write a big list
    if filename == None:
        filename = "output.txt"

    fout = open(filename, "w")
    for key in Dict:
       fout.write("---\n"+key+"\n---\n")
       for item in Dict[key]:
           fout.write(item+"@umn.edu"+",\n")
    fout.close()

def getInvalidSubmissions(user_data, submissions, sub_dir_format, sub_files, sub_dir):
    # Classifications
    bad_dir = []
    missing_file = []
    extra_files = []
    nested_folder = []

    for moodle_sub in submissions:
        sub_path = getJoinStr().join([sub_dir,user_data[moodle_sub]["submission"]])
        sub_directory = getSubName(user_data[moodle_sub]["submission"])
        # sd = os.listdir(d)[0] 

        # Did they submit a zip file? If so, this should be a directory
        if not os.path.isdir(sub_path):
            bad_dir.append(moodle_sub)
        elif sub_directory.lower() != (sub_dir_format.format(**user_data[moodle_sub])).lower():
            bad_dir.append(moodle_sub)
        else: 
            # sub_dir_contents = getJoinStr().join([sub_directory])
            file_list = os.listdir(sub_path)
        
            hasAllFiles = True
            nested = False
            extra = False
            if len(file_list) > len(sub_files):
                extra = True
            for f in sub_files:
                if f.format(**user_data[moodle_sub]) not in file_list:
                    hasAllFiles = False
            for f in file_list:
                if f.lower() in sub_directory.lower():
                    nested = True

            if not hasAllFiles and nested:
                nested_folder.append(moodle_sub)
            elif not hasAllFiles:
                missing_file.append(moodle_sub)
            if hasAllFiles and extra:
                extra_files.append(moodle_sub)
				
    return {"missing_file": missing_file, \
            "extra_files" : extra_files, \
            "bad_directory": bad_dir, \
            "nested_folder": nested_folder}

def getSubName(moodle_name):
    # Remove what moodle adds
    end_string = 'assignsubmission_file_'
    end_of_moodle = moodle_name.index(end_string)+len(end_string)
    #print(moodle_name[end_of_moodle:])
    return moodle_name[end_of_moodle:]

def merge(d1, d2):
# Combine two dicts
    return dict(d1.items()+d2.items())

def getJoinStr():
# Get the OS specific path string
    return os.path.join('.','.')[1:-1]
    
def getSubmissionStatus(sub_data, sub_dir):
# Pair student info with submissions and add a "submission" key
    subs = os.listdir(sub_dir)
    data = [sub_data[item] for item in sub_data]
    noSub = [datum["x500"] for datum in sub_data.values()]
    hasSub = []
    for sub in subs:
        for datum in data:
            if datum["pid"] in sub.lower():
                datum["submission"] = sub
                noSub.remove(datum["x500"])
                hasSub.append(datum["x500"])
                data.remove(datum)
            else:
                datum["submission"] = "no_submission"
    return {"no_sub": noSub, "has_sub": hasSub}

def addx500(datum):
    pid = getPid(datum)
    datum["pid"] = pid 
    x500 = getx500(datum)
    datum["x500"] = x500
    return x500

def getPid(datum):
    return datum["Identifier"].split(" ")[1]

def getx500(datum):
    return datum["Email address"].split("@")[0]

def getDictsFromCSV(filename):
    data_file = csv.DictReader(open(filename))
    return {addx500(entry): entry for entry in data_file}

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("student_info_file")
    parser.add_argument("submissions_dir")
    parser.add_argument("-o","--output")
    return parser.parse_args()

main()
