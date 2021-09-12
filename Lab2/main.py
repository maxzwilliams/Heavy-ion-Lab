from plotting import *
from calibrate import *
from fitPeak import *
from IntensityCal import *
import pickle
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
from uncertainties import ufloat

from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition,
                                                  mark_inset)

print("now doing")
calibratedData, gradient, gradientUncert, inter, interunc, xDataEu, rDataEu,xDataBa, rDataBa  = getCalibratedData()




print("starting intensity calibration")
m, mUncert, b, bUncert = intCal(xDataEu, rDataEu, xDataBa, rDataBa)
print("Intensity calibrated with parameters", m, mUncert, b, bUncert)

## equation for effeciency is something like
## \eta = exp((m \pm mUncert) frequency + (b \pm bUncert))
print("DONE CALIBRATING THE INTENSITIES")
callibrationInformation = gradient, gradientUncert, inter, interunc
names = dict()


## 192 chain
##Tl
##names[422.8]="$^{192}Tl$" ## this works provided that we restrict the domain of fitting to \pm 3

##Hg
##names[274.8] = "$^{192}Hg$" ## fine with \pm 10

##Au
##names[316.50791]="$^{192}Au$" ## fine with \pm 6



## The 193 chain
## Tl
#names[324.37]="$^{193}Tl$" ## good with 6
##names[343.99]="$^{193}Tl$" ## good with 6

## Hg
names[381.60]="$^{193}Hg$" ## good with 6
names[861.11]="$^{193}Hg$" ## good with 6
names[257.99] = "$^{193}Hg$" ## dont know what it is good with

## Au
##names[186.17]="$^{193}Au$" ## good with 6
##names[255.57]="$^{193}Au$" ## good with 6

#names[268.22] = "$^{193}Au$"




## these are our accepted ones

## 192 chain ones
names[422.8]="$^{192}Tl$"
names[634.8]="$^{192}Tl$"
names[786.3]="$^{192}Tl$"
names[745.5]="$^{192}Tl$"
names[174.0]="$^{192}Tl$" ## new one added here

names[274.8] = "$^{192}Hg$"
names[381.6] = "$^{193}Hg$"

names[316.50791]= "$^{192}Au$"
names[295.95827 ]= "$^{192}Au$"


## 193 chain ones
names[324.37]="$^{193}Tl$"
names[343.99]="$^{193}Tl$" ## good for I checking
names[1044.7]="$^{193}Tl$"
names[676.10]="$^{193}Tl$" ## good for I checking
names[1579.3]="$^{193}Tl$"
names[335.11]="$^{193}Tl$"
names[284.89]="$^{193}Tl$" ## good for I checking
names[692.3]="$^{193}Tl$"


## cannot get this to work
names[381.60]="$^{193}Hg$" ## good
names[861.11] = "$^{193}Hg$" ## good
names[257.99] = "$^{193}Hg$" ## good
names[1118.84] = "$^{193}Hg$" ## good
names[789.21] = "$^{193}Hg$" ## nah

## only one point isnt very good
names[186.17]="$^{193}Au$" ## good
names[255.57]="$^{193}Au$" ## no
names[268.22] = "$^{193}Au$" ## no
names[173.52] = "$^{193}Au$" ## no

names[365.2]="$^{193m}Tl$"



## 194 chain ones
names[428.0]="$^{194}Tl$"
names[636.5]="$^{194}Tl$"
names[645.20] = "$^{194}Tl$"
"""
names[428]="$^{194m}Tl$"
names[636.5]="$^{194m}Tl$"
names[748.9]="$^{194m}Tl$"
names[734.8]="$^{194m}Tl$"

names[257.99] = "$^{193m}Hg$"
names[407.63] = "$^{193m}Hg$"
names[573.25] = "$^{193m}Hg$"
names[257.99] = "$^{193m}Hg$"

names[257.99]="$^{193m}Au$"
names[219.75]="$^{193m}Au$"
names[252.5]=".$^{191m}Au$"
"""



## Here I will show the locations of some of the peaks match those those from lund
## I will use the dictionary names that I have already defined

