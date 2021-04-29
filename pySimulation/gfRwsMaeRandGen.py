# Generic Function RWS MAE Random Generator

# Description:
# This file provides functionality for generating random task sets and logging data about attempts to generate task sets and stats about the task sets themselves

#Imports
#   Import the general GF RWS MAE functions
import gfRwsMaeGeneral as GF_RWS_MAE_GEN

#   Import PRNG functions
import random

#   Import ceil, floor, GCD functions
import math

#   Import data timestamping
import datetime

#   Import deepcopy functions
import copy

#   Import time functions
import time

# Generate RWS task(s) for the provided experiment parameters
def feasibleRwsMaeTaskGenerator_ExpSetup(experimentSetup):

    # Generate the RWS task(s)
    return feasibleRwsMaeTaskGenerator(
        experimentSetup.numSamples,
        experimentSetup.numResetTimesLowerBound,
        experimentSetup.numResetTimesUpperBound,
        experimentSetup.numWcetsLowerBound,
        experimentSetup.numWcetsUpperBound,
        experimentSetup.utilizationLowerBound,
        experimentSetup.utilizationUpperBound,
        experimentSetup.fileName,
        experimentSetup.fixedVars,
        experimentSetup.startP,
        experimentSetup.endP,
        experimentSetup.deltaP,
        experimentSetup.maximumValueAtReset)

