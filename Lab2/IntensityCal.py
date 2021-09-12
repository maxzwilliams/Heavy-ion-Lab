"""
File for calibrating the intensitiy of peaks
"""

from scipy.optimize import curve_fit
import numpy as np
import math
import matplotlib.pyplot as plt
from plotting import *


def intCal(xDataEu, yDataEu, xDataBa, yDataBa):
    ## Locations for peaks
    peakLocationsEu = [121.7817, 344.2785   , 1408.006    , 964.079,1112.074,778.9040,1085.869,244.6975,867.378,443.965,411.1163
    ,1299.140,1212.948]
    PeakPercentagesEu = [28.58 , 26.5       ,21.005       ,14.605   ,13.644 ,	12.942 ,10.207  ,7.583   ,4.245  ,2.821  ,2.234
    ,1.623   ,1.422]

    peakLocationsBa =   [356.017, 80.9971,302.853, 276.398, 53.161]
    PeakPercentagesBa = [62.05  ,   34.06,18.33  ,   7.164, 2.199]

    decaysPerTimeEu = 18116.92
    decaysPerTimeBa = 13725.48
    timeEu = 315.4
    timeBa = 603.373333
    ## num emitted
    numEmittedEu = [decaysPerTimeEu * i/100 * timeEu for i in PeakPercentagesEu]
    numEmittedBa  = [decaysPerTimeBa * i/100 * timeBa for i in PeakPercentagesBa]
    areasEu = []
    areasBa = []
    areasUncertEu = []
    areasUncertBa = []
    effEu = []
    effBa = []

    for peak in peakLocationsEu:
        start = peak - 10
        end = peak + 10
        print("fitting Eu")
        area, uncert = fitPeak(xDataEu, yDataEu, start, end)
        areasEu.append(area)
        areasUncertEu.append(uncert)

    for peak in peakLocationsBa:
        start = peak - 5
        end = peak + 5
        print("fitting Ba")
        area, uncert = fitPeak(xDataBa, yDataBa, start, end)
        areasBa.append(area)
        areasUncertBa.append(uncert)

    effEu = [areasEu[i]/numEmittedEu[i] for i in range(len(areasEu))]
    effBa = [areasBa[i]/numEmittedBa[i] for i in range(len(areasBa))]

    effUncertEu = [areasUncertEu[i]/numEmittedEu[i] for i in range(len(areasEu))]
    effUncertBa = [areasUncertBa[i]/numEmittedBa[i] for i in range(len(areasBa))]

    peakLocations = peakLocationsEu
    peakLocations.extend(peakLocationsBa)
    eff = effEu
    eff.extend(effBa)

    effUncert = effUncertEu
    effUncert.extend(effUncertBa)

    ##peakLocations = [math.log(p) for p in peakLocations]
    ##eff = [math.log(f) for f in eff]
    ##effUncert =[math.log(f) for f in effUncert]
    plt.errorbar(peakLocations, eff, xerr = None, yerr = None, linestyle ="None", markersize = 6, marker="v")
    plt.title("effeciency data (raw)")
    plt.show()


    ## equation for calibration is something like
    ## \eta = exp(-1.4588/1.1523) f^(1.1523)
    m, mUncert, b, bUncert = fitExpCalibrationCurve(peakLocations, eff)
    return m, mUncert, b, bUncert

def lineModel(x, m, b):
    return [m*xi + b for xi in x]

def fitExpCalibrationCurve(peakLocations, eff):
    peakLocations = [math.log(p) for p in peakLocations]
    eff = [math.log(ef) for ef in eff]

    popt,errors = curve_fit(lineModel, peakLocations, eff)
    perr = np.sqrt(np.diag(errors))

    m, b = popt
    print("found parameters", list(popt))
    print("uncertainties", list(perr))

    print("printing the fit")

    y_line = lineModel(peakLocations, m, b)
    plt.clf()
    plt.plot(peakLocations, y_line)
    plt.scatter(peakLocations, eff)
    plt.show()
    plt.clf()

    return m, perr[0], b, perr[1]




## We have the locations of each of the peaks,
## we want to look at the spectrum and get the areas of each one

def peakModel(x, amp, center, std, backC, backG):
    return [abs(amp)*math.exp(-(xi-center)**2/(2*std**2)) + backC + backG*xi for xi in x ]


def fitPeak(xData, yData, start, end, guess = None):
    guess = [max(yData), (start+end)/2, 2, 100, -0.001]
    nxData = []
    nyData = []
    for index in range(len(xData)):
        if (xData[index] > start and xData[index] < end):
            nxData.append(xData[index])
            nyData.append(yData[index])
    xData = nxData
    yData = nyData

    popt, errors = curve_fit(peakModel, xData, yData, p0 = guess)
    perr = np.sqrt(np.diag(errors))
    amp, center, std, backC, backG = popt
    print("found parameters", list(popt))
    print("uncertainties", list(perr))
    print("printing the fit")
    y_line = peakModel(xData, amp, center, std, backC, backG)
    plt.clf()
    plt.plot(xData, yData)
    plt.plot(xData, y_line)
    plt.title("fitted peak")
    plt.xlabel("bucket")
    plt.ylabel("counts")
    plt.legend(("Experimental Data","Fitted Data"))
    ##plt.show()
    plt.clf()

    area = abs(amp)*math.sqrt(2*3.141)*abs(std)
    areaUncert = (abs(perr[0])/abs(amp) + abs(perr[2])/abs(std)) * area
    return area, areaUncert
