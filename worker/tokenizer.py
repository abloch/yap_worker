import sys
import json
import csv

filename = sys.argv[1]
inputdata = json.load(open(filename))
outputdata = csv.DictWriter(open(filename + ".csv", "w"), fieldnames = inputdata[0].keys())
for i in inputdata:
    i['tokens'] = " ".join([t['root'] for t in i['tokens']])
    del i["raw_yap"]
    
outputdata.writerows(inputdata)
