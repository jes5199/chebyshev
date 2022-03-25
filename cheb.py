import sys
import os
import requests
from numpy.polynomial import Chebyshev

planet = "moon"
jplCommand = "199"
degree = 32

os.system("mkdir -p results/" + planet)

#year = 2022
for year in range(1900, 2201):

  for month in range(1,13):
    nextMonthYear = year + 1 if month == 12 else year
    nextMonth = 1 if month == 12 else month + 1

    print(month, year)

    url = "https://ssd.jpl.nasa.gov/api/horizons.api?format=text&COMMAND=%27" + jplCommand+ "%27&OBJ_DATA=%27NO%27&MAKE_EPHEM=%27YES%27&EPHEM_TYPE=%27OBSERVER%27&CENTER=%27500@399%27&START_TIME=%27"+str(year)+"-"+str(month)+"-01%27&STOP_TIME=%27"+str(nextMonthYear)+"-"+str(nextMonth)+"-01%27&STEP_SIZE=%271m%27&QUANTITIES=%2731%27"


    response = None
    while response is None:
      print(url)
      try:
        response = requests.get(url)
      except Exception as e:
        response = None

    in_table = False

    lastVal = None
    rollCount = 0
    unrolledValues = []
    times = []

    if len(times) > 0:
      unrolledValues.pop()
      times.pop()

    for line in response.iter_lines():
      if line == b"$$SOE":
        in_table = True
      elif line == b"$$EOE":
        in_table = False
      elif in_table:
        columns = line.split()
        valString = columns[2]
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
    with open("results/" + planet + "/" + jplCommand + "."+str(year)+"-"+str(month)+".cheb.txt", "w") as file:
      file.write(str(c.domain.tolist()) + "\n")
      file.write("\n".join(str(x) for x in c.coef.tolist()) + "\n")
