import runWithInput

test = open(input("Enter a test script: "))
test_lines = test.read()

print(runWithInput.runInteractive("mod.py", test_lines)[0])