# Generate a feasible RWS task based on the provided values
def feasibleRwsMaeTaskGenerator(numberOfRandomTasks,
    numResetTimesLowerBound,
    numResetTimesUpperBound,
    numWcetsLowerBound,
    numWcetsUpperBound,
    utilizationLowerBound,
    utilizationUpperBound,
    fileName,
    fixedVars,
    startP,
    endP,
    deltaP,
    maximumValueAtReset):

    #Convert naming
    numRand = numberOfRandomTasks
    
    #Stats Initialization
    totalNumWcets = 0
    totalNumResetTimes = 0
    totalHyperperiods = 0
    totalGenerations = 0
    violatesMaximumValueAtResetTotal = 0
    violatesMaxStartingValueTotal = 0
    superperiodTooLargeTotal = 0
    superperiodTooSmall = 0
    lowestWcetBoundaryTooSmallTotal = 0
    
    dbf = [0]*10

    #Open file for logging
    csvFile = open(str(fileName),"a+",10)

    #If fixed vars requested...
    if(fixedVars == 2):

        #Number of random SCs
        numRand = int((endP - startP)/deltaP)
        rRwsTasks = [0]*numRand
        rRwsTaskGenStats = [0]*numRand
        index = 0

        #Check for deltaP
        if(deltaP < 0):

            #Assign to 1 if negative
            deltaP = 1

        #For each requested P...
        for i in range(startP,endP,deltaP):

            #While initial P is incorrect
            pNotTarget = True
            while(pNotTarget):

                #Generate a feasible RwsMaeTask
                (randomRwsTask, randomRwsTaskGenerationStats) = GF_RWS_MAE_GEN.generateRandomFeasibleRwsTask(
                                                                                                                1,
                                                                                                                10,
                                                                                                                numWcetsLowerBound,
                                                                                                                numWcetsUpperBound,
                                                                                                                utilizationLowerBound,
                                                                                                                utilizationUpperBound,
                                                                                                                maximumValueAtReset,
                                                                                                                1,
                                                                                                                50)

                #Chceck setpoint period length
                if(randomRwsTask.P == startP+index*deltaP):

                    pNotTarget = False

            #Calculate the WCDs
            print("Run with P ",randomRwsTask.P," of ",endP)
            printIt = True
            dbf[0] = randomRwsTask.calcDbf(0,printIt) #GMF
            dbf[1] = randomRwsTask.calcDbf(1,printIt) #RWSMAEDBF

            #Log RwsMaeTask
            rRwsTasks[index] = copy.deepcopy(randomRwsTask)
            rRwsTaskGenStats[index] = copy.deepcopy(randomRwsTaskGenerationStats)

            #Create output string
            output = str(rRwsTasks[index].n) + "," + str(rRwsTasks[index].P)

            #For each wcd calculation method...
            for j in range(2):

                #Gather Stats
                output += "," + str(rRwsTasks[index].getComputationTime()[j])

            #Get date
            today = datetime.date.today()
            output += "," + str(today)

            #Get Time
            now = datetime.datetime.now()
            current_time = now.strftime("%H-%M-%S")
            output += "," + str(current_time)

            #Write to file
            output += "\n"
            csvFile.write(output)

            #Increment Index
            index += 1
    
    elif(fixedVars == 1):

        #While initial P is too large
        initialPtooLarge = True
        while(initialPtooLarge):

            #Generate a feasible RwsMaeTask
            (randomRwsTask, randomRwsTaskGenerationStats) = GF_RWS_MAE_GEN.generateRandomFeasibleRwsTask(
                                                                                                            1,
                                                                                                            10,
                                                                                                            numWcetsLowerBound,
                                                                                                            numWcetsUpperBound,
                                                                                                            utilizationLowerBound,
                                                                                                            utilizationUpperBound,
                                                                                                            maximumValueAtReset,
                                                                                                            1,
                                                                                                            50
                                                                                                        )

            #Chceck setpoint period length
            if(randomRwsTask.P <= startP):

                initialPtooLarge = False

        #If P is below starting P...
        if(randomRwsTask.P < startP):

            #Calculate the difference
            difference = startP - randomRwsTask.P

            #Increment by difference
            randomRwsTask.incrementP(difference)

        #Number of random tasks
        numRand = int(1 + (endP - randomRwsTask.P)/deltaP)
        rRwsTasks = [0]*numRand
        rRwsTaskGenStats = [0]*numRand
        index = 0

        #While the P value is less than some value...
        while(randomRwsTask.P <= endP):

            #Calculate the WCDs
            print("Run with P ",randomRwsTask.P," of ",endP)
            printIt = True
            dbf[0] = randomRwsTask.calcDbf(0,printIt) #GMF
            dbf[1] = randomRwsTask.calcDbf(1,printIt) #RWSMAEDBF

            assert(dbf[4] >= 0)

            #Log RwsMaeTask
            rRwsTasks[index] = copy.deepcopy(randomRwsTask)
            rRwsTaskGenStats[index] = copy.deepcopy(randomRwsTaskGenerationStats)

            #Create output string
            output = str(rRwsTasks[index].n) + "," + str(rRwsTasks[index].P)


            #For each wcd calculation method...
            for j in range(2):

                #Gather Stats
                output += "," + str(rRwsTasks[index].getComputationTime()[j])

            #Get date
            today = datetime.date.today()
            output += "," + str(today)

            #Get Time
            now = datetime.datetime.now()
            current_time = now.strftime("%H-%M-%S")
            output += "," + str(current_time)

            #Write to file
            output += "\n"
            csvFile.write(output)

            #Increment P
            randomRwsTask.incrementP(deltaP)

            #Increment Index
            index += 1

    elif(fixedVars == 0):

        #10k Trials
        numRand = numberOfRandomTasks

        #Number of random SCs
        rRwsTasks = [0]*numRand
        rRwsTaskGenStats = [0]*numRand

        #Create random SC RwsMaeTasks and calc WCD until 10 results exist:
        for i in range(0,numRand):
            
            #Create RwsMaeTask Variable
            (randomRwsTask, randomRwsTaskGenerationStats) = GF_RWS_MAE_GEN.generateRandomFeasibleRwsTask(
                                                                                                            1,
                                                                                                            10,
                                                                                                            numWcetsLowerBound,
                                                                                                            numWcetsUpperBound,
                                                                                                            utilizationLowerBound,
                                                                                                            utilizationUpperBound,
                                                                                                            maximumValueAtReset,
                                                                                                            1,
                                                                                                            50
                                                                                                            )

            #Calculate the WCDs
            print(">Run # ",i," of ",numRand)
            printIt = True
            dbf[0] = randomRwsTask.calcDbf(0,printIt) #GMF
            dbf[1] = randomRwsTask.calcDbf(1,printIt) #RWS-MAE

            #Log RwsMaeTask
            rRwsTasks[i] = copy.deepcopy(randomRwsTask)
            rRwsTaskGenStats[i] = copy.deepcopy(randomRwsTaskGenerationStats)

            if(round(dbf[0],4) != round(dbf[1],4)):
                print(dbf[0] + "  =/=  " + dbf[1])
                assert(dbf[0] == dbf[1])

            #Create output string
            output = str(rRwsTasks[i].n) + "," + str(rRwsTasks[i].P)

            #For each wcd calculation method...
            for j in range(2):

                #Gather Stats
                output += "," + str(rRwsTasks[i].getComputationTime()[j])

            #Get date
            today = datetime.date.today()
            output += "," + str(today)

            #Get Time
            now = datetime.datetime.now()
            current_time = now.strftime("%H-%M-%S")
            output += "," + str(current_time)

            #Write to file
            output += "\n"
            csvFile.write(output)

    #Initialize average results vars
    totalPctReduction = [0]*10
    totalComputationTime = [0]*10
    totalRuntimeImprovement = [0]*10
    averagePctReduction = [0]*10
    averageComputationTime = [0]*10

    #Create CSV title row
    output = "n,P"
    output +=",L&L WCD,GMF DBF,NSW WCD,SDT WCD,SD DBF,SDT WCD (bSearch), SDT WCD (bSearch x2), NSW DBF, Date, Time"
    output +="\n"

    #Write CSV title row
    csvFile.write(output)

    #For every randomly generated switched RwsMaeTask...
    for i in range(0,numRand):

        #Log RwsMaeTasks, Setpoints
        totalNumWcets+=rRwsTasks[i].m
        totalNumResetTimes+=rRwsTasks[i].n
        totalHyperperiods+=rRwsTasks[i].P
        totalGenerations+=rRwsTaskGenStats[i].totalGenerations
        violatesMaximumValueAtResetTotal += rRwsTaskGenStats[i].violatesMaximumValueAtReset
        violatesMaxStartingValueTotal += rRwsTaskGenStats[i].violatesMaxStartingValue
        superperiodTooLargeTotal += rRwsTaskGenStats[i].superperiodTooLarge
        superperiodTooSmallTotal += rRwsTaskGenStats[i].superperiodTooSmall
        lowestWcetBoundaryTooSmallTotal += rRwsTaskGenStats[i].lowestWcetBoundaryTooSmall

        #For each wcd calculation method...
        for j in range(2):

            #Gather Stats
            totalComputationTime[j] +=  rRwsTasks[i].getComputationTime()[j]
            totalRuntimeImprovement[j] += ((rRwsTasks[i].getComputationTime()[0] - rRwsTasks[i].getComputationTime()[j])/rRwsTasks[i].getComputationTime()[0]) * 100

    #Close File
    csvFile.close()

    #Calculate Rates, Averages, Etc.
    successfulGenerationRate = numRand/totalGenerations
    failedGenerations = totalGenerations - numRand
    failedGenerationRate = failedGenerations / totalGenerations
    averageHyperperiod = totalHyperperiods/numRand
    averageNumSetpoints = totalNumResetTimes/numRand
    averageNumWcets = totalNumWcets/numRand

    #For each calculation method
    for i in range(0,len(totalComputationTime)):

        #Calculate the average computation time
        averageComputationTime[i] = totalComputationTime[i]/numRand

    #Print Stats
    print("===================================")
    print("Random SC Task Generation Stats")
    print("-----------------------------------")
    print("Successful Generations: ",numRand)
    print("Successful Gen Rate: ",successfulGenerationRate)
    print("Failed Generations:",failedGenerations)
    print("Violated Maximum Value at Reset Time:",violatesMaximumValueAtResetTotal)
    print("Violated Maximum Starting Value:",violatesMaxStartingValueTotal)
    print("Super Period Too Large (>1000):",superperiodTooLargeTotal)
    print("Super Period Too Small (<=0):",superperiodTooSmall)
    print("Lowest WCET Boundary Too Small (f(0)>B[m]):",lowestWcetBoundaryTooSmallTotal)
    print("===================================")
    print("Random RWS Task Feasibility Failure Analysis")
    print("-----------------------------------")
    print("Failed Gen Rate:",failedGenerationRate)
    print("Total Generations: ",totalGenerations)
    print("===================================")
    print("Random SC Feasibility Success Analysis:")
    print("-----------------------------------")
    print("Average Hyperperiod    : ",averageHyperperiod)
    print("Average Num Setpoints  : ",averageNumSetpoints)
    print("Average Num WCETs: ",averageNumWcets)
    print("===================================")
    print("Algorithm (type) - Table Build Time - Search Time - Asymp. - Average Computation Times (ms): ",)
    print("-----------------------------------")
    print("GMF         (dbf) - O(H^2 lg H)        - O(1)               : ",totalComputationTime[0]/numRand)
    print("RWS-MAE-DBF (dbf) - O(nH) + O(H lg H)) - O(1)               : ",totalComputationTime[1]/numRand)
    print("===================================")
    print("Algorithm (type) - Average % Improvement: ",)
    print("-----------------------------------")
    print("GMF         (dbf) : ",totalRuntimeImprovement[0]/numRand)
    print("RWS-MAE-DBF (dbf) : ",totalRuntimeImprovement[1]/numRand)
    print("===================================")