## I will use the 193 chain. One sample from all the components.



##plotAFullSpectra(calibratedData, callibrationInformation, names, 10)
##rampPlotSimple(calibratedData, callibrationInformation, spottedPeaks=names)
allTogetherPlot(calibratedData, callibrationInformation, spottedPeaks=names)
## Here we do the fitting for some of the peaks
## I have to pick a specific chain which I want to look at

## we will look at only the chain names here
cnames = dict()

##for key in list(names.keys()):
    ##if ("192^TL" in names[key] or "192^Hg" in names[key] or "192^Au" in names[key]):
    ##cnames[key] = names[key]




## comment this back in if I want to save to pickle.
"""
intensities = fitAll(calibratedData, names)
for key in list(intensities.keys()):
    for key2 in list(intensities[key].keys()):
        print("isotope", key, "peakLocation", key2, "results", intensities[key][key2])
        ## here I want to generate the data that we want to plot
        startTime = intensities[key][key2][0][2]
        xData = [intensities[key][key2][i][0] for i in range(len(intensities[key][key2]))]
        xDataUncert = [intensities[key][key2][i][1] for i in range(len(intensities[key][key2]))]
        tData = [(intensities[key][key2][i][2]-startTime).total_seconds() for i in range(len(intensities[key][key2]))]
        ##plt.errorbar(tData, xData, xerr=None, yerr=None)
        plt.scatter(tData, xData)
        plt.title("isotope "+str(key)+ " peakLocation "+ str(key2))
        plt.savefig("big ol plot")

        fileName = "PData//isotope|"+str(key)+"|peakLocation|"+ str(key2) +"|results.pickle"
        with open(fileName, 'wb') as f:
            pickle.dump([tData, xData, xDataUncert], f)
##plt.show()
"""








def pickleIntensitiesOfNames(names, calibratedData):
    intensities = fitAll(calibratedData, names)
    for key in list(intensities.keys()):
        for key2 in list(intensities[key].keys()):
            ##print("isotope", key, "peakLocation", key2, "results", intensities[key][key2])
            ## here I want to generate the data that we want to plot
            startTime = intensities[key][key2][0][2]
            xData = [intensities[key][key2][i][0] for i in range(len(intensities[key][key2]))]
            xDataUncert = [intensities[key][key2][i][1] for i in range(len(intensities[key][key2]))]
            tData = [(intensities[key][key2][i][2]-startTime).total_seconds() for i in range(len(intensities[key][key2]))]
            ##plt.errorbar(tData, xData, xerr=None, yerr=None)
            plt.scatter(tData, xData)
            plt.title("isotope "+str(key)+ " peakLocation "+ str(key2))
            plt.savefig("big ol plot")

            fileName = "NData//isotope|"+str(key)+"|peakLocation|"+ str(key2) +"|results.pickle"
            with open(fileName, 'wb') as f:
                pickle.dump([tData, xData, xDataUncert], f)
            plt.show()
        print("startTime", startTime)
        ##time.sleep(5)


##pickleIntensitiesOfNames(names, calibratedData)





## now lets gather and plot everything
def plotChain192():

    names = []
    names.append("PData//isotope|$^{192}Tl$|peakLocation|422.8|results.pickle")
    names.append("PData//isotope|$^{192}Hg$|peakLocation|274.8|results.pickle")
    names.append("PData//isotope|$^{192}Au$|peakLocation|316.50791|results.pickle")

    data = []
    for file in names:
        with open(file, 'rb') as f:
            data.append(pickle.load(f))
    plt.clf()
    counter = 0
    pointsIncluded = 50
    data.reverse()
    for d in data:
        if (counter == 2):
            pointsIncluded = 21
        tData = d[0][0:pointsIncluded]
        yData = d[1][0:pointsIncluded]
        yDataUncert = d[2][0:pointsIncluded]
        if (counter == 0):
            marker="v"
            color="r"
        if (counter == 1):
            marker="^"
            color = "b"
        if (counter == 2):
            marker="s"
            color = "g"
        plt.errorbar(tData, yData, xerr=None, yerr=None, linestyle='None', markersize = 6, marker=marker, color=color)
        counter += 1
        Au192 = mlines.Line2D([], [], color='red', marker='v', linestyle='None',
                          markersize=10, label='$^{192}Au$')
        Hg192 = mlines.Line2D([], [], color='blue', marker='^', linestyle='None',
                          markersize=10, label='$^{192}Hg$')
        Tl192 = mlines.Line2D([], [], color='green', marker='^', linestyle='None',
                          markersize=10, label='$^{192}Tl$')
    plt.xlabel("Time (seconds)", fontsize=16)
    plt.ylabel("Intensity (arb. units)", fontsize=16)
    plt.legend(handles=[Au192, Hg192, Tl192], prop={'size': 20})

    plt.show()

