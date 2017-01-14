import os, codecs, re

def do_replacements_on(line):
    # line = re.sub(r"-([0-9])-", r"-0\1-", line)
    # line = re.sub(r"-([0-9])\s", r"-0\1 ", line)
    # line = re.sub(r"1900", "2000", line)
    # line = re.sub(r"1899", "1999", line)
    # line = re.sub(r"NULL", "", line)
    line = re.sub(r"'", "", line)
    return line

fName = "resources/menu/OrderEntry-2.csv"
inFile = codecs.open(fName, "r", "utf-8")
outFile = codecs.open(fName + ".new", "w", "utf-8")
for line in inFile:
    newline = do_replacements_on(line)
    outFile.write(newline)
inFile.close()
outFile.close()
os.rename(fName + ".new", fName)