def slightVariantExperimentRunner_ExpSetup(experimentSetup):

    return slightVariantExperimentRunner(
        experimentSetup.numSamples,
        experimentSetup.numResetTimesLowerBound,
        experimentSetup.numResetTimesUpperBound,
        experimentSetup.numWcetsLowerBound,
        experimentSetup.numWcetsUpperBound,
        experimentSetup.utilizationLowerBound,
        experimentSetup.utilizationUpperBound,
        experimentSetup.maximumValueAtReset,
        experimentSetup.fileName,
        experimentSetup.checkpointFrequency
    )

# Create an ass
def slightVariantExperimentRunner(numberOfSamples,numResetTimesLowerBound,numResetTimesUpperBound,numWcetsLowerBound,numWcetsUpperBound,utilizationLowerBound,utilizationUpperBound,maximumValueAtReset,fileName,checkpointFrequency):

    #Create arrays
    rRwsArray = [0]*numberOfSamples
    rRwsTaskStatsArray = [0]*numberOfSamples
    scalingRatioArray = [0]*numberOfSamples
    rRwsTasks_tsl_up_Array = [0]*numberOfSamples
    rRwsTasks_tsl_dn_Array = [0]*numberOfSamples
    rRwsTasks_wcet_up_Array = [0]*numberOfSamples
    rRwsTasks_wcet_dn_Array = [0]*numberOfSamples
    rRwsTasks_timeBetweenReset_up_Array = [0]*numberOfSamples
    rRwsTasks_timeBetweenReset_dn_Array = [0]*numberOfSamples

    #Open file for logging
    csvFile = open(str(fileName),"a+",10)

    #Print title rows
    output = "RWS super period,Highest WCET,Scaling Ratio (SR),WCET*1.1,WCET*0.9 SR,Time Between Resets*1.1 SR, Time Between Resets*0.9 SR\n"
    csvFile.write(output)

    for i in range(0,numberOfSamples):

        allFeasible = False

        while(not allFeasible):

            (randomRwsTask, randomRwsTaskGenerationStats) = GF_RWS_MAE_GEN.generateRandomFeasibleRwsTask(
                numResetTimesLowerBound,
                numResetTimesUpperBound,
                numWcetsLowerBound,
                numWcetsUpperBound,
                utilizationLowerBound,
                utilizationUpperBound,
                maximumValueAtReset,
                1,
                50
                )

            #rwsMaeTask Variants
            rRwsTasks_wcet_up = copy.deepcopy(randomRwsTask)
            rRwsTasks_wcet_dn = copy.deepcopy(randomRwsTask)
            rRwsTasks_timeBetweenReset_up = copy.deepcopy(randomRwsTask)
            rRwsTasks_timeBetweenReset_dn = copy.deepcopy(randomRwsTask)

            #10% change
            rRwsTasks_wcet_up.C = [x * 1.1 for x in rRwsTasks_wcet_up.C]
            rRwsTasks_wcet_dn.C = [x * 0.9 for x in rRwsTasks_wcet_dn.C]

            #10% change
            rRwsTasks_timeBetweenReset_up.R = [int(math.ceil(x * 1.1)) for x in rRwsTasks_timeBetweenReset_up.R]
            rRwsTasks_timeBetweenReset_up.P = int(math.ceil(rRwsTasks_timeBetweenReset_up.P * 1.1))

            #10% change
            rRwsTasks_timeBetweenReset_dn.R = [int(math.floor(x * 0.9)) for x in rRwsTasks_timeBetweenReset_dn.R]
            rRwsTasks_timeBetweenReset_dn.P = int(math.floor(rRwsTasks_timeBetweenReset_dn.P * 0.9))

            #Assume all are feasible
            allFeasible = True

            #Check one by one
            if( rRwsTasks_wcet_up.checkForFeasibility() != 0 ): allFeasible = False
            if( rRwsTasks_wcet_dn.checkForFeasibility() != 0 ): allFeasible = False
            if( rRwsTasks_timeBetweenReset_up.checkForFeasibility() != 0 ): allFeasible = False
            if( rRwsTasks_timeBetweenReset_dn.checkForFeasibility() != 0 ): allFeasible = False
        
        #Compute DBFs
        randomRwsTask.calcDbf(1,True)
        rRwsTasks_wcet_up.calcDbf(1,True)
        rRwsTasks_wcet_dn.calcDbf(1,True)
        rRwsTasks_timeBetweenReset_up.calcDbf(1,True)
        rRwsTasks_timeBetweenReset_dn.calcDbf(1,True)

        #Compute scaling Ratios
        scalingRatio = []
        scalingRatio.append(randomRwsTask.dbf[1]/randomRwsTask.P)
        scalingRatio.append(rRwsTasks_wcet_up.dbf[1]/rRwsTasks_wcet_up.P)
        scalingRatio.append(rRwsTasks_wcet_dn.dbf[1]/rRwsTasks_wcet_dn.P)
        scalingRatio.append(rRwsTasks_timeBetweenReset_up.dbf[1]/rRwsTasks_timeBetweenReset_up.P)
        scalingRatio.append(rRwsTasks_timeBetweenReset_dn.dbf[1]/rRwsTasks_timeBetweenReset_dn.P)

        #Log data
        output = ""
        output += str(randomRwsTask.P) + ","
        output += str(randomRwsTask.C[0]) + ","
        output += str(scalingRatio[0]) + ","
        output += str(scalingRatio[1]) + ","
        output += str(scalingRatio[2]) + ","
        output += str(scalingRatio[3]) + ","
        output += str(scalingRatio[4])

        #Get date
        today = datetime.date.today()
        output += "," + str(today)

        #Get Time
        now = datetime.datetime.now()
        current_time = now.strftime("%H-%M-%S")
        output += "," + str(current_time)

        #Write to file
        output += "\n"
        csvFile.write(output)


        #Print Checkpoints (if desired)
        if(checkpointFrequency != 0 and i%checkpointFrequency == 0):
            print("Run # ",i)

        #Log Info
        rRwsArray[i] = randomRwsTask
        rRwsTaskStatsArray[i] = randomRwsTaskGenerationStats
        rRwsTasks_wcet_up_Array[i] = rRwsTasks_wcet_up
        rRwsTasks_wcet_dn_Array[i] = rRwsTasks_wcet_dn
        rRwsTasks_timeBetweenReset_up_Array[i] = rRwsTasks_timeBetweenReset_up
        rRwsTasks_timeBetweenReset_dn_Array[i] = rRwsTasks_timeBetweenReset_dn
        scalingRatioArray[i] = scalingRatio

    # Return results array
    return (rRwsArray,
        rRwsTaskStatsArray,
        rRwsTasks_wcet_up_Array,
        rRwsTasks_wcet_dn_Array,
        rRwsTasks_timeBetweenReset_up_Array,
        rRwsTasks_timeBetweenReset_dn_Array,
        scalingRatioArray)

