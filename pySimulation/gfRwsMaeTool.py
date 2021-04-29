# General Function RWS MAE Tool

#Floor, Ceil, etc.
import math

#Exit
import sys

#Copy
import copy

#Timing the WCD call
import time

#Roll (shift an array) fxn
import numpy as np

#Random
import random

class gfRwsMaeTool:

    def __init__(self,p,f,W,SpSch,w,f_scalar,f_radix,f_offset,maximumValueAtReset):

        #Extract params
        #   Real-Time Task Period
        self.p = copy.deepcopy(p)
        #   General Function
        self.f = copy.deepcopy(f)
        #   WCET
        self.C = copy.deepcopy(W.C)
        self.B = copy.deepcopy(W.B)
        #   Super Schedule
        self.S = copy.deepcopy(SpSch.S)
        self.R = copy.deepcopy(SpSch.R)
        self.P = copy.deepcopy(SpSch.P)
        #   Demand Window
        self.a = copy.deepcopy(w.a)
        self.delta = copy.deepcopy(w.delta)

        #Calculate Params
        self.n = len(self.S)
        self.m = len(self.C)

        #WCD vars
        self.dbf = [-1]*2

        #Feasibility Constraints
        self.maximumValueAtReset = maximumValueAtReset

        #Runtime Stats
        self.msStart = [0]*2
        self.msEnd = [-1]*2

        #WCETS
        self.WCETS = [0]
        self.f_scalar = copy.deepcopy(f_scalar)
        self.f_radix = copy.deepcopy(f_radix)
        self.f_offset = copy.deepcopy(f_offset)

    #FUNCTIONS
    def incrementP(self,increment):

        #For each increment required...
        for i in range(0,increment):

            #Increment P
            self.P = self.P + 1

            #Pick an offset to increase
            randOffsetToIncrease = random.randint(1,self.n)

            #For every offset  larger than the selected offset...
            for j in range(randOffsetToIncrease,self.n):
                
                #If any offset other than the final offset (the offset which ends at P) is selected...
                if(j != self.n):

                    #Increment the offset
                    self.R[j] += 1

    #Calculate the dimension variables (n and m)
    def calcDimensions(self):

        #Dimension S
        self.n = len(self.S)

        #Dimension C
        self.m = len(self.C)
    
    #Calculate all WCDs
    def calcAllWCDs(self):

        #For all methods...
        for i in range(2):

            #Calculate wcd
            self.calcDbf(i,False)

    #Calculate worst
    def calcDbf(self,method,printCheckpoints):

        #Calculate problem dimensions
        self.calcDimensions()

        #Convert all timing variables to integer multiples of p
        self.makeIntegerMultiples()

        #Perform Feasibility Checks
        feasible = self.checkForFeasibility()
        if( feasible < 0):
            return feasible

        #Switch Executions depending on the method

        #If method 0 selected...
        if(method == 0):

            #Execute default GMF model approach...
            # print("GMF WCD...")
            self.msStart[method] = time.time() * 1000
            self.dbf[method] = self.GMF_DBF(print)
            self.msEnd[method] = time.time() * 1000

        # If method 1 selected...
        if(method == 1):

            #Calculate WCD using Exp. Stable Switched Control simulation (dbf)...
            self.msStart[method] = time.time() * 1000
            self.dbf[method] = self.RWS_MAE_DBF()
            self.msEnd[method] = time.time() * 1000

        #Calc Stats
        self.calcStats()

        # Return Result
        return self.dbf[method]

    #Switched Control, wcet sequence, dbf - O(nH lg nH)
    def RWS_MAE_DBF(self):
        
        #Calculate WCET Sequence
        WCETS = self.calcWcetSequence()

        #Create possible subarrays
        self.RWS_MAE_DBF_table = [0]*self.P

        #Initialize sums
        sumWcet = [0]*self.n

        #For each delta of length d... O(H)
        for d in range(0,len(WCETS)):

            maxDemand = 0

            #For each setpoint update... O(n)
            for s in range(0, self.n):

                #Calculate index to access
                index = ((self.R[s]-d-1)%self.P)

                #Calculate execution time
                sumWcet[s] += WCETS[index]

                #If the summed execution time is greater than the current max time for this delta...
                if(sumWcet[s] > maxDemand):

                    #Update the max
                    maxDemand = sumWcet[s]
            
            #Insert into possible demand list
            self.RWS_MAE_DBF_table[d] = maxDemand

        #Determine how many hyperperiods are included
        numHyperperiods = math.floor(self.delta / self.P)

        #Determine the remainder
        deltaRemaining = self.delta % self.P

        #Calculate hyperperiod demand
        self.fullHyperperiod_RWS_MAE_DBF = math.fsum(WCETS)

        #Total hyperperiod demand
        totalHyperperiodDemand = self.fullHyperperiod_RWS_MAE_DBF * numHyperperiods

        #If remamining time is greater than zero...
        if(deltaRemaining > 0):

            #Get the demand for the delta remaining
            self.partialMaxDemand_RWS_MAE_DBF = self.RWS_MAE_DBF_table[deltaRemaining-1]

        #otherwise...
        else:

            #Set the partial demand to zero
            self.partialMaxDemand_RWS_MAE_DBF = 0

        #Convert to WCD
        self.totalDemand_RWS_MAE_DBF = totalHyperperiodDemand + self.partialMaxDemand_RWS_MAE_DBF

        #Create global DBF var
        self.dbf_RWS_MAE_DBF = self.RWS_MAE_DBF_table

        #Return
        return self.totalDemand_RWS_MAE_DBF

    #GMF Calculation - O(H^2 lg H)
    def GMF_DBF(self,printCheckpoints):

        #Calculate WCET Sequence - O(H)
        WCETS = self.calcWcetSequence()

        #Create possible subarrays
        self.GMF_DBF_table = ()
        self.GMF_DBF_table = list(self.GMF_DBF_table)

        #Copy WCETS in series
        WCETStimesTwo = WCETS*2

        #Execute GMF Alg

        #For each frame... O(H)
        for i in range(0,len(WCETS)):

            if(i%100 == 0 and printCheckpoints):

                print("Calculating Frame:",str(i)," of ", str(len(WCETS)))

            summedExecutionTime = 0

            #For each number of consecutive frames... O(H)
            for j in range(0, len(WCETS)):

                #Calculate execution time
                summedExecutionTime += WCETStimesTwo[i+j]
                #Calculate interval time
                interval = j+1
                #Insert into possible demand list
                self.GMF_DBF_table.insert(0,(summedExecutionTime,interval))

        #Remove Duplicates - O(H^2)
        self.GMF_DBF_table = list(set([i for i in self.GMF_DBF_table]))

        #Sort Possible Demands by workload (descending) - O(H^2 lg H^2) => O(H^2 * 2 * lg H) => O(H^2 lg H)
        self.GMF_DBF_table = sorted(self.GMF_DBF_table,key = lambda x : x[0], reverse = True)

        #Sort Possible Demands by interval length (ascending) O(lg H^2)
        self.GMF_DBF_table = sorted(self.GMF_DBF_table,key = lambda x : x[1])

        #Setup entry scanner
        i = 1

        #While not all entries scanned... O(H^2)
        while(i < len(self.GMF_DBF_table)):

            #If the previous entry has the same distance but smaller workload...
            if( self.GMF_DBF_table[i][1] == self.GMF_DBF_table[i-1][1]):

                #If the previous entry also has a larger or equal workload value...
                if( self.GMF_DBF_table[i][0] <= self.GMF_DBF_table[i-1][0]):

                    #Mark the entry for deletion
                    self.GMF_DBF_table.pop(i)

                    #Decrement i since we lost an item
                    i = i - 1

            #Increase i
            i = i + 1

        #Determine how many hyperperiods are included
        numHyperperiods = math.floor(self.delta / self.P)

        #Determine the remainder
        deltaRemaining = self.delta % self.P

        #Calculate hyperperiod demand
        self.fullHyperperiod_GMF_DBF = math.fsum(WCETS)

        #Total hyperperiod demand
        totalHyperperiodDemand = self.fullHyperperiod_GMF_DBF * numHyperperiods

        #If remamining time is greater than zero...
        if(deltaRemaining > 0):

            #Get the demand for the delta remaining
            self.partialMaxDemand_GMF_DBF = self.GMF_DBF_table[deltaRemaining-1][0]

        #otherwise...
        else:

            #Set the partial demand to zero
            self.partialMaxDemand_GMF_DBF = 0

        #Convert to WCD
        self.totalDemand_GMF_DBF = totalHyperperiodDemand + self.partialMaxDemand_GMF_DBF

        #Create Global DBF Var
        self.dbfGmf = self.GMF_DBF_table

        #Return
        return self.totalDemand_GMF_DBF

    def calcStats(self):

        #Calculate time taken
        self.computationTime = [0]*2

        #For each wcd calc...
        for i in range(0,len(self.dbf)):

            #If WCD is negative...
            if(self.dbf[i] < 0):

                #Compute nothing
                continue
            
            #Otherwise...
            else:

                #Calculate the computation time...
                self.computationTime[i] = self.msEnd[i] - self.msStart[i]

    def calcWcetSequence(self):

        #Calculate number of Jobs
        numJobs = self.P

        #Create array for storing WCET
        self.WCETS = [0]*numJobs

        #For each job release
        for i in range(0,numJobs):

            # Find starting value
            startingValue = self.getStartingValue(i)

            # Get Time Since Reset
            timeSinceReset = self.getTimeSinceReset(i)

            # Calculate Instantaneous Driving Function Value
            instantaneousDrivingFunctionValue = self.f(startingValue + timeSinceReset)

            # Find WCET of job given driving fxn value
            wcet = self.getWcetForValue(instantaneousDrivingFunctionValue)

            # Log 
            self.WCETS[i] = wcet

        return self.WCETS

    def printStats(self):

        print("WCD Results")
        print("GMF: ",self.dbf[0])
        print("RWS-MAE-DBF: ",self.dbf[1])
        print("Computation Time: ")
        print("GMF: ",self.computationTime[0])
        print("RWS-MAE-DBF: ",self.computationTime[1])

    #Return
    def getPercentOfNaive(self):
        return self.pctOfNaive

    #Return computation time array
    def getComputationTime(self):
        return self.computationTime

    def printParams(self):

        print("WCET Boundaries and Values:")
        print("C:", self.C)
        print("B:", self.B)

        print("Super Schedule:")
        print("S:",self.S)
        print("R:",self.R)
        print("P:",self.P)

        print("Demand Window:")
        print("a:",self.a)
        print("delta:",self.delta)

        print("Real-Time Task:")
        print("p:",self.p)

    #Determine whether analysis is feasible
    def checkForFeasibility(self):

        #Assume there's no problem
        violatesMaximumValueAtReset = False

        #Check if value of F is below required value at end of each sequence
        for i in range(0,self.n):

            #If index is last index...
            if(i==self.n-1):

                #Determine if F is below required value
                if(self.f(self.S[i] + self.P - self.R[i]) > self.maximumValueAtReset):

                    #Flag violation
                    violatesMaximumValueAtReset = True

            #Otherwise...
            else:

                #Determine if F is below required value
                if(self.f(self.S[i] + self.R[i+1] - self.R[i]) > self.maximumValueAtReset):

                    #Flag violation
                    violatesMaximumValueAtReset = True

            #If violation flagged...
            if(violatesMaximumValueAtReset):

                # Return error
                return -8

        #The largest value of F is within the boundaries
        if(self.f(0) > self.B[self.m]):

            # Return error
            return -12

        #Check that s_i < s_{i-1 % P} + r_i - r_{i-1 % P}
        violatesMaxStartingValue = False

        #For every starting value
        for i in range(0,self.n):

            #If first index is being searched
            if(i == 0):
                
                if(self.S[i] > self.S[(i-1)%(self.n)] + self.P-self.R[i]):

                    #Flag as violation
                    violatesMaxStartingValue = True

            #Otherwise...
            else:

                #If starting value is greater than last starting value plus time between...
                if(self.S[i] > self.S[(i-1)%self.n] + self.R[i] - self.R[(i-1)%self.n]):

                    #Flag as violation
                    violatesMaxStartingValue = True

        # If any case in the loop violated the max starting value...
        if(violatesMaxStartingValue):

            # Return error
            return -9


        #   P too Large (taxing for GMF DBF)
        if(self.P > 1000):

            # Return error
            return -10
        
        #   P too small
        if(self.P <= 0):

            # Return Error
            return -13

        #No other errors to check
        return 0

    #Convert all time-based variables to integer multiples of p
    def makeIntegerMultiples(self):

        #If p is not 1
        if(self.p != 1):

            #Scale all period-based and time-based variables accordingly
            for i in range(0,self.m):
                
                #WCET
                self.C[i] = round(self.C[i]/self.p,3)

            #Scale 
            for i in range(0,self.n):
                
                #Offset
                self.R[i] = math.ceil(self.R[i]/self.p)

            #Scale hyperperiod to nearest integer multiple
            self.P = math.ceil(self.P/self.p)

            #Scale Delta to nearest Integer multiple (use floor because this won't decrease demand)
            self.delta = math.floor(self.delta/self.p)

            #Scale period to 1
            self.p = math.ceil(self.p/self.p)

    #Index Fxn
    def getStartingIndex(self,t):

        #Calculate the remainder
        remainder = t%self.P

        #For every pair of offsets (not including the last offset and hyperperiod)...
        for i in range(0,self.n-2+1):

            #If t%P is between two offsets...
            if(self.R[i] <= remainder and remainder < self.R[(i+1)]):

                #Return the first of the two offsets
                return i
        
        #Check the final offset and hyperperiod
        if(self.R[self.n-1] <= remainder and remainder < self.P):

            #Return the last offset (before the hyperperiod)
            return self.n-1

    #Starting Value Function
    def getStartingValue(self,t):
        
        #Get the current starting index
        startingIndex = self.getStartingIndex(t)

        #Get the current starting value
        startingValue = self.S[startingIndex]

        #Return the starting value
        return startingValue

    #Get time since last reset time
    def getTimeSinceReset(self,t):

        #Create return value
        retVal = 0

        #Get starting value index
        startingValueIndex = self.getStartingIndex(t)

        if(startingValueIndex == -1):

            retVal = -1

        else:

            #Get last reset time value
            lastResetTimeValue = self.R[startingValueIndex]

            #Get number of superperiods to subtract
            superperiodToSubtract = math.floor(t / self.P) * self.P

            #Calculate time since reset
            timeSinceReset = t - lastResetTimeValue - superperiodToSubtract

            #Assign Return Value
            retVal = timeSinceReset

        #Return the value
        return retVal
    
    #WCET of value
    def getWcetForValue(self,value):

        #Get boundary index
        bIndex = self.boundaryIndex(value)

        #Return the WCET
        return self.C[bIndex]

    #Boundary index of value
    def boundaryIndex(self,value):

        #For pair of boundaries...
        for i in range(0,len(self.B)-1):

            #If value is zero, return highest WCET
            if(value == 0):
                return 0

            #if the value is between the pair of boundaries...
            if(self.B[i] < value and value <= self.B[i+1]):

                #return the index of the smaller boundary
                return i
