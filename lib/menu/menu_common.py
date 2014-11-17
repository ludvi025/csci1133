# Not to be included by modules other than the menu submodules

def print_menu_common(dec, name, optenum, options):
    print()
    print(dec*80)
    print(dec + name.center(78) + dec)
    print(dec*80)
    for i in range(len(optenum)):
        print(dec + str(i+1).rjust(3) + ' : ' + options[optenum(i+1)].ljust(72) + dec)
    print(dec*80)
    print()