def inflationExperimentRunner_ExpSetup(experimentSetup):

    return inflationExperimentRunner(
        experimentSetup.numSamples,
        experimentSetup.numResetTimesLowerBound,
        experimentSetup.numResetTimesUpperBound,
        experimentSetup.numWcetsLowerBound,
        experimentSetup.numWcetsUpperBound,
        experimentSetup.utilizationLowerBound,
        experimentSetup.utilizationUpperBound,
        experimentSetup.maximumValueAtReset,
        experimentSetup.minSepBetweenSuccessiveResets,
        experimentSetup.maxSepBetweenSuccessiveResets,
        experimentSetup.nPeriodic_lo,
        experimentSetup.nPeriodic_hi,
        experimentSetup.periodUpperBoundCode,
        experimentSetup.fileName,
        experimentSetup.checkpointFrequency
    )

def inflationExperimentRunner(
    numberOfSamples,
    numResetTimesLowerBound,
    numResetTimesUpperBound,
    numWcetsLowerBound,
    numWcetsUpperBound,
    utilizationLowerBound,
    utilizationUpperBound,
    maximumValueAtReset,
    minSepBetweenSuccessiveResets,
    maxSepBetweenSuccessiveResets,
    nPeriodic_lo,
    nPeriodic_hi,
    periodUpperBoundCode,
    fileName,
    checkpointFrequency):

    #Establish arrays of data
    rRwsArray = [0]*numberOfSamples
    rRwsTaskStatsArray = [0]*numberOfSamples
    cSetArray = [0]*numberOfSamples
    pSetArray = [0]*numberOfSamples
    uSetArray = [0]*numberOfSamples
    expStatsArray = [0]*numberOfSamples

    #Open file for logging
    csvFile = open(str(fileName),"a+",10)

    #Print title rows
    output = "minCtrlTaskUtil,maxCtrlTaskUtil,TargetUtil,P,AllTasksDbfSum,AllPeriodsLcm,PctTimeUnused,"
    output += "ScalingRatio,NumPeriodicTasks,NumResets,NumWcets,avgStartingValues,"
    output += "avgTimeBetweenResetDuration,dbf/apLcm,"
    output += "avgWcet,wcetLowToHighRatio,wcetAvgToHighRatio,minUtil,avgUtil,"
    output += "periodUpperBoundCode,gmfCalcTime,rwsCalcTime,perfImproveNoSA,schedAnalysisTime,perfImproveWithSA,schedulable,Date,Time\n"
    csvFile.write(output)

    #For each sample requested...
    for i in range(0,numberOfSamples):

        print("Run #",i)

        #Generate an inflation comparison
        (rRwsArray[i], rRwsTaskStatsArray[i], (cSetArray[i],pSetArray[i], uSetArray[i]), expStatsArray[i]) = inflationComparisonGenerator(
            numResetTimesLowerBound,
            numResetTimesUpperBound,
            numWcetsLowerBound,
            numWcetsUpperBound,
            utilizationLowerBound,
            utilizationUpperBound,
            maximumValueAtReset,
            minSepBetweenSuccessiveResets,
            maxSepBetweenSuccessiveResets,
            nPeriodic_lo,
            nPeriodic_hi,
            periodUpperBoundCode)

        #Calculate Average starting value
        sumStartingValues = 0
        for j in range(0,rRwsArray[i].n):
            sumStartingValues += abs(rRwsArray[i].S[j] - rRwsArray[i].S[(j-1)%rRwsArray[i].n])
        avgStartingValues = sumStartingValues / rRwsArray[i].n

        #Calculate average time between resets duration
        avgTimeBetweenResetDuration = rRwsArray[i].P/rRwsArray[i].n

        #Calculate avg WCET
        avgWcet = sum(rRwsArray[i].C)/len(rRwsArray[i].C)

        #Calculate ratio of lowest WCET to highest
        wcetLowToHighRatio = min(rRwsArray[i].C) / max(rRwsArray[i].C)

        #Calc avg WCET ratio to highest
        wcetAvgToHighRatio = avgWcet / max(rRwsArray[i].C)

        #Calc min util
        minUtil = min(rRwsArray[i].C)/rRwsArray[i].p

        #Calc avg util
        avgUtil = avgWcet/rRwsArray[i].p

        #Get calc times
        (gmfCalcTime,rwsCalcTime) = rRwsArray[i].getComputationTime()

        #Log data
        output = str(expStatsArray[i].minCtrlTaskUtil) + ","
        output += str(expStatsArray[i].maxCtrlTaskUtil) + ","
        output += str(expStatsArray[i].targetUtilization) + ","
        output += str(rRwsArray[i].P) +","
        output += str(expStatsArray[i].allTasksDbfSum) + ","
        output += str(expStatsArray[i].allPeriodsLCM) + ","
        output += str(expStatsArray[i].percentTimeUnusedVarAdc) + ","
        output += str(expStatsArray[i].scalingRatio) + ","
        output += str(expStatsArray[i].nPeriodicTasks) + ","
        output += str(rRwsArray[i].n) + ","
        output += str(rRwsArray[i].m) + ","
        output += str(avgStartingValues) + ","
        output += str(avgTimeBetweenResetDuration) + ","
        output += str(rRwsArray[i].dbf[1]/expStatsArray[i].allPeriodsLCM) +","
        output += str(avgWcet) + ","
        output += str(wcetLowToHighRatio) + ","
        output += str(wcetAvgToHighRatio) + ","
        output += str(minUtil) + ","
        output += str(avgUtil) + ","
        output += str(periodUpperBoundCode) + ","
        output += str(gmfCalcTime) + ","
        output += str(rwsCalcTime) + ","
        output += str(gmfCalcTime/rwsCalcTime) + ","
        output += str(expStatsArray[i].schedAnalysisTime) + ","
        output += str((gmfCalcTime+expStatsArray[i].schedAnalysisTime)/(rwsCalcTime+expStatsArray[i].schedAnalysisTime)) + ","
        output += str(expStatsArray[i].schedulable)

        #Get date
        today = datetime.date.today()
        output += "," + str(today)

        #Get Time
        now = datetime.datetime.now()
        current_time = now.strftime("%H-%M-%S")
        output += "," + str(current_time)

        #Write to file
        output += "\n"
        csvFile.write(output)

        #Print Checkpoints (if desired)
        if(checkpointFrequency != 0 and i%checkpointFrequency == 0):
            print("Run # ",i)

    #Calculate average stats
    avgExpStats = inflationExperimentCalculateAverageStats(expStatsArray,numberOfSamples)

    #Return results
    return (rRwsArray, rRwsTaskStatsArray, (cSetArray, pSetArray, uSetArray), expStatsArray, avgExpStats)

