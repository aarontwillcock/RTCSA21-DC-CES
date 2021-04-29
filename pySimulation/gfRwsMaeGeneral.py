# Generic Function RWS MAE General Functions

#Imports

#Deepcopy
import copy

#Floor, Ceil, etc.
import math

#PRNG
import random

#Switched Control System Classes
import gfClasses as GFC
import gfRwsMaeTool as GFRWSMAE_TOOL
import gfRwsMaeGeneral as GF_RWS_MAE_GEN

def generateRandomRwsMaeTask(
    numResetTimesLowerBound,
    numResetTimesUpperBound,
    numWcetsLowerBound,
    numWcetsUpperBound,
    utilizationLowerBound,
    utilizationUpperBound,
    maximumValueAtReset,
    minSepBetweenSuccessiveResets,
    maxSepBetweenSuccessiveResets):

    #Establish bounds on minimum and maximum spacing between successive reset times
    minimumSeparationBetweenSuccessiveResetTimes = minSepBetweenSuccessiveResets
    maximumSeparationBetweenSuccessiveResetTimes = maxSepBetweenSuccessiveResets

    #If numResetTimesLowerBound or numResetTimesUpperBound are incorrect or incompatible...
    if(numResetTimesLowerBound <= 0 or numResetTimesUpperBound < numResetTimesLowerBound):

        #Establish default range
        numResetTimesLowerBound = 1
        numResetTimesUpperBound = 10

    #Force period to 1
    p = 1

    #If numWcets bounds are incorrect or incompatible...
    if(numWcetsLowerBound <= 0 or numResetTimesUpperBound < numWcetsLowerBound):

        #Establish default range
        numWcetsLowerBound = 1
        numWcetsUpperBound = 10

    #Select number of WCETs
    m = random.randint(numWcetsLowerBound,numWcetsUpperBound)

    #Instantiate WCETs
    C = [0]*m

    #For each WCET...
    for i in range(0,m):

        #If utilization bounds are incorrect or incompatible...
        if(utilizationLowerBound <= 0 or utilizationUpperBound < utilizationLowerBound):

            #Set utilization bounds to defaults
            utilizationLowerBound = 1
            utilizationUpperBound = 100

        #Initialize to a random WCET (WCET may not exceed p)
        C[i] = random.randint(utilizationLowerBound,utilizationUpperBound)/100

    #Sort the WCETs in correct order
    C.sort(reverse=True)

    #Create Boundaries

    #Instantiate Boundaries
    B = [0]*(m+1)

    #Set boundary 0 to zero
    B[0] = 0

    #For each boundary...
    for i in range(0,m):

        #Initialize to random error
        B[i+1] = random.randint(1,100)

    #Sort the boundaries in correct order
    B.sort()

    #Create Operating Bounds
    operatingBounds_rand = GFC.randomRwsTaskWcet(C,B)

    #Create Generic Function
    #   Slope
    f_scalar = random.random()
    #   Exponent
    f_radix = random.random()+1
    #   Offset
    f_offset = random.random()
     #   Round
    f_scalar = round(f_scalar,2) 
    f_radix = round(f_radix,2)  
    f_offset = round(f_offset,2) 
    #   Create Function
    f_rand = lambda a : float(f_scalar) * math.pow(float(f_radix),-a) + float(f_offset)

    assert(f_rand(100) >= 0)

    #Create Setpoint Schedule

    #Pick # of Setpoints
    n = random.randint(numResetTimesLowerBound,numResetTimesUpperBound)

    #Instantiate Setpoint Updates
    S = [0]*n

    #For each setpoint update...
    for i in range(0,n-1+1):

        #Initialize setpoint update to random starting value
        S[i] = random.randint(0,10)

    #Instantiate Setpoint Update Offsets
    A = [0]*n

    #For each offset (except the first offset):
    for i in range(1,n-1+1):

        #Initialize offset to random time 
        A[i] = random.randint(minimumSeparationBetweenSuccessiveResetTimes,maximumSeparationBetweenSuccessiveResetTimes)*p

        #Since these are offsets, add the previous value if this is not the first offset
        if(i>0):
            A[i] += A[i-1]

    #Initialize hyperperiod to random time
    P = A[n-1] + random.randint(minimumSeparationBetweenSuccessiveResetTimes,maximumSeparationBetweenSuccessiveResetTimes)*p

    #Create Setpoint Schedule
    SpSch_rand = GFC.superSchedule(S,A,P)

    #Create Demand Window
    a = random.randint(1,100)
    delta = random.randint(p,10*P)
    w_rand = GFC.demandWindow(a,delta)

    #Set max value to half of highest WCET if asked...
    if(maximumValueAtReset == -1):
        maximumValueAtReset = B[1] / 2

    #Create RwsMaeTask
    randRwsMaeTask = GFRWSMAE_TOOL.gfRwsMaeTool(p,f_rand,operatingBounds_rand,SpSch_rand,w_rand,f_scalar,f_radix,f_offset,maximumValueAtReset)

    #Return RwsMaeTask
    return randRwsMaeTask