## now lets gather and plot everything
def plotChain193():

    names = []
    ##names.append("PData//isotope|$^{193}Tl$|peakLocation|343.99|results.pickle")
    names.append("PData//isotope|$^{193}Tl$|peakLocation|324.37|results.pickle") ## testing


    names.append("PData//isotope|$^{193}Hg$|peakLocation|861.11|results.pickle") ## testing


    names.append("PData//isotope|$^{193}Hg$|peakLocation|257.99|results.pickle")

    ## the old golds
    ##names.append("PData//isotope|$^{193}Au$|peakLocation|186.17|results.pickle")
    ##names.append("PData//isotope|$^{193}Au$|peakLocation|255.57|results.pickle")

    ## the new one gold
    names.append("PData//isotope|$^{193}Au$|peakLocation|268.22|results.pickle")
    ##names.append("PData//isotope|$^{193}Au$|peakLocation|268.22|results.pickle")


    data = []
    for file in names:
        with open(file, 'rb') as f:
            data.append(pickle.load(f))
    plt.clf()
    counter = 0
    pointsIncluded = 50
    fig, ax1 = plt.subplots()

    # Create a set of inset Axes: these should fill the bounding box allocated to
    # them.
    ax2 = plt.axes([0,0,1000,1000])
    # Manually set the position and relative size of the inset axes within ax1
    ip = InsetPosition(ax1, [0.4,0.2,0.5,0.5])
    ax2.set_axes_locator(ip)
    # Mark the region corresponding to the inset axes on ax1 and draw lines
    # in grey linking the two axes.
    mark_inset(ax1, ax2, loc1=2, loc2=4, fc="none", ec='0.5')


    ax2.legend(loc=0)

    # Some ad hoc tweaks.
    ax2.set_yticks(np.arange(0,20,2.5))
    ##ax2.set_xticklabels( ax2.get_xticks() , backgroundcolor='w')
    ax2.tick_params(axis='x', which='major', pad=8)




    for d in data:
        tData = d[0][0:pointsIncluded]
        yData = d[1][0:pointsIncluded]

        yDataUncert = d[2][0:pointsIncluded]
        if (counter == 3):
            for index in range(0, 20):
                yDataUncert[index] = 0
        if (counter == 0):
            marker="v"
            color="r"
        if (counter == 1):
            marker="^"
            color = "g"
        if (counter == 2):
            marker="^"
            color = "y"
        if (counter == 3):
            marker="s"
            color = "black"
        if (counter == 4):
            marker = "s"
            color = "purple"

        if ( counter == 3):
            yData = [el*10 for el in yData]
        if (counter == 1):
            yData = [el*10 for el in yData]

        ax2.errorbar(tData[0:15], yData[0:15], xerr=None, yerr=yDataUncert[0:15], linestyle='None', markersize = 6, marker=marker, color=color)
        ax1.errorbar(tData, yData, xerr=None, yerr=yDataUncert, linestyle='None', markersize = 6, marker=marker, color=color)


        ##ax2.errorbar(tData[0:15], yData[0:15], xerr=None, yerr=None, linestyle='None', markersize = 6, marker=marker, color=color)
        ##ax1.errorbar(tData, yData, xerr=None, yerr=None, linestyle='None', markersize = 6, marker=marker, color=color)


        counter += 1
        TL193= mlines.Line2D([], [], color='red', marker='v', linestyle='None',
                          markersize=10, label="$^{193}Tl$")
        TL193Num2= mlines.Line2D([], [], color='blue', marker='v', linestyle='None',
                          markersize=10, label='$^{193}Tl$')
        HG193 = mlines.Line2D([], [], color='green', marker='^', linestyle='None',
                          markersize=10, label='$^{193}Hg$')
        HG193Num2 = mlines.Line2D([], [], color='yellow', marker='^', linestyle='None',
                              markersize=10, label='$^{193}Hg$')

        Au193 = mlines.Line2D([], [], color='black', marker='s', linestyle='None',
                          markersize=10, label='$^{193}Au$')

        Au193Num2 = mlines.Line2D([], [], color='purple', marker='s', linestyle='None',
                          markersize=10, label='$^{193}Au$')

    ax1.set_xlabel("Time (seconds)", fontsize=20)
    ax1.set_ylabel("Intensity (arb. units)", fontsize=20)

    ax1.legend(handles=[TL193, HG193, HG193Num2, Au193 ], prop={'size': 20})

    plt.show()


