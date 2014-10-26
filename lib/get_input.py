from random import randint

# For bad input
#   "Try to limit to the length of this text to prevent egregious output."
witty_comebacks = [
    "You're smarter than that...",
    "And you think you're good enough to be a TA?",
]


def get_witty_comeback():
    return witty_combacks[randint(0, len(witty_comebacks)-1)]


def yes_or_no(prompt_string):
    """Returns true for an affirmatory input by appending " (y/n): " on to the
    prompt string. See functin definition for what counts as affirmatory. This
    function tends towards a whitelist of confirmation actions."""
    prompt_string += ' (y/n): '
    yesses = ['y', 'yes']

    result = input(prompt_string)
    return (result.lower() in yesses)


def grade(maxpoints):
    grade = -1
    if maxpoints == -1:
        maxpoints = float('inf')
    while (grade > maxpoints) or (grade < 0):
        gradestr = input('Enter grade: ')
        try:
            grade = float(gradestr)
        except ValueError:
            print("Not a valid grade.", get_witty_comeback())
    return grade