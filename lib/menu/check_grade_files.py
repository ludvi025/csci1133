from enum import Enum   # Available in Python 3.4+
from _common import *



class options(Enum):
    """Gives the option to either check all grade files for unfinished
    grading, or check all grade files for unfinished and in progress 
    grading."""
    UnfinishedOnly  = 1
    AllIncomplete   = 2
    PrintHelpText   = 3
    GoToMain        = 4


_ShortNames = {
    options.UnfinishedOnly:   "Unfinished grade files only",
    options.AllIncomplete:    "Unfinished and in progress grade files",
    options.PrintHelpText:    "Print help text",
    options.GoToMain:         "Go to the main menu",
}


# 72 character limit
_Explanations = {
    options.UnfinishedOnly: 
"""Will find and delete any grade files that contain the phrase "Grading
unfinished for" in them (which would indicate that the grader killed the
grading script while grading a homework).""",
    options.AllIncomplete:
"""In addition to removing the unfinished grading files, this option will
also remove and grade files that contain the phrase "Grading in progress
for" in them (which will only happen while someone is grading a file or
something went horribly wrong).""",
    options.PrintHelpText:
"""Unsurprisingly, print this help text.""",
    options.GoToMain:
"""Go back to the main menu.""",
}


def print_menu():
    common_print_menu('#', 'Check Grade Files', options, _ShortNames)


def print_help_menu():
    common_print_help_menu('Check Grade Files Extended Help', options, _Explanations)


def get_option(printmenu=False):
    if printmenu:
        print_menu()
    opt = common_get_option(options)
    while opt == options.PrintHelpText:
        print_help_menu()
        opt = common_get_option(options)
    return opt
