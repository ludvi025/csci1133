#!/usr/bin/env python

# Call my recursive unzip script before running this

import argparse, os, csv, configparser

SENDMAIL = "/usr/sbin/sendmail"

def main():
    # Command line options
    args = parseArgs() 
    config = parseConfig(args.config)

    # Map moodle ids to submission objects
    subs = getSubs(args.student_info_file)

    tests = [hasSubmission, checkForDirs, correctNumberOfFiles, correctSubmission]
    for t in tests:
        for sub in subs:
            t(sub, args.submissions_dir, config)

    ## Send email
    #if args.send_email:
        #if config.email and config.course and config.subject:
            #sendEmail(config.email, config.course, config.subject, result, user_data)
        #else:
            #print("Missing email information from config file")
    if args.send_email:
        if config["email"] and config["course"] and config["subject"]:
            sendEmail(config["email"], config["course"], config["subject"], subs)
        else:
            print("Missing email information from config file.")
    else:
        if config["email"] and config["course"] and config["subject"]:
            sendEmail(config["email"], config["course"], config["subject"], subs, True)

    ## Write to file
    if args.output:
        writeToFile(subs, args.output)

def hasSubmission(sub, sub_dir, config):
# Pair student info with submissions and add a "submission" key
    subs = os.listdir(sub_dir)
    if sub.moodle_id not in subs:
        sub.tag("no submission")

def checkForDirs(sub, sub_dir, config):
    if "no submission" not in sub:
        files = os.listdir(os.path.join(sub_dir,sub.moodle_id))
        if len(files) == 1 and os.path.isdir(os.path.join(sub_dir,sub.moodle_id,files[0])):
            sub.tag("nested")
        else:
            for f in files:
                if os.path.isdir(os.path.join(sub_dir,sub.moodle_id,f)):
                    sub.tag("extra directory")

def correctNumberOfFiles(sub, sub_dir, config):
    if "no submission" not in sub:
        items = os.listdir(os.path.join(sub_dir,sub.moodle_id))
        files = []
        for i in items:
            if not os.path.isdir(os.path.join(sub_dir,sub.moodle_id,i)):
                files.append(i)
        if len(files) > len(config["files"]):
            sub.tag("extra files")
        if len(files) < len(config["files"]):
            sub.tag("missing files")

def correctSubmission(sub, sub_dir, config):
    if "no submission" not in sub and "nested" not in sub:
        files = [removeMoodlePrefix(f) for f in os.listdir(os.path.join(sub_dir,sub.moodle_id))]
        correct_submission = True
        for f in config["files"]:
            correct_file = f.format(**sub.info()) 
            if correct_file in files:
                sub.match(correct_file)
            else:
                sub.miss(correct_file)
                correct_submission = False
                if "missing files" not in sub and "nested" not in sub:
                    sub.tag("incorrectly named")
        if correct_submission:
            sub.tag("correct submission")

def removeMoodlePrefix(s):
    return s.split('assign_submission_file_')[-1]

def sendEmail(TA_email, course_name, email_subject, submissions, test=False):
    # Send emails 
    for sub in submissions:
        if "correct submission" not in sub and "no submission" not in sub:
            if not test:
                p = os.popen("%s -t" %SENDMAIL, "w")
            else:
                p = open("email_dump.txt", "a")

            p.write("To:"+sub.email+"\n")
            p.write("Subject: "+email_subject+"\n")
            p.write("\n")
            p.write("[THIS IS AN AUTOMATED MESSAGE - PLEASE DO NOT REPLY DIRECTLY TO THIS EMAIL]\n\n")
            p.write("Your submission for "+course_name+" is invalid.\n")
            p.write("The following error flags have been detected: "+str(sub.tags)[1:-1]+"\n")
            p.write("The following files were correctly submitted: "+str(sub.matched_files)[1:-1]+"\n")
            p.write("The following files are missing: "+str(sub.missing_files)[1:-1]+"\n")
            p.write("Please follow the submission instructions on your assignment and resubmit your assignment within the next 24 hours.\n")
            p.write("Otherwise you won't get credit for this assignment.\n")
            p.write("\nIf you have any questions regarding this email, please contact: "+TA_email+"\n\n")
            p.close()
		
def writeToFile(subs, filename):
    # Write a big list
    fout = open(filename, "w")
    for s in subs:
        fout.write(str(s))
        fout.write("\n")
    fout.close()

