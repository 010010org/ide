teststring = "testing('hahahaah')"

def stripping():
    teststring.replace('"', '')
    return teststring.encode()

def testing(yes):
    print(yes)
    return "hallo"

stripping()
print(type(teststring.encode()))
