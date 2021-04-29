# Experiment Classes for configuring experiments before running in via driver

#Imports
#   Data timestamping
import datetime

#Experiment Classes
#   DBF Calculation Experiment Setup
class dbfCalcExperimentSetup:

    def __init__(self):

        self.numSamples = 0
        self.numResetTimesLowerBound = 0
        self.numResetTimesUpperBound = 0
        self.numWcetsLowerBound = 0
        self.numWcetsUpperBound = 0
        self.utilizationLowerBound = 0
        self.utilizationUpperBound = 0
        self.fileName = 0
        self.fixedVars = 0
        self.startP = 0
        self.endP = 0
        self.deltaP = 0

#   Inflation 
class inflationExperimentSetup:

    def __init__(self):

        self.numberOfSamples = 0
        self.numResetTimesLowerBound = 0
        self.numResetTimesUpperBound = 0
        self.numWcetsLowerBound = 0
        self.numWcetsUpperBound = 0
        self.utilizationLowerBound = 0
        self.utilizationUpperBound = 0
        self.nPeriodic_lo = 0
        self.nPeriodic_hi = 0
        self.periodUpperBoundCode = 0
        self.fileName = 0
        self.checkpointFrequency = 0

class slightVariationSetup:

    def __init__(self):

        self.numResetTimesLowerBound = 0
        self.numResetTimesUpperBound = 0
        self.numWcetsLowerBound = 0
        self.numWcetsUpperBound = 0
        self.utilizationLowerBound = 0
        self.utilizationUpperBound = 0
        self.fileName = 0

# Accepts a base file name (called a prefix) and adds the preceeding data folder, postfixed date, time, and file extension
def createFileNameTimeStamp(prefix):

    #Begin with prefix
    fileName = prefix

    #Get date
    today = datetime.date.today()

    #Add formatted date
    fileName += "-" + str(today)

    #Get Time
    now = datetime.datetime.now()

    #Convert time to formatted string
    current_time = now.strftime("%H-%M-%S")

    #Add formatted time to filename
    fileName += "-" + str(current_time)

    #Append suffix
    fileName += ".csv"

    #Append directory
    fileName = "data/" + fileName

    #Return completed Filename
    return fileName

# Fills all experiments with predefined configurations and returns to caller
# <<< THIS IS WHERE EXPERIMENTS MAY BE ALTERED >>>
def initializeDbfExperiments():

    #Create Experiment Array
    exp = []
    for i in range(0,7):
        exp.append(dbfCalcExperimentSetup())

    #Experiment 0
    exp[0].numSamples = 10000
    exp[0].numResetTimesLowerBound = 1
    exp[0].numResetTimesUpperBound = 10
    exp[0].numWcetsLowerBound = -1
    exp[0].numWcetsUpperBound = -1
    exp[0].utilizationLowerBound = 1
    exp[0].utilizationUpperBound = 100
    exp[0].fileName = createFileNameTimeStamp("gfRwsMaeExpWcd0")
    exp[0].fixedVars = 0
    exp[0].startP = -1
    exp[0].endP = -1
    exp[0].deltaP = -1
    exp[0].maximumValueAtReset = 1000

    #Experiment 1
    exp[1].numSamples = 1
    exp[1].numResetTimesLowerBound = -1
    exp[1].numResetTimesUpperBound = -1
    exp[1].numWcetsLowerBound = -1
    exp[1].numWcetsUpperBound = -1
    exp[1].utilizationLowerBound = 1
    exp[1].utilizationUpperBound = 100
    exp[1].fileName = createFileNameTimeStamp("gfRwsMaeExpWcd1")
    exp[1].fixedVars = 0
    exp[1].startP = -1
    exp[1].endP = -1
    exp[1].deltaP = -1
    exp[1].maximumValueAtReset = 1000

    #Experiment 2
    exp[2].numSamples = -1
    exp[2].nRequested = -1
    exp[2].numResetTimesLowerBound = -1
    exp[2].numResetTimesUpperBound = -1
    exp[2].numWcetsLowerBound = -1
    exp[2].numWcetsUpperBound = -1
    exp[2].utilizationLowerBound = 1
    exp[2].utilizationUpperBound = 100
    exp[2].fileName = createFileNameTimeStamp("gfRwsMaeExpWcd2")
    exp[2].fixedVars = 2
    exp[2].startP = 100
    exp[2].endP = 800
    exp[2].deltaP = 100
    exp[2].maximumValueAtReset = 1000

    #Experiment 3
    exp[3].numSamples = -1
    exp[3].nRequested = -1
    exp[3].numResetTimesLowerBound = -1
    exp[3].numResetTimesUpperBound = -1
    exp[3].numResetTimesLowerBound = -1
    exp[3].numWcetsUpperBound = -1
    exp[3].utilizationLowerBound = 1
    exp[3].utilizationUpperBound = 100
    exp[3].fileName = createFileNameTimeStamp("gfRwsMaeExpWcd3")
    exp[3].fixedVars = 2
    exp[3].startP = 100
    exp[3].endP = 800
    exp[3].deltaP = 50
    exp[3].maximumValueAtReset = 1000

    #Experiment 4
    exp[4].numSamples = -1
    exp[4].numResetTimesLowerBound = 1
    exp[4].numResetTimesUpperBound = 10
    exp[4].numWcetsLowerBound = -1
    exp[4].numWcetsUpperBound = -1
    exp[4].utilizationLowerBound = 1
    exp[4].utilizationUpperBound = 100
    exp[4].fileName = createFileNameTimeStamp("gfRwsMaeExpWcd4")
    exp[4].fixedVars = 2
    exp[4].startP = 100
    exp[4].endP = 800
    exp[4].deltaP = 5
    exp[4].maximumValueAtReset = 1000

    #Experiment 6
    exp[5].numSamples = 10
    exp[5].numResetTimesLowerBound = 1
    exp[5].numResetTimesUpperBound = 10
    exp[5].numWcetsLowerBound = -1
    exp[5].numWcetsUpperBound = -1
    exp[5].utilizationLowerBound = 1
    exp[5].utilizationUpperBound = 100
    exp[5].fileName = createFileNameTimeStamp("gfRwsMaeExpWcd5")
    exp[5].fixedVars = 1
    exp[5].startP = 100
    exp[5].endP = 500
    exp[5].deltaP = 100
    exp[5].maximumValueAtReset = 1000

    #Experiment 7
    exp[6].numSamples = 10000
    exp[6].numResetTimesLowerBound = 1
    exp[6].numResetTimesUpperBound = 10
    exp[6].numWcetsLowerBound = -1
    exp[6].numWcetsUpperBound = -1
    exp[6].utilizationLowerBound = 1
    exp[6].utilizationUpperBound = 100
    exp[6].fileName = createFileNameTimeStamp("gfRwsMaeExpWcd6")
    exp[6].fixedVars = 0
    exp[6].startP = -1
    exp[6].endP = -1
    exp[6].deltaP = -1
    exp[6].maximumValueAtReset = -1

    #Return experiment array
    return exp

