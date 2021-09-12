import math
import matplotlib.pyplot as plt
import time
import datetime
##from datetime import datetime
import pickle
import scipy.signal
import random
import numpy as np


from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition,
                                                  mark_inset)

def plotRawData(fullData, block=True, timer = None):
    data, livetime, realtime, starttime = fullData
    print("here is data", data)
    peaks, prop = scipy.signal.find_peaks(data,height=500)
    for index in range(len(peaks)):
        print("peak"+str(index)+ " :"+str(peaks[index]))

    plt.plot(data)
    for x,y in zip(peaks, prop['peak_heights']):
        plt.text(x,y,str(x),color="red",fontsize=12)

    ##plt.scatter(peaks, prop['peak_heights'],marker="x")
    plt.xlabel("Energy (Hz)")
    plt.ylabel("intensity (arb. units)")
    plt.title( "livetime :"+ str(livetime)+ " realtime: "+ str(realtime)+ " starttime: " +str(starttime) )
    plt.show(block=block)
    if (timer != None):
        plt.pause(timer)
    plt.clf()

def getyLoc(xLoc, yData, xData):
    for index in range(0, len(xData)-1):
        if (xLoc >= xData[index] and xLoc <= xData[index+1]):
            return yData[index]

def plotCalibratedData(fullData, calibrationInformation, axes, ylims, block = True, timer = None, spottedPeaks=None):
    ## spotted peaks is a dicrionary between a frequency and a string that is the name of the element that it decays with.
    gradient, _, intercept, _ = calibrationInformation
    xData, yData, livetime, realtime, starttime = fullData
    ##peaks, prop = scipy.signal.find_peaks(yData, height=0, prominence=1)
    ##peaks = [p*gradient + intercept for p in peaks]
    xData = xData
    yData = yData
    yData = [el/livetime for el in yData]
    axes.plot(xData, yData, color="red")




    for pos in list(spottedPeaks.keys()):
        yPos = getyLoc(pos, yData, xData)
        axes.text(pos, yPos+0.2, spottedPeaks[pos] , rotation=90, color="black", fontsize=15)

    ##forf x,y in zip(peaks, prop['peak_heights']):
        ##plt.text(x,y,str(x),color="red",fontsize=12)

    ##plt.scatter(peaks, prop['peak_heights'],marker="x")
    ##plt.xlabel("Energy (KeV)")
    ##plt.ylabel("Intensity (arb. units)")
    ##plt.title( "livetime :"+ str(livetime)+ " realtime: "+ str(realtime)+ " starttime: " +str(starttime) )

    plt.minorticks_on()
    axes.set_xlim(0, 150)
    ##plt.savefig("plots\livetime"+str(livetime)+"ID"+str(random.randint(0,100))+ ".png" )
    ##axes.set_xticklabels( axes.get_xticklabels(), fontSize=14)
    ##axes.set_yticklabels(ylabels, fontSize=14)
    plt.show(block=block)
    if (timer != None):
        plt.pause(timer)
    ##plt.clf()

    """
    plt.minorticks_on()
    xstart = 170
    xend = 450
    labels = [200, 250, 300, 350, 400, 450]

    if (ylims[1]==12):
        ylabels = [0, 3, 6, 9, 12]
    if (ylims[1] == 10):
        ylabels = [0, 2, 4, 6, 8, 10]
    if (ylims[1] == 6):
        ylabels = [0,  2,  4,  6]
    if (ylims[1] == 3):
        ylabels = [0,1,2,3]

    ylabels = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
    axes.set_xlim(170, 450)
    ##axes.set_xlim(290,300)
    axes.set_ylim(ylims[0],ylims[1])
    ##plt.savefig("plots\livetime"+str(livetime)+"ID"+str(random.randint(0,100))+ ".png" )
    ##axes.set_xticklabels( axes.get_xticklabels(), fontSize=14)
    ##axes.set_yticklabels(ylabels, fontSize=14)
    plt.show(block=block)
    if (timer != None):
        plt.pause(timer)
    ##plt.clf()
    """

