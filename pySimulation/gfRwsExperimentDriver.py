#Generic Function RWS Driver

#Import random generator
import gfRwsMaeRandGen as GF_RWS_MAE_RANDGEN

#Import general RWS MAE fxns
import gfRwsMaeGeneral as GF_RWS_MAE_GEN

#Import experiment configurations / parameters
import gfRwsMaeExperimentClassesAndSetup as GF_RWS_MAE_EXPSETUP

#Initialize Experiment Setups
#   Simple DBF calculation experiment setup array
dbfExperimentSetups = GF_RWS_MAE_EXPSETUP.initializeDbfExperiments()
#   Inflation Experiments for combining RWS tasks with UUNIFAST generated tasks
inflationExperimentSetups = GF_RWS_MAE_EXPSETUP.initializeInflationExperiments()
#   Slight Variation Experiments
slightVariationExperimentSetups = GF_RWS_MAE_EXPSETUP.initializeSlightVariationExperiments()

#Create experiment run flags to run experiments when driver file (this file) is executed
wcdExperimentRunFlags = [0,0,0,0,0,0,0]
inflationExperimentRunFlags = [1,0,0]
slightVariationExperimentRunFlags = [0]

#Exectute requested experiments
#   Run experiment 1
if(wcdExperimentRunFlags[0]):
    
    #Experiment #1: 10k randomly generated tasks with default params
    print(">> Experiment #1 <<")

    #Generate
    GF_RWS_MAE_RANDGEN.feasibleRwsMaeTaskGenerator_ExpSetup(dbfExperimentSetups[0])

#   Run experiment 2
if(wcdExperimentRunFlags[1]):

    #Experiment #2: 10 randomly generated tasks for each fixed values of n
    print(">> Experiment #2 <<")

    #Configure the start and end values of the loop
    nStart = 10
    nEnd = 16

    #For each particular number of reset times...
    for i in range(nStart,nEnd):

        #Assign the number of setpoints
        dbfExperimentSetups[1].numResetTimesLowerBound = i
        dbfExperimentSetups[1].numResetTimesUpperBound = i

        #Generate amd execute
        GF_RWS_MAE_RANDGEN.feasibleRwsMaeTaskGenerator_ExpSetup(dbfExperimentSetups[1])

#   Run experiment 3
if(wcdExperimentRunFlags[2]):

    #Experiment #3: Fixed parameters with increasing P (deltaP = 100 each time) (distributing the extra time randomly across reset times)
    print(">> Experiment #3 <<")

    #Generate amd execute
    GF_RWS_MAE_RANDGEN.feasibleRwsMaeTaskGenerator_ExpSetup(dbfExperimentSetups[2])

#   Run experiment 4
if(wcdExperimentRunFlags[3]):

    #Experiment #4: Fixed parameters with increasing P (deltaP = 50 each time) (distributing the extra time randomly across reset times)
    print(">> Experiment #4 <<")

    #Generate amd execute
    GF_RWS_MAE_RANDGEN.feasibleRwsMaeTaskGenerator_ExpSetup(dbfExperimentSetups[3])

#   Run experiment 5
if(wcdExperimentRunFlags[4]):

    #Experiment #5: Fixed parameters with increasing P (deltaP = 5 each time) (distributing the extra time randomly across reset times)
    print(">> Experiment #5 <<")

    #Generate amd execute
    GF_RWS_MAE_RANDGEN.feasibleRwsMaeTaskGenerator_ExpSetup(dbfExperimentSetups[4])

#   Run experiment 6
if(wcdExperimentRunFlags[5]):

    #Experiment #6: Randomized parameters with increasing P (deltaP = 100 each time).
    print(">> Experiment #6 <<")

    #Generate amd execute
    GF_RWS_MAE_RANDGEN.feasibleRwsMaeTaskGenerator_ExpSetup(dbfExperimentSetups[5])

#   Run experiment 7
if(wcdExperimentRunFlags[6]):

    #Experiment #7: 10k random. Requires f(x) to reach value of 1/2 the highest WCET range
    print(">> Experiment #7 <<")

    #Generate amd execute
    GF_RWS_MAE_RANDGEN.feasibleRwsMaeTaskGenerator_ExpSetup(dbfExperimentSetups[6])

#   Run experiment 8
if(inflationExperimentRunFlags[0]):

    #Experiment #8: Generate RWS task. Calculate scaling ratio of random RWS Task with UUNIFAST-generated periodic tasks with varying utilization [1-c_{m-1},1-c_0]. Perform schedulability analysis.
    (randomRwsTask, randomRwsTaskGenerationStats, (cSet,pSet, uSet), expStats, avgExpStats) = GF_RWS_MAE_RANDGEN.inflationExperimentRunner_ExpSetup(inflationExperimentSetups[0])

#   Run experiment 9
if(inflationExperimentRunFlags[1]):

    #Experiment 9: Generate RWS task. Calculate scaling ratio of random RWS Task with UUNIFAST-generated periodic tasks with varying utilization [1-c_{m-1},1-c_0].  Perform schedulability analysis.
    (randomRwsTask, randomRwsTaskGenerationStats, (cSet,pSet, uSet), expStats, avgExpStats) = GF_RWS_MAE_RANDGEN.inflationExperimentRunner_ExpSetup(inflationExperimentSetups[1])

#   Run experiment 10
if(inflationExperimentRunFlags[1]):

    #Experiment 10: Generate RWS task. Calculate scaling ratio of random RWS Task with UUNIFAST-generated periodic tasks with varying utilization [1-c_{m-1},1-c_0]. Perform schedulability analysis.
    (randomRwsTask, randomRwsTaskGenerationStats, (cSet,pSet, uSet), expStats, avgExpStats) = GF_RWS_MAE_RANDGEN.inflationExperimentRunner_ExpSetup(inflationExperimentSetups[2])

#   Run experiment 11
if(slightVariationExperimentRunFlags[0]):

    #Experiment 11: Generate random, feasible RWS task whose parameters may be slightly varied and still represent a feasible RWS task. Compare DBF/P calculations.
    retVal = GF_RWS_MAE_RANDGEN.slightVariantExperimentRunner_ExpSetup(slightVariationExperimentSetups[0])