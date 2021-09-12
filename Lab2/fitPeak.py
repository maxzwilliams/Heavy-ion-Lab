"""
Program for fitting peaks

Lets only include simple single peaks here
"""

import math
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import datetime
import random
import time
## we want to be given names and the full data set
## we want to give the counts per live time as a function of real time

## takes the full data and  the names
## returns a dictionary. The dictionary has keys that are names
## is has value that is a dictionary
## each dictionary has key of peak location and values [counts per live time, time of measurement]

## each data point has something that looks like xData, yData, livetime, realtime, dateTime
def fitAll(fullData, names):
    namesToPeaks = dict()
    for key in names:
        namesToPeaks[names[key]] = []

    for key in names:
        namesToPeaks[names[key]].append(key)


    bigDict = dict()
    actualNames = set()
    for key in list(names.keys()):
        actualNames.add(names[key])
        bigDict[names[key]] = dict()

    ##fullData.reverse()
    counter = 0
    for data in fullData:
        xData, yData, liveTime, realTime, dateTime = data
        counter = counter + 1
        for n in actualNames:
            for peak in namesToPeaks[n]:


                guess = [1000, 0 ,max(yData), peak, 2]
                ##lowerBounds = [0, -2, 0, 0, 0]
                ##upperBounds = [float('inf'), 2, float('inf'), float('inf'), 3]
                lowerBounds = [float("-inf"), float("-inf"),float("-inf"), peak-1, 0.1]
                upperBounds = [float("inf"), float("inf"),float("inf"), peak+1, 100]
                bounds = (lowerBounds,upperBounds)
                dataName = "time " + str(dateTime) + " element " + str(n) + " at " + str(peak)

                totalIntensity, totalIntensityUncert, center, centerU = fitPeak(xData, yData, peak-6, peak+6, guess, bounds, dataName)
                if (counter == 1):


                    if (peak == 343.99):
                        print("+++++++++++++++++++++++")
                        print(n ,center,centerU, peak )
                        print("-----------------------")
                        time.sleep(2)
                    if (peak == 324.37):
                        print("+++++++++++++++++++++++")
                        print(n ,center,centerU, peak )
                        print("-----------------------")
                        time.sleep(2)

                    if (peak == 381.60):
                        print("+++++++++++++++++++++++")
                        print(n ,center,centerU, peak )
                        print("-----------------------")
                        time.sleep(2)
                    if (peak == 257.99):
                        print("+++++++++++++++++++++++")
                        print(n ,center,centerU, peak )
                        print("-----------------------")
                        ##print(center,centerU, peak )
                        time.sleep(2)

                    if (peak == 186.17):
                        print("+++++++++++++++++++++++")
                        print(n ,center,centerU, peak )
                        print("-----------------------")
                        time.sleep(2)
                    if (peak == 268.22):
                        print("+++++++++++++++++++++++")
                        print(n ,center,centerU, peak )
                        print("-----------------------")
                        time.sleep(2)


                ## not configured for intensity just yet
                intensityPerTime = totalIntensity/liveTime
                intensityPerTimeUncert = totalIntensityUncert/liveTime


                d = datetime.timedelta(seconds = realTime*0.5)
                ndateTime = dateTime + d

                try:
                    bigDict[n][peak].append([intensityPerTime, intensityPerTimeUncert, ndateTime])
                except:
                    bigDict[n][peak] = [[intensityPerTime, intensityPerTimeUncert, ndateTime]]
    return bigDict

def peakModel(x, verticalShift, b, amp, c, s):
    return [verticalShift + b * xi
    + abs(amp)*math.exp(-(xi-c)**2/(2* s**2)) for xi in x]

def getyLoc(xLoc, yData, xData):
    for index in range(0, len(xData)-1):
        if (xLoc >= xData[index] and xLoc <= xData[index+1]):
            return yData[index]



def fitPeak(xDatap, yDatap, start, end, guess=None, bounds = None, name=None):

    xData = []
    yData = []
    for index in range(len(xDatap)):
        if (xDatap[index] > start and xDatap[index] < end):
            xData.append(xDatap[index])
            yData.append(yDatap[index])

    labx = (end+start)/2.0
    print("FIT FOR PEAK", labx)
    laby = getyLoc(labx, yDatap, xDatap)
    try:
        popt, errors = curve_fit(peakModel, xData, yData, p0 = guess, bounds = bounds)
    except:
        plt.clf()
        plt.plot(xData, yData)
        plt.text(labx, laby, "HERE", color="red", fontsize=20)
        plt.title("could not fit this")
        plt.savefig("couldNotFindSTART"+str(start)+"END"+str(end)+"IND"+str(random.uniform(0,1))+".png")
        plt.clf()
        return 0, 0
    perr = np.sqrt(np.diag(errors))
    verticalShift, a, amp, c, s = popt
    print("found parameters", list(popt))
    print("uncertainties", list(perr))
    print("printing the fit")
    y_line = peakModel(xData, verticalShift,a,  amp, c, s)
    plt.clf()
    plt.text(labx, laby, "HERE", color="red", fontsize=20)
    plt.plot(xData, yData)
    plt.plot(xData, y_line)
    plt.title(name)
    plt.xlabel("bucket")
    plt.ylabel("counts")
    plt.legend(("Experimental Data","Fitted Data"))
    plt.savefig("plots//"+name+".png")
    ##plt.show()
    plt.clf()

    area = abs(amp *math.sqrt(2 *3.141) * s)
    areaUncert = (abs(perr[2])/abs(amp) + abs(perr[4])/abs(s)) * area

    return area, areaUncert, c, perr[3]
