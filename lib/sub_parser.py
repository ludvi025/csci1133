import re

regex = r"(?:.*/)?(?P<firstname>[^/]*) (?P<lastname>[^/]*)_(?P<moodleid>\d*)_\w*_\w*_\w*/?.*"
#compileing the regex is optional. It is a performance optimization.
cmp_regex = re.compile(regex)

def parse(file_name):
    m = re.match(cmp_regex, file_name)
    if m:
      return {
          'lastname' : m.group('lastname'), 
          'firstname' : m.group('firstname'), 
          'moodleid' : m.group('moodleid')
      }
    else:
      return {
          'lastname' : '', 
          'firstname' : '', 
          'moodleid' : ''
          }

def test():
    test1 = "firstname lastname_1128269_assignsubmission_file_HW2/"
    test2 = "firstname(alternatefirstname) lastname_1093811_assignsubmission_file_HW2/"
    test3 = "stuff/directories/firstname lastname_1128269_assignsubmission_file_HW2/"
    test4 = "stuff/directories/firstname lastname_1128269_assignsubmission_file_HW2/stuffagain/file.py"
    test5 = "stuff/directories/firstname(alternatefirstname) lastname_1093811_assignsubmission_file_HW2/moredire/file.py"
    test6 = ""

    for test in [test1, test2, test3, test4, test5, test6]:
        print(parse(test))