def getJoinStr():
# Get the OS specific path string
    return os.path.join('.','.')[1:-1]

def getSubs(filename):
    data_file = csv.DictReader(open(filename))
    return [Submission(entry["Email address"], entry["Moodle ID"], ) for entry in data_file]
    #return {entry["Moodle ID"] : Submission(entry["Email address"]) for entry in data_file}

class Submission:
    def __init__(this, email, moodle_id):
        this.email = email
        this.x500 = email.split("@")[0]
        this.moodle_id = moodle_id
        this.tags = []
        this.matched_files = []
        this.missing_files = []

    def tag(this, tag):
        if (tag not in this.tags):
            this.tags.append(tag)

    def match(this, match):
        this.matched_files.append(match)

    def miss(this, miss):
        this.missing_files.append(miss)

    def info(this):
        return {"x500": this.x500, "Moodle ID": this.moodle_id, "Email address": this.email}

    def __contains__(this, tag):
        return tag in this.tags

    def __str__(this):
        return this.email + ' : \n\ttags : ' + str(this.tags) + '\n' \
                + '\tmatched : ' + str(this.matched_files) + '\n' \
                + '\tmissing : ' + str(this.missing_files)

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("student_info_file")
    parser.add_argument("submissions_dir")
    parser.add_argument("-c", "--config")
    parser.add_argument("-o","--output")
    parser.add_argument("-e", "--send_email")
    return parser.parse_args()

def parseConfig(config_file):
    parser = configparser.ConfigParser()
    opts = {}
    parser.read(config_file)

    opts['email'] = parser['EMAIL']['email']
    opts['course'] = parser['EMAIL']['course']
    opts['subject'] = parser['EMAIL']['subject']

    opts['files'] = eval(parser['TEMPLATE']['files'])
    return opts

if __name__ == "__main__":
    main()

#def getInvalidSubmissions(user_data, submissions, sub_dir_format, sub_files, sub_dir):

    ## Classifications
    #bad_dir = []
    #bad_filename = []
    #missing_file = []
    #extra_file = []
    #extra_folder = []
    #for moodle_sub in submissions:
        #sub_path = getJoinStr().join([sub_dir,user_data[moodle_sub]["submission"]])
        #sub_directory = getSubName(user_data[moodle_sub]["submission"])
        ## sd = os.listdir(d)[0] 
        ## Did they submit a zip file? If so, this should be a directory
        #if not os.path.isdir(sub_path):
                #bad_dir.append(moodle_sub)
        #elif sub_directory != sub_dir_format.format(**user_data[moodle_sub]):
                #bad_dir.append(moodle_sub)
        #else: 
            ## sub_dir_contents = getJoinStr().join([sub_directory])
            #file_list = os.listdir(sub_path)		
            #hasAllFiles = True
            #has_extra_folder = False
            #sub_item = os.listdir(sub_path)
            #for fi in sub_item:
                #one_item = getJoinStr().join([sub_path,fi])
                #if os.path.isdir(one_item):
                    #has_extra_folder = True
            #if has_extra_folder:
                #extra_folder.append(moodle_sub)
            #elif len(file_list) < len(sub_files):
                #missing_file.append(moodle_sub)
            #elif len(file_list) > len(sub_files):
                #extra_file.append(moodle_sub)
            #else:
                #for f in sub_files:
                    #if f.format(**user_data[moodle_sub]) not in file_list:
                        #hasAllFiles = False
                #if not hasAllFiles: 
                    #bad_filename.append(moodle_sub)
    #return {"Bad Filename": bad_filename,\
        #"Missing File": missing_file,\
        #"Has Extra File": extra_file,\
        #"Bad Zip Filename": bad_dir,\
        #"Has Extra Folder": extra_folder}

#def getSubName(moodle_name):
    ## Remove what moodle adds
    #end_string = 'assignsubmission_file_'
    #end_of_moodle = moodle_name.index(end_string)+len(end_string)
    #print(moodle_name[end_of_moodle:])
    #return moodle_name[end_of_moodle:]

#def merge(d1, d2):
## Combine two dicts
    #return dict(d1.items()+d2.items())
    
#def addx500(datum):
    #x500 = getx500(datum)
    #datum["x500"] = x500
    #return x500
