from enum import Enum   # Available in Python 3.4+
# An example interface for all of the other menu modules


class options(Enum):
    # The enum to define all the elements of this menu
    pass

_ShortNames = {}

_Explanations = {}

def print_menu():
    # A method used to print the menu using _ShortNames
    pass

def print_help_menu():
    # A method used to print the menu using _Explanations
    pass

def get_option():
    # A method to solict and verify the input from the user
    pass