def inflationComparisonGenerator(   numResetTimesLowerBound,
                                    numResetTimesUpperBound,
                                    numWcetsLowerBound,
                                    numWcetsUpperBound,
                                    utilizationLowerBound,
                                    utilizationUpperBound,
                                    maximumValueAtReset,
                                    minSepBetweenSuccessiveResets,
                                    maxSepBetweenSuccessiveResets,
                                    nPeriodic_lo,
                                    nPeriodic_hi,
                                    periodUpperBoundCode):

    #Create Experiment Stats
    expStats = breakdownUtilExpStats()

    #Establish target utilization
    targetUtil = 0 

    #While target utilization is zero...
    while(targetUtil == 0):

        #Generate Control Task
        (randomRwsTask, randomRwsTaskGenerationStats) = GF_RWS_MAE_GEN.generateRandomFeasibleRwsTask(
            numResetTimesLowerBound,
            numResetTimesUpperBound,
            numWcetsLowerBound,
            numWcetsUpperBound,
            utilizationLowerBound,
            utilizationUpperBound,
            maximumValueAtReset,
            1,
            50)

        #Calculate maximum utilization of control task
        maxCtrlTaskUtil = randomRwsTask.C[0]/randomRwsTask.p

        #Calculate minimum utilization of control task
        minCtrlTaskUtil = randomRwsTask.C[randomRwsTask.m-1]/randomRwsTask.p

        #Log data
        expStats.maxCtrlTaskUtil = maxCtrlTaskUtil
        expStats.minCtrlTaskUtil = minCtrlTaskUtil

        #Calculate remainders
        minTargetPeriodicUtil = 1-maxCtrlTaskUtil
        maxTargetPeriodicUtil = 1-minCtrlTaskUtil

        #Generate random target util
        targetUtil = random.random()*(maxTargetPeriodicUtil - minTargetPeriodicUtil) + minTargetPeriodicUtil
        expStats.targetUtilization = targetUtil

    #Pick number of additional, periodic tasks
    if(nPeriodic_lo < 0 or nPeriodic_hi < 0 or nPeriodic_lo > nPeriodic_hi):
        nPeriodicTasks = random.randint(0,5)
    else:
        nPeriodicTasks = random.randint(nPeriodic_lo, nPeriodic_hi)
    expStats.nPeriodicTasks = nPeriodicTasks

    #Establish utilization sum and set
    uSum = 0
    uSet = []

    #Continually generate utilizations until sum of utilizations and target utilization are equal
    while(uSum != targetUtil):

        #Generate Utilizations using UUNIFAST
        uSet = UUNIFAST(nPeriodicTasks, targetUtil)

        #Calc total utilization
        uSum = sum(uSet)

    #Create array of periods, WCETs
    cSet = []
    pSet = []

    #Generate Random Periods for the utilizations
    (cSet, pSet) = genRandomPeriods(uSet, periodUpperBoundCode, randomRwsTask)

    #Create array of all periodic periods and SCS major period
    allPeriods = copy.deepcopy(pSet)
    allPeriods.append(randomRwsTask.P)

    #Calculate LCM of all periodic periods and SCS major period
    apLcm = allPeriods[0]
    for i in allPeriods[1:]:
        apLcm = apLcm*i//math.gcd(apLcm, i)

    #Assert LCM is actually LCM
    for i in range(0,len(allPeriods)):
        assert(apLcm % allPeriods[i] == 0)

    #Log apLcm
    expStats.allPeriodsLCM = apLcm

    #Create DBF function of each periodic task
    def dbf(c,p,t):

        #Calculate demand
        d = math.floor(t/p)*c

        #Return
        return d

    #Create DBF array
    dbfSet = []

    #Calculate DBF of all periodic functions up to hyperperiod (apLcm)
    for i in range(0,nPeriodicTasks-1):

        #Append DBF
        dbfSet.append(dbf(cSet[i],pSet[i],apLcm))

    #Calculate DBF of SCS
    randomRwsTask.delta = apLcm
    randomRwsTask.calcDbf(1,True)
    randomRwsTask.calcDbf(0,True)
    dbfSet.append(randomRwsTask.dbf[1])

    #Start Sched. Analysis Clock
    schedStartTime = time.time()

    #Assert feasibility
    #   For every time step
    for i in range(0,len(randomRwsTask.RWS_MAE_DBF_table)):

        #Get RWS DBF
        demand = randomRwsTask.RWS_MAE_DBF_table[i]

        #Reset non-RWS demand
        nonRwsDemand = 0

        #Sum non-RWS demand
        for j in range(0,nPeriodicTasks-1):

            #Add demand of periodic task
            nonRwsDemand += dbf(cSet[j],pSet[j],i)

        if(demand + nonRwsDemand > i+1):

            expStats.schedulable = False

            break;

    #Stop Sched. Analysis Clock
    schedStopTime = time.time()

    #Calculate Sched. Analysis Time
    schedAnalysisTime = schedStopTime - schedStartTime

    #Log Data
    expStats.schedAnalysisTime = schedAnalysisTime

    #Sum all DBF
    sumDbf = sum(dbfSet)
    expStats.allTasksDbfSum = sumDbf

    #Compare against identity
    diff = apLcm - sumDbf

    #Calculate pct time used
    pctTimeUnused = diff / apLcm
    expStats.percentTimeUnusedVarAdc = pctTimeUnused

    #Calculate ratio
    scalingRatio = apLcm / sumDbf
    expStats.scalingRatio = scalingRatio

    #Return scs, periodic tasks, experiment stats
    return (randomRwsTask, randomRwsTaskGenerationStats, (cSet,pSet, uSet), expStats)

