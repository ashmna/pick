import os, codecs, re
import time
import datetime

def do_replacements_on(line):
    line = re.sub(r"([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})", (lambda m: "%d" % time.mktime(datetime.datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S").timetuple()) ), line)
    return line


fName = "resources/menu/OrderEntry.csv"
inFile = codecs.open(fName, "r", "utf-8")
outFile = codecs.open(fName + ".new", "w", "utf-8")
for line in inFile:
    newline = do_replacements_on(line)
    outFile.write(newline)
inFile.close()
outFile.close()
os.rename(fName + ".new", fName + ".timestamp")
