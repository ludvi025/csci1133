from enum import Enum   # Available in Python 3.4+
from lib.menu._common import *



class options(Enum):
    """The grading homeworks menu options."""
    RunTests        = 1
    RunShell        = 2
    ViewCode        = 3
    #EditCode        = 3 #BETA
    GradeCode       = 4
    PrintHelpText   = 5
    NextHomework    = 6


_ShortNames = {
    options.RunTests:      "Run the code",
    options.RunShell:     "Start a python shell",
    options.ViewCode:     "Print the code",
    #options.EditCode:     "BETA BETA edit the code BETA BETA",
    options.GradeCode:    "Enter grades for the code",
    options.PrintHelpText:"Print help text",
    options.NextHomework: "Continue / Main Menu"
}


# 72 character limit
_Explanations = {
    options.RunTests: 
"""Run the homework code in a Python subprocess, optionally piping input if
so defined by the session file.""",
    options.RunShell:
"""Open the student's code in an interactive python shell. Press Ctrl+D to 
return to script. Hint: Call `dir()` to see what's available.""",
    options.ViewCode:
"""Print the code to the console.""",
#    options.EditCode:
#"""!!UNSUPPORTED BETA OPTION!! If this feature is ever implemented, it will
#open an editor in order to edit the code. !!UNSUPPORTED BETA OPTION!!""",
    options.GradeCode:
"""Enter a grade and comments for the code before saving the finished grade
file. Will then select the next file and enter this menu again.""",
    options.PrintHelpText:
"""Unsurprisingly, print this help text.""",
    options.NextHomework:
"""Uhm... grade the next homework..."""
}


def print_menu():
    common_print_menu('#', 'Grade Homeworks', options, _ShortNames)


def print_help_menu():
    common_print_help_menu('Grade Homeworks Extended Help', options, _Explanations)


def get_option(printmenu=False):
    if printmenu:
        print_menu()
    opt = common_get_option(options)
    while opt == options.PrintHelpText:
        print_help_menu()
        opt = common_get_option(options)
    return opt