def genRandomPeriods(uSet, periodUpperBoundCode, randomRwsTask):

    #Create array of periods, WCETs
    cSet = []
    pSet = []

    #If period bound code is negative...
    if(periodUpperBoundCode < 0):

        #Make period upper bound a multiple of major period
        periodUpperBound = randomRwsTask.P * periodUpperBoundCode * -1
    
    #If period bound code is positive...
    if(periodUpperBoundCode > 0):

        #Make period upper bound a multiple of minor period
        periodUpperBound = randomRwsTask.p * periodUpperBoundCode

    assert(periodUpperBoundCode != 0)

    #For each task...
    for i in range(0,len(uSet)):

        #Create random period
        pRand = 0

        #While random period is not positive...
        while(pRand <= 0):

            #Generate random period in range 0 to twice the SCS task major period
            pRand = math.floor(random.random()*periodUpperBound)

        #Append to pSet
        pSet.append(pRand)

        #Generate corresponding WCETs
        cSet.append(uSet[i] * pRand)
    
    #Assert WCET and period were selected correctly
    for i in range(0,len(uSet)):

        assert(round(cSet[i]/pSet[i],10) == round(uSet[i],10))

    #Return
    return (cSet, pSet)

def UUNIFAST(nPeriodicTasks, targetUtil):

    #Establish set of utilizations
    uSet = []

    #Establish target utilization
    sumU = targetUtil

    #For each task
    for i in range(1, nPeriodicTasks):

        #Assume the task has an invalid utilization
        valid = 0

        #While the utilization is invalid
        while(not valid):

            #Generate a utilization
            nextSumU = sumU * random.random() ** (1.0 / (nPeriodicTasks - i))

            #Check if the utilization is valid
            valid = nextSumU > 0
        
        #Append the difference (a utilization) to the set of utilizations
        uSet.append(sumU - nextSumU)

        #Select the next utilization
        sumU = nextSumU

    #Append the final utilization
    uSet.append(sumU)

    #Return utilizations
    return uSet