def linearModel(x, m, b):
    return [m*xi + b for xi in x]

def quickLinearFit(xData, yData, indexesUsed):
    uxData = [xData[i] for i in indexesUsed]
    uyData = [yData[i] for i in indexesUsed]
    popt, errors = curve_fit(linearModel, uxData, uyData)
    perr = np.sqrt(np.diag(errors))
    m, b = popt
    newYData = linearModel(xData, m, b)

    m =  round(m, 4 - int(math.floor(math.log10(abs(m)))) - 1)
    perr[0] =  round(perr[0] , 4 - int(math.floor(math.log10(abs(perr[0] )))) - 1)
    return m, perr[0], b, perr[1], newYData




def plotChain193Linear():
    names = []
    ##names.append("PData//isotope|$^{193}Tl$|peakLocation|343.99|results.pickle")
    names.append("PData//isotope|$^{193}Tl$|peakLocation|324.37|results.pickle") ## testing


    names.append("PData//isotope|$^{193}Hg$|peakLocation|861.11|results.pickle") ## testing


    names.append("PData//isotope|$^{193}Hg$|peakLocation|257.99|results.pickle")

    ## the old golds
    ##names.append("PData//isotope|$^{193}Au$|peakLocation|186.17|results.pickle")
    ##names.append("PData//isotope|$^{193}Au$|peakLocation|255.57|results.pickle")

    ## the new one gold
    names.append("PData//isotope|$^{193}Au$|peakLocation|268.22|results.pickle")
    ##names.append("PData//isotope|$^{193}Au$|peakLocation|268.22|results.pickle")


    data = []
    for file in names:
        with open(file, 'rb') as f:
            data.append(pickle.load(f))
    plt.clf()
    counter = 0
    pointsIncluded = 50
    fig, ax1 = plt.subplots()
    ax1.set_ylim(-10, 5)

    # Create a set of inset Axes: these should fill the bounding box allocated to
    # them.
    ##ax2 = plt.axes([0,0,5,5])
    # Manually set the position and relative size of the inset axes within ax1
    ##ip = InsetPosition(ax1, [0.5,0.1,0.3,0.4])
    ##ax2.set_axes_locator(ip)
    # Mark the region corresponding to the inset axes on ax1 and draw lines
    # in grey linking the two axes.
    ##mark_inset(ax1, ax2, loc1=3, loc2=1, fc="none", ec='0.5')


    ##ax2.legend(loc=0)

    # Some ad hoc tweaks.
    ##ax2.set_yticks(np.arange(-10, 20, 2.5))
    ##ax2.set_xticklabels( ax2.get_xticks() , backgroundcolor='w')
    ##ax2.tick_params(axis='x', which='major', pad=8)

    stats = dict()
    for index in range(10):
        stats[index] = ""
    for d in data:
        if (counter == 3):
            tData = d[0][19:pointsIncluded]
            yData = d[1][19:pointsIncluded]
        else:
            tData = d[0][0:pointsIncluded]
            yData = d[1][0:pointsIncluded]

        if (counter == 0):
            include = [i for i in range(0, 13)]
        if (counter == 1):
            include = [i for i in range(16, len(tData))]
        if (counter == 2):
            include = [i for i in range(15, 25)]
        if (counter == 3):
            include = [i for i in range(len(tData)-7, len(tData))]

        loggedyData = [math.log(el) for el in yData]



        m, mu, b, bu, modYData = quickLinearFit(tData, loggedyData, include)
        print("counter " +  str(counter))
        print("m " + str(m))
        print("mu " + str(mu))
        bigm = ufloat(-m, mu)
        bigLog2 = ufloat(math.log(2), 0)
        print("half life: " + str(bigLog2/bigm) + "s")
        stats[counter] = "half life: " + str(bigLog2/bigm) + "s"
        yDataUncert = d[2][0:pointsIncluded]
        loggedyDataUncert = [yDataUncert[j]/yData[j] for j in range(len(yData))]
        if (counter == 0):
            marker="v"
            color="r"
        if (counter == 1):
            marker="^"
            color = "g"
        if (counter == 2):
            marker="^"
            color = "y"
        if (counter == 3):
            marker="s"
            color = "black"
        if (counter == 4):
            marker = "s"
            color = "purple"
        if (counter == 1 or counter == 2):
            yData = [el*5 for el in yData]

        ##ax2.errorbar(tData, modYData, err=None, yerr = None, color=color)
        ##ax2.errorbar(tData, loggedyData, xerr=None, yerr=None, linestyle='None', markersize = 6, marker=marker, color=color)
        ##ax2.errorbar(tData[0:20], modYData[0:20], err=None, yerr = None, color=color)
        ##ax2.errorbar(tData[0:20], loggedyData[0:20], xerr=None, yerr=None, linestyle='None', markersize = 6, marker=marker, color=color)
        if (counter == 3):
            ax1.errorbar(tData, loggedyData, xerr = None, yerr = None, linestyle='None', markersize = 6, marker=marker, color=color)
        else:
            ax1.errorbar(tData, loggedyData, xerr = None, yerr = loggedyDataUncert, linestyle='None', markersize = 6, marker=marker, color=color)
        ax1.errorbar(tData, modYData, err = None, yerr = None, color=color)

        TL193= mlines.Line2D([], [], color='red', marker='v', linestyle='None',
                          markersize=10, label="$^{193}Tl$  half life: $1413 \pm 42$ s" )
        TL193Num2= mlines.Line2D([], [], color='blue', marker='v', linestyle='None',
                          markersize=10, label='$^{193}Tl$  ')
        HG193 = mlines.Line2D([], [], color='green', marker='^', linestyle='None',
                          markersize=10, label='$^{193}Hg$ half life: $(1.257 \pm 0.092) \\times 10^{4}$ s' )
        HG193Num2 = mlines.Line2D([], [], color='yellow', marker='^', linestyle='None',
                              markersize=10, label="$^{193}Hg$ "+"half life: " + "$(1.53 \pm 0.25) \\times 10^{4}$" + " s")

        Au193 = mlines.Line2D([], [], color='black', marker='s', linestyle='None',
                          markersize=10, label='$^{193}Au$ half life: '+"$(6.7 \pm 2.8) \\times 10^{4} $" + " s")

        Au193Num2 = mlines.Line2D([], [], color='purple', marker='s', linestyle='None',
                          markersize=10, label='$^{193}Au$  '+stats[3])
        counter += 1

    ax1.set_xlabel("Time (seconds)", fontsize=20)
    ax1.set_ylabel("Log of Intensity (arb. units)", fontsize=20)

    ax1.legend(handles=[TL193, HG193, HG193Num2, Au193 ], prop={'size': 16}, loc='upper right')

    plt.show()



