import sys
import os
import requests
from numpy.polynomial import Chebyshev
import datetime
from dateutil.relativedelta import relativedelta

degree = 64

jplCommand = "301"
planet = "northnode"

os.system("mkdir -p results/" + planet)

yearRange = range(1900, 2100)
if len(sys.argv) > 1:
  century = int(sys.argv[1]) * 100
  yearRange = range(century, century + 100)

  if century < 20:
    yearRange = reversed(yearRange)
  
#year = 2022
#for year in range(1666, 2223):

for year in yearRange:
  for month in range(1,13):
    filename = "results/" + planet + "/" + jplCommand + "node."+str(year)+"-"+str(month)+".cheb.txt"

    if os.path.isfile(filename):
      continue

    print(jplCommand, planet, year, month)

    lastTime = None

    lastDayOfMonth = (datetime.datetime(year, month, 1) + relativedelta(months=1, days=-1)).day

    lastVal = None
    rollCount = 0
    unrolledValues = []
    times = []

    for day in range(1,lastDayOfMonth + 1):
      date = datetime.datetime(year, month, day)
      nextDate = date + relativedelta(days = 1)
      stopYear = nextDate.year
      stopMonth = nextDate.month
      stopDay = nextDate.day

      url = "https://ssd.jpl.nasa.gov/api/horizons.api?" \
            + "format=text" \
            + "&COMMAND=" + jplCommand \
            + "&OBJ_DATA=NO" \
            + "&MAKE_EPHEM=YES" \
            + "&EPHEM_TYPE=ELEMENTS" \
            + "&CENTER=500@399" \
            + f"&START_TIME={year}-{month}-{day}" \
            + f"&STOP_TIME={stopYear}-{stopMonth}-{stopDay}" \
            + "&STEP_SIZE=1m"

      response = None
      while response is None:
        print(url)
        try:
          response = requests.get(url)
        except Exception as e:
          response = None

      in_table = False
      skip_line = True

      for line in response.iter_lines():
        if line == b"$$SOE":
          in_table = True
        elif line == b"$$EOE":
          in_table = False
        elif in_table:
          if b"TDB" in line:
            if line != lastTime:
              lastTime = line
              skip_line = False
            else:
              print("skipping", line)
          if b'OM=' in line:
            if not skip_line:
              skip_line = True
              columns = line.split()
              if columns[0] != b"OM=":
                print("PROBLEM", lastTime, line)
                exit
              valString = columns[1]
              valOrig = float(valString)
              
              if lastVal is not None:
                if valOrig - lastVal < -180:
                  rollCount += 1
                elif valOrig - lastVal > 180:
                  rollCount -= 1
              valUnrolled = valOrig + rollCount * 360
              lastVal = valOrig
              unrolledValues.append(valUnrolled)
              times.append(len(times) / 60 / 24)

    print(month, len(times))

    c = Chebyshev.fit(times, unrolledValues, deg=degree)

    print([c])
    with open("results/" + planet + "/" + jplCommand + "node."+str(year)+"-"+str(month)+".cheb.txt", "w") as file:
      file.write(str(c.domain.tolist()) + "\n")
      file.write("\n".join(str(x) for x in c.coef.tolist()) + "\n")
