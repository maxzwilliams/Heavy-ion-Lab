"""
File for analysing lab2 data
"""

import math
import matplotlib.pyplot as plt
import time
from datetime import datetime
import pickle
import os


def dataReader(filename):
    data = []
    calibration = []
    f = open(filename, "r")
    counter = 0
    inData = False
    inCal = False
    for x in f:
        if ("<<END>>" in x and inData == True):
            inData = False

        if ("<<DATA>>" in x):
            inCal = False

        if (inCal and not inData):
            newEntry = x.split(" ")
            newEntry[1] = newEntry[1][:-1]
            calibration.append([float(newEntry[0]), float(newEntry[1])])

        if (inData):
            data.append(float(x[:-1]))
        if ("LIVE_TIME" in x):
            livetime = float(x[12:])
            ##print(livetime)
        if ("REAL_TIME" in x):
            realtime = float(x[12:])
            ##print(realtime)
        if ("START_TIME" in x):
            dateTime = x[13:-1]
            dateTime = datetime.strptime(dateTime, '%m/%d/%Y %H:%M:%S')
        if ("<<DATA>>" in x and inData == False):
            inData = True
        if ("LABEL - Channel" in x):
            inCal = True
        counter += 1
    return data, livetime, realtime, dateTime


def calibrationReader(filename):
    data = []
    f = open(filename, "r")
    counter = 0
    for x in f:
        ##print("counter", counter, x)
        ##time.sleep(0.1)
        if (counter >= 19):
            try:
                data.append(float(x[:-1]))
            except:
                pass
        if (counter == 7):
            livetime = float(x[12:])
            ##print(livetime)
        if (counter == 8):
            realtime = float(x[12:])
            ##print(realtime)
        if (counter == 9):
            dateTime = x[13:-1]
            dateTime = datetime.strptime(dateTime, '%m/%d/%Y %H:%M:%S')
        counter += 1
        ##print(data)
    f.close()
    return data, livetime, realtime, dateTime

##calibrationReader("data\BASampleSetBCal.mca")

def dataReaderFullSet(baseName, bound):
    datasets = []
    extension = ".mca"
    if (bound >= 10):
        for b in range(1,bound+1):
            if (b < 10):
                datasets.append(dataReader(baseName +str("0")+str(b) + extension))
            else:
                datasets.append(dataReader(baseName +str(b)+ extension))
    else:
        for b in range(1,bound+1):
            datasets.append(dataReader(baseName +str(b) + extension))
    return datasets

def readEverything():
    additionalPath = "data/"
    baseNames = ["120s_","10mins_","30mins_","onehr_","twohr_", "sixhr_","eighthr_","twelvehr_"]
    baseNames = [additionalPath + b for b in baseNames]
    bounds = [10, 5, 12, 15, 12, 4, 3, 6]
    bigData = [ [calibrationReader("data/EUSampleSetBCal.mca"),calibrationReader("data/BASampleSetBCal.mca")] ]
    ##bigData = []
    for index in range(len(baseNames)):
        bigData.append( dataReaderFullSet(baseNames[index], bounds[index]))
    pickle.dump(bigData, open("formattedData.p", "wb"))
    return bigData
    

print("starting read")
readEverything()
print("done reading")