## okay these work
##plotChain192()
##plotChain193Linear()
##plotChain193()
plotChain193Linear()

def claibrationFunction(energy,  m, mUncert, b, bUncert):
    rtn = ((energy)**(m)) * math.exp(b)
    rtn1 = (energy)**(m+mUncert) * math.exp(b+bUncert)
    rtn2 = (energy)**(m+mUncert) * math.exp(b-bUncert)
    rtn3 = (energy)**(m-mUncert) * math.exp(b+bUncert)
    rtn4 = (energy)**(m-mUncert) * math.exp(b-bUncert)
    return rtn, (max([rtn1,rtn2,rtn3,rtn4])-min([rtn1,rtn2,rtn3,rtn4]))/2



## Now all I have to do is make sure that the relative peak strengths make sense
## lets try chain 193 first
import os
def IntensityCheck(nameString, m, mUncert, b, bUncert, percentDict):
    ## loop over all the files that have 193Tl in their name and print them out
    directory = r'NData'
    energiesToData = dict()
    for fileName in os.listdir(directory):
        if (nameString in str(fileName)):
            energy = str(fileName).split("|")[3]
            with open(os.path.join(directory, fileName), 'rb') as f:
                energiesToData[energy] = pickle.load(f)
                timeLength = len(energiesToData[energy][0])

    ## I want at each time, the set of intensities for all the peaks
    fullData =  [ [0 for i in range(len(list(energiesToData.keys())))] for t in range(timeLength)]
    fullDataUncerts = [ [0 for i in range(len(list(energiesToData.keys())))] for t in range(timeLength)]
    energiesToDataKeys = list(energiesToData.keys())
    energiesToDataKeys.sort()

    for energyIndex in range(len(energiesToData.keys())):
        for timeIndex in range(timeLength):
            energy = energiesToDataKeys[energyIndex]
            ## this is wrong, the calibration function gives the effeciency, not the calibrated intensity
            eff, _ = claibrationFunction(float(energy), m, mUncert, b, bUncert)
            ##print(claibrationFunction(200, 0, m, mUncert, b, bUncert))
            fullData[timeIndex][energyIndex] = energiesToData[energy][1][timeIndex]/(percentDict[float(energy)]*eff)
            fullDataUncerts[timeIndex][energyIndex] = energiesToData[energy][2][timeIndex]/(percentDict[float(energy)]*eff)

    for time in range(timeLength):
        ##plt.xlim(250, 700)
        ##plt.axes.Axes.set_xscale(1, 'linear')
        print(energiesToDataKeys)
        print(fullData[time])
        energiesToDataKeys = [float(el) for el in energiesToDataKeys]


        plt.errorbar(energiesToDataKeys, fullData[time], xerr = None, yerr = fullDataUncerts[time], linestyle="None", markersize=6, marker="s")
        plt.plot([int(min(energiesToDataKeys))-50, int(min(energiesToDataKeys)), int(max(energiesToDataKeys))+50], [np.average(fullData[time]) for i in fullData[time]], color="red")
        plt.xlabel("Energy (keV)", fontsize=16)
        plt.ylabel(r'$\frac{I_0}{\eta I_{p}}$',fontsize=20)
        plt.legend(("Common Line","$^{193}Tl$"))

        for index in range(len(energiesToDataKeys)):
            plt.text(energiesToDataKeys[index], fullData[time][index]+0.5, str(energiesToDataKeys[index]), color="black", fontsize=12)

        plt.show()

Tl193Dict = dict()
Tl193Dict[324.37] = 100
Tl193Dict[1044.7] = 59
Tl193Dict[676.10] = 48
Tl193Dict[1579.3] = 45
Tl193Dict[343.99] = 41.7
Tl193Dict[335.11] = 26.1
Tl193Dict[284.89] = 21.6
Tl193Dict[692.3] = 20.9



Hg193Dict = dict()

Hg193Dict[381.60] = 16
Hg193Dict[861.11] = 12.4
Hg193Dict[257.99] = 9.0
Hg193Dict[1118.84] = 8.0
Hg193Dict[789.21] = 4.5


Au193Dict = dict()
Au193Dict[186.17] = 9.4
Au193Dict[255.57] = 6.2
Au193Dict[268.22] = 3.6







IntensityCheck("193^TL",m, mUncert, b, bUncert, Tl193Dict)
