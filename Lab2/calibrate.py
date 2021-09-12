"""
File for calibrating the data
"""
from scipy.optimize import curve_fit
import numpy as np
import math
import matplotlib.pyplot as plt
from plotting import *

## we want to be able to get the location of a peak

def peakModel(x, verticalShift, amp, c, s):
    return [verticalShift
    + amp*math.exp(-(xi-c)**2/(2* s**2)) for xi in x]

def fitPeak(data, start, end, guess=None):
    xData = []
    yData = []
    for index in range(len(data)):
        if (index > start and index < end):
            xData.append(index)
            yData.append(data[index])

    popt, errors = curve_fit(peakModel, xData, yData, p0 = [100, 1000, (start+end)/2.0, 8])
    perr = np.sqrt(np.diag(errors))
    verticalShift, amp, c, s = popt
    print("found parameters", list(popt))
    print("uncertainties", list(perr))
    print("printing the fit")
    y_line = peakModel(xData, verticalShift, amp, c, s)
    plt.clf()
    plt.plot(xData, yData)
    plt.plot(xData, y_line)
    plt.title("fitted peak")
    plt.xlabel("bucket")
    plt.ylabel("counts")
    plt.legend(("Experimental Data","Fitted Data"))
    ####plt.show()
    plt.clf()

    return c, perr[2]


def lineModel(x, a, b):
    return [a*xi + b for xi in x]

def fitLine(xData, yData):
    popt, errors = curve_fit(lineModel, xData, yData)
    perr = np.sqrt(np.diag(errors))
    a, b = popt
    print("found parameters", list(popt))
    print("uncertainties", list(perr))
    print("printing the fit")
    y_line = lineModel(xData, a, b)
    plt.clf()
    plt.scatter(xData, yData)
    plt.scatter(xData, y_line)
    plt.title("Calibration Fitting")
    plt.xlabel("Buckets")
    plt.ylabel("Frequency")
    plt.legend(("Raw Data","Fitted Data"))
    ##plt.show()
    plt.clf()
    return a, perr[0], b, perr[1]

def cal():
    print("RUNNING CAL")
    ## Here we calibrate to the Eu peaks
    data = getData()[0][0]
    rData, _,_,_ = data
    ##plt.plot(rData)
    ######plt.show()
    guessedlocations = [551, 1118, 1575, 3580, 6480]
    tlocations = []
    tuncerts = []
    realLocations = [121.78, 244.70, 344.28, 778.915, 1408.01]
    for l in guessedlocations:
        val, unc = fitPeak(rData, l-15, l+15)
        tlocations.append(val)
        tuncerts.append(unc)

    ## then lets calibrate to the Ba peaks
    print("CALIBRATING BA")
    data = getData()[0][1]
    rData, _ ,_, _ = data


    newRealLocations = [356.017, 80.997, 302.853, 276.398,  79.6139, 53.161, 160.613, 223.234]
    realLocations.extend(newRealLocations)
    guessedlocations = [1/(0.2180) * el - 5 for el in newRealLocations]

    print("guessedlocations", guessedlocations)
    plt.plot(rData)
    ####plt.show()
    for l in guessedlocations:
        val, unc = fitPeak(rData, l-15, l+15)
        print("new real location ", val)
        tlocations.append(val)
        tuncerts.append(unc)
    convFactor, convUnc, inter, interunc = fitLine(tlocations, realLocations)
    print("convFactor, convUnc", convFactor, convUnc)
    print("DONEDONEDONE")
    return convFactor, convUnc, inter, interunc



def getCalibratedData():
    ## this function gets frequency calibrated data
    convFactor, convUnc, inter, interunc = cal()
    bigData = getData()[1:]
    newBigData = []
    ## okay we need to generate calibrated data
    for dataSet in bigData:
        for data in dataSet:
            yData, livetime, realtime, dateTime = data
            xData = [index * convFactor + inter for index in range(len(yData))]
            nData = xData, yData, livetime, realtime, dateTime
            newBigData.append(nData)



    spectrum = getData()[0][0]
    rDataEu, _, _ ,_  = spectrum
    xDataEu = [convFactor * xi + inter for xi in range(len(rDataEu))]
    plt.plot(xDataEu, rDataEu)
    plt.xlabel("Energy (Kev)", fontsize = 30)
    plt.ylabel("Intensity (arb. units)", fontsize = 30)

    ## Here we want to label the peaks in the data
    xlocs = [121.78, 244.70, 344.28, 778.915, 1408.01]
    ylocs = []
    for el in xlocs:

        for correctEl in xDataEu:
            if (correctEl >= el):
                el = correctEl
                break;
        index = xDataEu.index(el)
        ylocs.append(rDataEu[index])


    for x,y in zip(xlocs, ylocs):
        plt.text(x,y,str(x),color="red",fontsize=12)
    #plt.show()


    spectrum = getData()[0][1]
    rDataBa, _, _ ,_  = spectrum
    xDataBa = [convFactor * xi + inter for xi in range(len(rDataBa))]
    plt.plot(xDataBa[0:2500], rDataBa[0:2500])


    ## Here we want to label the peaks in the data
    xlocs = [356.017, 80.997, 302.853, 276.398,  79.6139, 53.161, 160.613, 223.234]
    ylocs = []
    for el in xlocs:

        for correctEl in xDataEu:
            if (correctEl >= el):
                el = correctEl
                break;
        index = xDataEu.index(el)
        ylocs.append(rDataEu[index])


    for x,y in zip(xlocs, ylocs):
        plt.text(x,y,str(x),color="red",fontsize=12)

    ###plt.show()
    return newBigData, convFactor, convUnc, inter, interunc, xDataEu, rDataEu,xDataBa, rDataBa
