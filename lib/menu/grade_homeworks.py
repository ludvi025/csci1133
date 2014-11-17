from enum import Enum   # Available in Python 3.4+



class _enum(Enum):
    """The grading homeworks menu options."""
    RunCode         = 1
    ViewCode        = 2
    EditCode        = 3 #BETA
    GradeCode       = 4
    PrintHelpText   = 5
    GoToMain        = 6


_ShortNames = {
    _enum.RunCode:      "Run the code",
    _enum.ViewCode:     "Print the code",
    _enum.EditCode:     "BETA BETA edit the code BETA BETA",
    _enum.GradeCode:    "Enter grades for the code",
    _enum.PrintHelpText:"Print help text",
    _enum.GoToMain:     "Go to the main menu",
}


_Explanations = {
    _enum.RunCode: 
"""Run the homework code in a Python subprocess, optionally piping input if so \
defined by the session file.""",
    _enum.ViewCode:
"""Print the code to the console.""",
    _enum.EditCode:
"""!!UNSUPPORTED BETA OPTION!! If this feature is ever implemented, it will \
open an editor in order to edit the code. !!UNSUPPORTED BETA OPTION!!""",
    _enum.GradeCode:
"""Enter a grade and comments for the code before saving the finished grade \
file. Will then select the next file and enter this menu again.""",
    _enum.PrintHelpText:
"""Unsurprisingly, print this help text.""",
    _enum.GoToMain:
"""Go back to the main menu.""",
}


def print_menu():
    pass


def print_help_menu():
    pass


def get_option():
    pass

