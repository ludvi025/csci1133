from enum import Enum   # Available in Python 3.4+
from menu_common import *



class options(Enum):
    """The grading homeworks menu options."""
    RunCode         = 1
    ViewCode        = 2
    EditCode        = 3 #BETA
    GradeCode       = 4
    PrintHelpText   = 5
    GoToMain        = 6


_ShortNames = {
    options.RunCode:      "Run the code",
    options.ViewCode:     "Print the code",
    options.EditCode:     "BETA BETA edit the code BETA BETA",
    options.GradeCode:    "Enter grades for the code",
    options.PrintHelpText:"Print help text",
    options.GoToMain:     "Go to the main menu",
}


_Explanations = {
    options.RunCode: 
"""Run the homework code in a Python subprocess, optionally piping input if so \
defined by the session file.""",
    options.ViewCode:
"""Print the code to the console.""",
    options.EditCode:
"""!!UNSUPPORTED BETA OPTION!! If this feature is ever implemented, it will \
open an editor in order to edit the code. !!UNSUPPORTED BETA OPTION!!""",
    options.GradeCode:
"""Enter a grade and comments for the code before saving the finished grade \
file. Will then select the next file and enter this menu again.""",
    options.PrintHelpText:
"""Unsurprisingly, print this help text.""",
    options.GoToMain:
"""Go back to the main menu.""",
}


def print_menu():
    pass


def print_help_menu():
    pass


def get_option():
    pass