def plotCalibratedData2(fullData, calibrationInformation, axes, ylims, block = True, timer = None, spottedPeaks=None):
    ## spotted peaks is a dicrionary between a frequency and a string that is the name of the element that it decays with.
    gradient, _, intercept, _ = calibrationInformation
    xData, yData, livetime, realtime, starttime = fullData
    ##peaks, prop = scipy.signal.find_peaks(yData, height=0, prominence=1)
    ##peaks = [p*gradient + intercept for p in peaks]
    xData = xData
    yData = yData
    yData = [el/livetime for el in yData]
    axes.plot(xData, yData, color="red")




    for pos in list(spottedPeaks.keys()):
        yPos = getyLoc(pos, yData, xData)
        axes.text(pos, yPos+0.2, spottedPeaks[pos] , rotation=90, color="black", fontsize=15)

    ##for x,y in zip(peaks, prop['peak_heights']):
        ##plt.text(x,y,str(x),color="red",fontsize=12)

    ##plt.scatter(peaks, prop['peak_heights'],marker="x")
    ##plt.xlabel("Energy (KeV)")
    ##plt.ylabel("Intensity (arb. units)")
    print("livetime :"+ str(livetime)+ " realtime: "+ str(realtime)+ " starttime: " +str(starttime))
    ##plt.title( "livetime :"+ str(livetime)+ " realtime: "+ str(realtime)+ " starttime: " +str(starttime) )

    plt.minorticks_on()
    axes.set_xlim(0, 1750)


    # Create a set of inset Axes: these should fill the bounding box allocated to
    # them.
    ax2 = plt.axes([0,0,1750,1750])
    # Manually set the position and relative size of the inset axes within ax1
    ip = InsetPosition(axes, [0.1,0.2,0.85,0.6])
    ax2.set_axes_locator(ip)
    # Mark the region corresponding to the inset axes on ax1 and draw lines
    # in grey linking the two axes.
    mark_inset(axes, ax2, loc1=2, loc2=4, fc="none", ec='0.5')


    ax2.legend(loc=0)

    # Some ad hoc tweaks.
    ax2.set_yticks(np.arange(0,20,2.5))
    ##ax2.set_xticklabels( ax2.get_xticks() , backgroundcolor='w')
    ax2.tick_params(axis='x', which='major', pad=8)



    ax2.plot(xData[800:6000], yData[800:6000], color="red")

    for pos in list(spottedPeaks.keys()):
        if (pos < 1200):
            yPos = getyLoc(pos, yData, xData)

            ax2.text(pos, yPos+0.2, spottedPeaks[pos] , rotation=90, color="black", fontsize=15)

    plt.show(block=block)
    if (timer != None):
        plt.pause(timer)
    ##plt.clf()

    """
    plt.minorticks_on()
    xstart = 170
    xend = 450
    labels = [200, 250, 300, 350, 400, 450]

    if (ylims[1]==12):
        ylabels = [0, 3, 6, 9, 12]
    if (ylims[1] == 10):
        ylabels = [0, 2, 4, 6, 8, 10]
    if (ylims[1] == 6):
        ylabels = [0,  2,  4,  6]
    if (ylims[1] == 3):
        ylabels = [0,1,2,3]

    ylabels = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
    axes.set_xlim(170, 450)
    ##axes.set_xlim(290,300)
    axes.set_ylim(ylims[0],ylims[1])
    ##plt.savefig("plots\livetime"+str(livetime)+"ID"+str(random.randint(0,100))+ ".png" )
    ##axes.set_xticklabels( axes.get_xticklabels(), fontSize=14)
    ##axes.set_yticklabels(ylabels, fontSize=14)
    plt.show(block=block)
    if (timer != None):
        plt.pause(timer)
    ##plt.clf()
    """

def rampPlot():
    fullData = getData()[1:]

    while True:
        for dataclass in fullData:
            for dataset in dataclass:
                ##data, livetime, realtime, dateTime = dataset
                plotRawData(dataset, block=False, timer =1)

def rampPlotClose(fullData, cal, spottedPeaks):
    ##fullData.reverse()
    counter = 0
    ncounter = 0
    fig, axs = plt.subplots(4)
    draw = False

    for data in fullData:
        if (counter == 1):
            ##ncounter = ncounter + 1
            draw = True
            ##ylim = [1,10]
            ylim = [0,13]
            block = False
        if (draw):
            plotCalibratedData(data, cal, axs[ncounter-1], ylim, block=block , timer = 0.1,spottedPeaks=spottedPeaks)

        _, _, _, _, starttime = data
        print("counter:", str(counter), "time:", str(starttime) )
        counter += 1

def rampPlotSimple(fullData, cal, spottedPeaks):
    ##fullData.reverse()
    counter = 0
    ncounter = 0
    fig, axs = plt.subplots(4)
    draw = False

    for data in fullData:
        if (counter == 1):
            ncounter = ncounter + 1
            draw = True
            ##ylim = [1,10]
            ylim = [0,1000]
            block = False
        if (counter == 5):
            ncounter = ncounter + 1
            draw = True
            ##ylim = [1,10]
            ylim = [0,1000]
            block = False
        if (counter == 25):
            ncounter = ncounter + 1
            draw = True
            ##ylim = [0,6]
            ylim = [0,1000]
            block = False
        if (counter == 35):
            ncounter = ncounter + 1
            draw = True
            ##ylim = [0,3]
            ylim = [0,1000]
            block = True
        if (draw):
            plotCalibratedData(data, cal, axs[ncounter-1], ylim, block=block , timer = 0.1,spottedPeaks=spottedPeaks)
            draw = False

        _, _, _, _, starttime = data
        print("counter:", str(counter), "time:", str(starttime) )
        counter += 1


def allTogetherPlot(fullData, cal, spottedPeaks):
    indexes = [1,15,40,50]
    counter = 0
    styleCounter = 0
    styles = ["-","--", "-.", ":"]
    for data in fullData:
        if (counter in indexes):
            xData = fullData[counter][0]
            yData = fullData[counter][1]
            oldMax = max(yData)
            yData = [el/oldMax for el in yData]
            plt.plot(xData, yData, linewidth=4.0, linestyle=styles[styleCounter])
            styleCounter += 1

            plt.xlim(40,100)

            delta = datetime.timedelta(minutes=22)
            plt.legend(( fullData[indexes[0]][4]+delta ,fullData[indexes[1]][4]+delta,fullData[indexes[2]][4]+delta,fullData[indexes[3]][4]+delta ), prop={'size': 20})

            if (indexes[-1] == counter):
                print("here")
                print(fullData[0][4])
                plt.xlabel("KeV", fontsize=20)
                plt.ylabel("Normalised Counts", fontsize=20)
                plt.show(block=True)
        counter += 1



def plotAFullSpectra(fullData, cal, spottedPeaks, index):
    fig, axs = plt.subplots(1)
    ylim = [0,150]
    plotCalibratedData(fullData[index], cal, axs ,  ylim, block=True, timer= 0.1, spottedPeaks = spottedPeaks)




def getPeaks(dataSet):
    data, _, _, _

def getData():
    return pickle.load(open("formattedData.p","rb"))
