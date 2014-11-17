# Not to be included by modules other than the menu submodules

def print_menu_common(dec, name, optenum, options):
    print()
    print(dec*80)
    print(dec + name.center(78) + dec)
    print(dec*80)
    for i in range(len(optenum)):
        first = True
        for line in options[optenum(i+1)].split('\n'):
            if first:
                print(dec + str(i+1).rjust(3) + ' : ' + line.ljust(72) + dec)
                first = False
            else:
                print(dec + ' '*6 + line.ljust(72) + dec)
    print(dec*80)
    print()


def print_help_menu_common(name, optenum, options):
    print_menu_common('?', name, optenum, options)
