from enum import Enum   # Available in Python 3.4+



class options(Enum):
    """The main menu options available after setting up the grading session."""
    GradeHomeworks      = 1
    CheckGradeFiles     = 2
    GradingStatistics   = 3
    ConsolidateGrades   = 4
    PrintHelpText       = 5
    TerminateProgram    = 6


_ShortNames = {
    options.GradeHomeworks:   "Go to grading homeworks",
    options.CheckGradeFiles:  "Go to checking grade files",
    options.GradingStatistics:"Compute some statistics",
    options.ConsolidateGrades:"Consolidate grade files",
    options.PrintHelpText:    "Print help text",
    options.TerminateProgram: "Cleanly exit this script",
}


_Explanations = {
    options.GradeHomeworks: 
"""Enter the grade homework assignment menu, after passing verification that \
there are still homeworks that need grading.""",
    options.CheckGradeFiles:
"""Enter the check grade files menu to cleanup any grade files corresponding \
to unfinished or in progress grading.""",
    options.GradingStatistics:
"""Show some grading statistics. Will compute average grade, number graded per \
grader, average grade per grader, and maybe even grading rate. Note that this \
may be slow as it will compute the statistics upon calling and not continually \
in the background.""",
    options.ConsolidateGrades:
"""The graduate TA part of the job that consolidates all the individual grade \
files into one large CSV.""",
    options.PrintHelpText:
"""Unsurprisingly, print this help text.""",
    options.TerminateProgram:
"""A way to cleanly exit the grading script. This is much preferred to mashing \
Ctrl-C like a monkey with a bone after encountering a monolith.""",
}


def print_menu():
    pass


def print_help_menu():
    pass


def get_option():
    pass