#Generate a feasible RwsMaeTask
def generateRandomFeasibleRwsTask(   numResetTimesLowerBound,
                                        numResetTimesUpperBound,
                                        numWcetsLowerBound,
                                        numWcetsUpperBound,
                                        utilizationLowerBound,
                                        utilizationUpperBound,
                                        maximumValueAtReset,
                                        minSepBetweenSuccessiveResets,
                                        maxSepBetweenSuccessiveResets):

    #Create stats storage
    randomRwsTaskGenerationStats = randomFeasibleGenerationStats()
    
    #Assume the RwsMaeTask is infeasible
    RwsMaeTaskIsInfeasible = True

    #While the RwsMaeTask remains infeasible...
    while(RwsMaeTaskIsInfeasible == True):

        #Generate a random RwsMaeTask...
        randomRwsTask = GF_RWS_MAE_GEN.generateRandomRwsMaeTask( numResetTimesLowerBound,
                                                                    numResetTimesUpperBound,
                                                                    numWcetsLowerBound,
                                                                    numWcetsUpperBound,
                                                                    utilizationLowerBound,
                                                                    utilizationUpperBound,
                                                                    maximumValueAtReset,
                                                                    minSepBetweenSuccessiveResets,
                                                                    maxSepBetweenSuccessiveResets)

        #Calculate Dimensions
        randomRwsTask.calcDimensions()

        #Make integer multiples
        randomRwsTask.makeIntegerMultiples()

        #Check feasibility
        feasibility = randomRwsTask.checkForFeasibility()

        #If WCD is less than 0 (there's an error)
        if(feasibility < 0):            

            #Log the error
            if(feasibility == -8):
                randomRwsTaskGenerationStats.violatesMaximumValueAtReset+=1
            elif(feasibility == -9):
                randomRwsTaskGenerationStats.violatesMaxStartingValue+=1
            elif(feasibility == -10):
                randomRwsTaskGenerationStats.superperiodTooLarge+=1
            elif(feasibility == -12):
                randomRwsTaskGenerationStats.lowestWcetBoundaryTooSmall+=1
            elif(feasibility == -13):
                randomRwsTaskGenerationStats.superperiodTooSmall+=1

        #otherwise...
        else:

            #flag as valid
            RwsMaeTaskIsInfeasible = False

        #Log Generations
        randomRwsTaskGenerationStats.totalGenerations+=1

    #Return RwsMaeTask and Stats
    return (randomRwsTask,randomRwsTaskGenerationStats)

class randomFeasibleGenerationStats:

    def __init__(self,
        violatesMaximumValueAtReset = 0,
        violatesMaxStartingValue = 0,
        superperiodTooLarge = 0,
        superperiodTooSmall = 0,
        lowestWcetBoundaryTooSmall = 0,
        totalGenerations = 0):

            #Copy over information
            
            self.violatesMaximumValueAtReset = copy.deepcopy(violatesMaximumValueAtReset)
            self.violatesMaxStartingValue = copy.deepcopy(violatesMaxStartingValue)
            self.superperiodTooLarge = copy.deepcopy(superperiodTooLarge)
            self.superperiodTooSmall = copy.deepcopy(superperiodTooSmall)
            self.lowestWcetBoundaryTooSmall = copy.deepcopy(lowestWcetBoundaryTooSmall)
            self.totalGenerations = copy.deepcopy(totalGenerations)
