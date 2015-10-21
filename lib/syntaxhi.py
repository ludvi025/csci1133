# Is a string an official python keyword or an operator?
def is_keyword(s):
        s = str(s)
        keywords = ['and', 'as', 'assert', 'bool', 'break', 'chr', 'class',
        'continue', 'def', 'del', 'del', 'dict', 'elif', 'else', 'except',
        'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'int', 'is',
        'lambda', 'len', 'list', 'nonlocal', 'not', 'open', 'or', 'pass', 'print',
        'raise', 'return', 'set', 'str', 'try', 'while', 'with', 'yield']
        return s in keywords

# Is a string a value? (bool / number / None)
def is_value(s):
        s = str(s)
        values = ['False', 'None', 'True']
        return s in values or is_number(s)

# Is a string a number? (float / int)
def is_number(s):
        s = str(s)
        for c in s:
                if not c.isdigit() and c != ".":
                        return False
        return True

# Is a string a string "with quotes around it?"
def is_string(s):
        if not s:
                return False
        s = str(s)
        if (s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'"):
                return True
        return False

# Is a string a comment?
def is_comment(s):
        s = str(s)
        if not s:
                return False
        if (s[0] == "#"):
                return True
        return False

# Syntax highlight a word using ANSI colors
def color_word(s):
        s = str(s)
        if is_value(s):
                return "\x1B[38;2;255;18;18m" + s + "\033[0m"
        elif is_keyword(s):
                return "\x1B[38;2;255;177;18m" + s + "\033[0m"
        elif is_string(s):
                return "\x1B[38;2;18;232;18m" + s + "\033[0m"
        elif is_comment(s):
                return "\x1B[38;2;18;156;238m" + s + "\033[0m"
        else:
                return s

# List of words and symbols in a string
def words(s):
        s = str(s)
        separators = " ()[]{}+=-/*%&^|><,:;"
        s_chars = "'\""
        word_list = []
        in_string = False
        start = 0
        end = 1
        while end < len(s):
                if s[start] in s_chars:
                        in_string = True
                if not in_string:
                        if s[end] in separators:
                                word_list.append(s[start:end])
                                start = end
                        elif s[start] in separators:
                                word_list.append(s[start])
                                start += 1
                else:
                        if s[end] in s_chars:
                                in_string = False
                                word_list.append(s[start:end + 1])
                                start = end + 1
                end += 1
        word_list.append(s[start:])
        return word_list

# Colors a string of Python syntax
def color_line(line):
        line = str(line)
        lwords = words(line)
        i = 0
        if not is_comment(line.lstrip()):
                while i < len(lwords):
                        lwords[i] = color_word(lwords[i])
                        i += 1
                return "".join(lwords)
        else:
                line = "\x1B[38;2;18;156;238m" + line + "\033[0m"
                return line
