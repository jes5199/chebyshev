import sys
import math
import os
import struct
from datetime import datetime

startedAt = datetime.now()

planet = sys.argv[1] # e.g. "sun"

valueName = "longitude"
if len(sys.argv) > 2:
    valueName = sys.argv[2] # e.g. "latitude"

#cutoff = math.pow(10.0,-5)
cutoff = 1.0 / 60 / 60 / 4

body = None

records = {}

# iterate over all of the files in the directory
for filename in os.listdir("results/" + planet):
    nameParts = filename.split(".")

    if body is None:
        body = nameParts[0]
    elif body != nameParts[0]:
        body2 = nameParts[0]
        raise Exception(f"Problem! inconsistent planet id {body} vs {body2}")

    fileValueName = nameParts[2]
    if fileValueName == "cheb":
        fileValueName = "longitude"

    if fileValueName != valueName:
        continue

    yearAndMonth = nameParts[1].split("-")
    year = int(yearAndMonth[0])
    month = int(yearAndMonth[1])

    #if year < 1900:
    #  continue
    #if year >= 2100:
    #  continue

    record = []

    with open("results/" + planet + "/"+ filename) as file:
        days = int(file.readline().split(", ")[1].split(".")[0])
        record = [days]
        for degreeString in file.readlines():
            record.append(float(degreeString))

        while len(record) > 3 and abs(record[-1]) < cutoff:
            record.pop()

    if records.get(year) is None:
        records[year] = [None] * 12
    records[year][month - 1] = record

last = None

niceStartedAt = startedAt.strftime("%y-%m-%dT%H:%M:%S")
century = -100000
outfileName = None
file = None
maxDegrees = 0

for year in sorted(records.keys()):
    newCentury = math.floor(year / 100)
    if newCentury != century:
        century = newCentury

        outfileName = f"results/{planet}.{century}00s.weft"
        if valueName != "longitude":
            outfileName = f"results/{planet}.{century}00s.{valueName}.weft"

        print(outfileName)
        file = open(outfileName, "w+b")

        preamble = f"#weft! v0.01 {planet} jpl:{body} {century}00s 32bit {valueName} chebychevs generated@{niceStartedAt}"
        
        # align to 16bit word for aesthetics when reading hexdumps
        if len(preamble) % 2 == 0:
            preamble += " "
        #print(preamble)
        
        file.write(bytes(preamble + "\n" + "\0\0", "utf8"))


    for index, record in enumerate(records[year]):
        if record is None:
            pass
        else:
            month = index + 1
            days = record[0]
            degreeCount = len(record) - 1
            degrees = record[1:]
            data = struct.pack(f"!hBBI{degreeCount}f", year, month, days, degreeCount, *degrees)
            file.write(data + b"\0\0")
            last = [year, month, days, degreeCount]
            if degreeCount > maxDegrees:
                maxDegrees = degreeCount

#print(*last)
print(f"up to {maxDegrees} degrees")
