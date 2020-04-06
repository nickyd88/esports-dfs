
import csv

#input is name map csv, output is dictionary

def GetNameMap(csvfile):
    map = {}
    with open(csvfile) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = 1
        r = 0
        for row in reader:
            if r < header:
                r += 1
            else:
                map[row[0]] = row[1]
        return map


