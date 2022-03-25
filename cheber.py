import sys
import os
import requests
from numpy.polynomial import Chebyshev
import time

planet = sys.argv[1] # e.g. "sun"
jplCommand = sys.argv[2] # e.g. "10"
degree = 64

lastUrl = None
responseLines = []

os.system("mkdir -p results/" + planet)

yearRange = range(1900, 2100)
if len(sys.argv) > 3:
  if (sys.argv[3]) == "us":
    yearRange = range(1969, 1985)
  elif (sys.argv[3]) == "kids":
    yearRange = range(2015, 2023)
  elif (sys.argv[3]) == "soon":
    yearRange = range(2022, 2035)
  elif (sys.argv[3]) == "90s":
    yearRange = range(1990, 2001)
  elif (sys.argv[3]) == "21st":
    yearRange = range(2000, 2070)
  elif (sys.argv[3]) == "parents":
    yearRange = range(1940, 1970)
  else:
    century = int(sys.argv[3]) * 100
    yearRange = range(century, century + 100)

    if century < 2000:
      yearRange = reversed(yearRange)

#valueName = "longitude"
#if len(sys.argv) > 4:
#  if sys.argv[4] in ["latitude"]:
#    valueName = sys.argv[4]
  
#year = 2022
#for year in range(1666, 2223):

for year in yearRange:
  for month in range(1,13):
    for valueName in ["longitude", "latitude"]:
      nextMonthYear = year + 1 if month == 12 else year
      nextMonth = 1 if month == 12 else month + 1

      jplCommandSafe = jplCommand.replace(" ", "_")

      filename = "results/" + planet + "/" + jplCommandSafe + "."+str(year)+"-"+str(month)+".cheb.txt"
      if valueName != "longitude":
        filename = "results/" + planet + "/" + jplCommandSafe + "."+str(year)+"-"+str(month)+f".{valueName}.cheb.txt"

      if os.path.isfile(filename):
        with open(filename, 'r') as existingData:
          count = len(existingData.readlines())
          if count >= degree + 2:
            continue
          else:
            print("need to redo:", count - 2, "is less than", degree)

      print(jplCommand, planet, year, month, valueName)

      url = "https://ssd.jpl.nasa.gov/api/horizons.api?format=text&COMMAND=%27" + jplCommand+ "%27&OBJ_DATA=%27NO%27&MAKE_EPHEM=%27YES%27&EPHEM_TYPE=%27OBSERVER%27&CENTER=%27500@399%27&START_TIME=%27"+str(year)+"-"+str(month)+"-01%27&STOP_TIME=%27"+str(nextMonthYear)+"-"+str(nextMonth)+"-01%27&STEP_SIZE=%271m%27&QUANTITIES=%2731%27"

      if url != lastUrl:
        response = None
        while response is None:
          print(url)
          try:
            response = requests.get(url, timeout=6)
            responseLines = list(response.iter_lines())
            print("ok")
          except Exception as e:
            print(e)
            response = None
        lastUrl = url
      else:
        print(f"reusing last request for {valueName}")

      in_table = False

      lastVal = None
      rollCount = 0
      unrolledValues = []
      times = []

      #if len(times) > 0:
      #  unrolledValues.pop()
      #  times.pop()

      for line in responseLines:
        if line == b"$$SOE":
          in_table = True
        elif line == b"$$EOE":
          in_table = False
        elif in_table:
          columns = line.split()
          valString = None
          if valueName == "longitude":
            valString = columns[2]
          elif valueName == "latitude":
            valString = columns[3]

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
      #jplCommandSafe = jplCommand.replace(" ", "_")

      print([c])
      #with open("results/" + planet + "/" + jplCommandSafe + "."+str(year)+"-"+str(month)+".cheb.txt", "w") as file:
      with open(filename, "w") as file:
        file.write(str(c.domain.tolist()) + "\n")
        file.write("\n".join(str(x) for x in c.coef.tolist()) + "\n")
      time.sleep(1)
