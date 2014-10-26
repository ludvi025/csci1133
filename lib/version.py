#! /usr/env/python
# A way to get the number of revisions in git
# The number of revisions is what we use as a version number, divided by 100
import subprocess
import os.path


def get_version():
    # Chdir to the location of this file (hopefully the git repo)
    olddir = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    # Call git for the versioning
    version = subprocess.Popen(['git', 'rev-list', 'HEAD', '--count'],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    version.wait()
    version = version.communicate()[0].decode()
    # Restore old dir
    os.chdir(olddir)

    try:
        version = '{0:06.2f}'.format(int(version)/100)
    except:
        version = 'NOGIT'
    return version
