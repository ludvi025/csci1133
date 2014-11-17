from enum import Enum   # Available in Python 3.4+



class _enum(Enum):
    """The main menu options available after setting up the grading session."""
    GradeHomeworks      = 1
    CheckGradeFiles     = 2
    GradingStatistics   = 3
    ConsolidateGrades   = 4
    PrintHelpText       = 5
    TerminateProgram    = 6


_ShortNames = {
    _enum.GradeHomeworks:   "Go to grading homeworks",
    _enum.CheckGradeFiles:  "Go to checking grade files",
    _enum.GradingStatistics:"Compute some statistics",
    _enum.ConsolidateGrades:"Consolidate grade files",
    _enum.PrintHelpText:    "Print help text",
    _enum.TerminateProgram: "Cleanly exit this script",
}


_Explanations = {
    _enum.GradeHomeworks: 
"""Enter the grade homework assignment menu, after passing verification that \
there are still homeworks that need grading.""",
    _enum.CheckGradeFiles:
"""Enter the check grade files menu to cleanup any grade files corresponding \
to unfinished or in progress grading.""",
    _enum.GradingStatistics:
"""Show some grading statistics. Will compute average grade, number graded per \
grader, average grade per grader, and maybe even grading rate. Note that this \
may be slow as it will compute the statistics upon calling and not continually \
in the background.""",
    _enum.ConsolidateGrades:
"""The graduate TA part of the job that consolidates all the individual grade \
files into one large CSV.""",
    _enum.PrintHelpText:
"""Unsurprisingly, print this help text.""",
    _enum.TerminateProgram:
"""A way to cleanly exit the grading script. This is much preferred to mashing \
Ctrl-C like a monkey with a bone after encountering a monolith.""",
}


def print_menu():
    pass


def print_help_menu():
    pass


def get_option():
    pass