# Fills all inflation experiments with preconfigured data
# <<< THIS IS WHERE EXPERIMENTS MAY BE ALTERED >>>
def initializeInflationExperiments():

    #Create experiment list
    exp = []
    for i in range(0,3):
        exp.append(inflationExperimentSetup())

    #Experiment 8 - Testing with Varying Utilization [1-c_{m-1},1-c_0], larger num reset times
    exp[0].numSamples = 10000
    exp[0].numResetTimesLowerBound = 5
    exp[0].numResetTimesUpperBound = 10
    exp[0].numWcetsLowerBound = -1
    exp[0].numWcetsUpperBound = -1
    exp[0].utilizationLowerBound = 1
    exp[0].utilizationUpperBound = 100
    exp[0].maximumValueAtReset = 1000
    exp[0].minSepBetweenSuccessiveResets = 10
    exp[0].maxSepBetweenSuccessiveResets = 100
    exp[0].nPeriodic_hi = 5
    exp[0].nPeriodic_lo = 1
    exp[0].periodUpperBoundCode = -1
    exp[0].fileName = createFileNameTimeStamp("gfRwsMaeExpInf0")
    exp[0].checkpointFrequency = 100

    #Experiment 9 - Testing with Varying Utilization [1-c_{m-1},1-c_0], smaller num reset times
    exp[1].numSamples = 1000
    exp[1].numResetTimesLowerBound = 1
    exp[1].numResetTimesUpperBound = 5
    exp[1].numWcetsLowerBound = -1
    exp[1].numWcetsUpperBound = -1
    exp[1].utilizationLowerBound = 1
    exp[1].utilizationUpperBound = 100
    exp[1].maximumValueAtReset = 1000
    exp[1].minSepBetweenSuccessiveResets = 1
    exp[1].maxSepBetweenSuccessiveResets = 50
    exp[1].nPeriodic_hi = 5
    exp[1].nPeriodic_lo = 1
    exp[1].periodUpperBoundCode = -1
    exp[1].fileName = createFileNameTimeStamp("gfRwsMaeExpInf1")
    exp[1].checkpointFrequency = 100

    #Experiment 10 - Testing with Varying Utilization [1-c_{m-1},1-c_0], varied num reset times
    exp[2].numSamples = 1000
    exp[2].numResetTimesLowerBound = 1
    exp[2].numResetTimesUpperBound = 10
    exp[2].numWcetsLowerBound = -1
    exp[2].numWcetsUpperBound = -1
    exp[2].utilizationLowerBound = 1
    exp[2].utilizationUpperBound = 100
    exp[2].maximumValueAtReset = 1000
    exp[2].minSepBetweenSuccessiveResets = 1
    exp[2].maxSepBetweenSuccessiveResets = 50
    exp[2].nPeriodic_hi = 5
    exp[2].nPeriodic_lo = 1
    exp[2].periodUpperBoundCode = -1
    exp[2].fileName = createFileNameTimeStamp("gfRwsMaeExpInf2")
    exp[2].checkpointFrequency = 100

    #Return experiments array
    return exp

# Fill slight variation experiment with preconfigured values
def initializeSlightVariationExperiments():

    # Fill experiment with configuration
    exp = []
    exp.append(slightVariationSetup())

    #Experiment 11
    exp[0].numSamples = 1000
    exp[0].numResetTimesLowerBound = 1
    exp[0].numResetTimesUpperBound = 10
    exp[0].numWcetsLowerBound = -1
    exp[0].numWcetsUpperBound = -1
    exp[0].utilizationLowerBound = 1
    exp[0].utilizationUpperBound = 100
    exp[0].fileName = createFileNameTimeStamp("gfRwsMaeexpSV0")
    exp[0].checkpointFrequency = 100

    return exp