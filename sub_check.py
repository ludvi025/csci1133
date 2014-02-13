#!/usr/bin/env python

# Call my recursive unzip script before running this

import argparse, os, csv

SENDMAIL = "/usr/sbin/sendmail"
TA_email = "liux1342@umn.edu"
course_name = " CSCI 1113 "
email_subject = "CSCI 1113 - Submission Error"
submission_directory_format = "HW0"
submission_files = ["{x500}_0A.cpp", "{x500}_0B.cpp"]

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
    result = merge(invalidSubmissions, {"No Submission or Submission is Not a Zip File":subStatus["no_sub"]})
    # Write to file
    sendEmail(result,user_data)
    writeToFile(result, args.output)

def sendEmail(Dict,userDict):
# Send emails 
	for key in Dict:
		p = os.popen("%s -t" %SENDMAIL, "w")
		p.write("To:"+TA_email+"\n")
		accountNames = Dict[key]
		emails = [userDict[item]["Email address"] for item in accountNames]
		p.write("BCC:"+",".join(emails)+"\n")
		p.write("Subject: "+email_subject+": "+key+"\n")
		p.write("\n")
		p.write("[THIS IS AN AUTOMATED MESSAGE - PLEASE DO NOT REPLY DIRECTLY TO THIS EMAIL]\n\n")
		p.write("Your submission on moodle site course "+course_name+" is invalid\n")
		p.write("The error detected is: "+key+"\n")
		p.write("Please following the submission instruction on you assignment and resubmit your assignment within the next 24 hours\n")
		p.write("Otherwise you won't get credit for this assignment\n")
		p.write("\n If you have any questions regarding this email, please only contact: "+TA_email+"\n\n Thanks\n\n")
		#p.write("\n".join(Dict[key]))
		p.close()
		
def writeToFile(Dict, filename):
# Write a big list
    if filename == None:
        filename = "output.txt"

    fout = open(filename, "w")
    for key in Dict:
       fout.write("---\n"+key+"\n---\n")
       for item in Dict[key]:
           fout.write(item+"@umn.edu"+"\n")
    fout.close()

def getInvalidSubmissions(user_data, submissions, sub_dir_format, sub_files, sub_dir):
	# Classifications
	bad_dir = []
	bad_filename = []
	missing_file = []
	extra_file = []
	extra_folder = []
	for moodle_sub in submissions:
		sub_path = getJoinStr().join([sub_dir,user_data[moodle_sub]["submission"]])
		sub_directory = getSubName(user_data[moodle_sub]["submission"])
		# sd = os.listdir(d)[0] 
		# Did they submit a zip file? If so, this should be a directory
		if not os.path.isdir(sub_path):
			bad_dir.append(moodle_sub)
		elif sub_directory != sub_dir_format.format(**user_data[moodle_sub]):
			bad_dir.append(moodle_sub)
		else: 
            # sub_dir_contents = getJoinStr().join([sub_directory])
			file_list = os.listdir(sub_path)		
			hasAllFiles = True
			has_extra_folder = False
			sub_item = os.listdir(sub_path)
			for fi in sub_item:
				one_item = getJoinStr().join([sub_path,fi])
				if os.path.isdir(one_item):
					has_extra_folder = True
			if has_extra_folder:
				extra_folder.append(moodle_sub)
			elif len(file_list) < len(sub_files):
				missing_file.append(moodle_sub)
			elif len(file_list) > len(sub_files):
				extra_file.append(moodle_sub)
			else:
				for f in sub_files:
					if f.format(**user_data[moodle_sub]) not in file_list:
						hasAllFiles = False
				if not hasAllFiles: 
					bad_filename.append(moodle_sub)
	return {"Bad Filename": bad_filename,\
            "Missing File": missing_file,\
            "Has Extra File": extra_file,\
            "Bad Zip Filename": bad_dir,\
			"Has Extra Folder": extra_folder}

def getSubName(moodle_name):
    # Remove what moodle adds
    end_string = 'assignsubmission_file_'
    end_of_moodle = moodle_name.index(end_string)+len(end_string)
    print(moodle_name[end_of_moodle:])
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
            if (datum["Last name"].lower() in sub.lower()) and (datum["First name"].lower() in sub.lower()):
                datum["submission"] = sub
                noSub.remove(datum["x500"])
                hasSub.append(datum["x500"])
                data.remove(datum)
            else:
                datum["submission"] = "no_submission"
    return {"no_sub": noSub, "has_sub": hasSub}

def addx500(datum):
    x500 = getx500(datum)
    datum["x500"] = x500
    return x500

def getx500(datum):
    return datum["Username"].split("@")[0]

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
