#Imports
#   Import general RWS MAE fxns
import gfRwsMaeGeneral as GF_RWS_MAE_GEN
#   Import PRNG
import random
#   Import floor, ceil, gcd
import math
#   Import deepcopy
import copy

#Generate Control Task
(randomRwsTask, randomRwsTaskGenerationStats) = GF_RWS_MAE_GEN.generateRandomFeasibleRwsTask(
    1,
    10,
    -1,
    -1, 
    1, 
    100, 
    1000,
    1,
    100)

#Calculate utilization using only highest WCET
scsUtil = randomRwsTask.C[0]/randomRwsTask.p

#Assign highest-WCET Util of RWS Task as target utilization for UUNIFAST
targetUtil = 1 - scsUtil

#Pick number of additional, periodic tasks
nTasks = random.randint(0,5)

#Generate Utilizations using UUNIFAST

#Establish set of utilizations
uSet = []

#Establish target utilization
sumU = targetUtil

#For each task
for i in range(1, nTasks):

    #Assume the task has an invalid utilization
    valid = 0

    #While the utilization is invalid
    while(not valid):

        #Generate a utilization
        nextSumU = sumU * random.random() ** (1.0 / (nTasks - i))

        #Check if the utilization is valid
        valid = nextSumU > 0
    
    #Append the difference (a utilization) to the set of utilizations
    uSet.append(sumU - nextSumU)

    #Select the next utilization
    sumU = nextSumU

#Append the final utilization
uSet.append(sumU)

#Assert all task sums plus equals target util
uSum = sum(uSet)
assert(uSum == targetUtil)

#Create array of periods, WCETs
cSet = []
pSet = []

#Generate Random Periods for the utilizations
for i in range(1,nTasks):

    #Generate random period in range 0 to twice the RWS task super period
    pRand = math.floor(random.random()*2*randomRwsTask.P)

    #Append to pSet
    pSet.append(pRand)

    #Generate corresponding WCETs
    cSet.append(uSet[i] * pRand)

#Print all
print(uSet,cSet,pSet)

#Create array of all periodic periods and RWS major period
allPeriods = copy.deepcopy(pSet)
allPeriods.append(randomRwsTask.P)

#Calculate LCM of all periodic periods and RWS major period
apLcm = allPeriods[0]
for i in allPeriods[1:]:
  apLcm = apLcm*i//math.gcd(apLcm, i)

#Assert LCM is actually LCM
for i in range(0,len(allPeriods)):
    assert(apLcm % allPeriods[i] == 0)

#Create DBF function of each periodic task
def dbf(c,p,t):

    #Calculate demand
    d = math.floor(t/p)*c

    #Return
    return d

#Create DBF array
dbfSet = []

#Calculate DBF of all periodic functions up to hyperperiod (apLcm)
for i in range(0,nTasks-1):

    #Append DBF
    dbfSet.append(dbf(cSet[i],pSet[i],apLcm))

#Calculate DBF of RWS
randomRwsTask.delta = apLcm
randomRwsTask.calcDbf(1,True)
randomRwsTask.calcDbf(0,True)
dbfSet.append(randomRwsTask.dbf[1])

#Compare calculation times
#   Get Computation Time
compTime = randomRwsTask.getComputationTime()
#   Compare computation times
timeDifference = compTime[0]-compTime[1]

print(round(timeDifference,2),"ms saved with RWS-MAE-DBF")
print(1-(compTime[1]/compTime[0])*100,"% improvement")
print(compTime[0]/compTime[1],"times faster")
#Sum all DBF
sumDbf = sum(dbfSet)

#Calculate pct time used
pctTimeUsed = sumDbf / apLcm

#Calculate ratio
scalingRatio = apLcm / sumDbf

print(apLcm,": Period LCM")
print(round(pctTimeUsed*100,2),"% of all periods LCM used")
print("WCETs may be scaled by ",round(scalingRatio,2),"times")

print("Done")