def inflationExperimentCalculateAverageStats(expStatsArray, numberOfSamples):

    #Create average stats
    avgExpStats = breakdownUtilExpStats()

    #Calculate sums
    for i in range(0,numberOfSamples):
        # avgExpStats.scsUtilization += expStatsArray[i].scsUtilization
        avgExpStats.targetUtilization += expStatsArray[i].targetUtilization
        avgExpStats.allPeriodsLCM += expStatsArray[i].allPeriodsLCM
        avgExpStats.allTasksDbfSum += expStatsArray[i].allTasksDbfSum
        avgExpStats.percentTimeUnusedVarAdc += expStatsArray[i].percentTimeUnusedVarAdc
        avgExpStats.scalingRatio += expStatsArray[i].scalingRatio

    #Calc averages
    # avgExpStats.scsUtilization /= numberOfSamples
    avgExpStats.targetUtilization /= numberOfSamples
    avgExpStats.allPeriodsLCM /= numberOfSamples
    avgExpStats.allTasksDbfSum /= numberOfSamples
    avgExpStats.percentTimeUnusedVarAdc /= numberOfSamples
    avgExpStats.scalingRatio /= numberOfSamples

    #Return
    return avgExpStats

class breakdownUtilExpStats:

    def __init__(self,
        maxCtrlTaskUtil = 0,
        minCtrlTaskUtil = 0,
        targetUtilization = 0,
        allPeriodsLCM = 0,
        allTasksDbfSum = 0,
        percentTimeUnusedVarAdc = 0,
        scalingRatio = 0,
        nPeriodicTasks = 0,
        schedAnalysisTime = 0,
        schedulable = True):

            #Copy over information
            self.maxCtrlTaskUtil = copy.deepcopy(maxCtrlTaskUtil)
            self.minCtrlTaskUtil = copy.deepcopy(minCtrlTaskUtil)
            self.targetUtilization = copy.deepcopy(targetUtilization)
            self.allPeriodsLCM = copy.deepcopy(allPeriodsLCM)
            self.allTasksDbfSum = copy.deepcopy(allTasksDbfSum)
            self.percentTimeUnusedVarAdc = copy.deepcopy(percentTimeUnusedVarAdc)
            self.scalingRatio = copy.deepcopy(scalingRatio)
            self.nPeriodicTasks = copy.deepcopy(nPeriodicTasks)
            self.schedAnalysisTime = copy.deepcopy(schedAnalysisTime)
            self.schedulable = copy.deepcopy(schedulable)