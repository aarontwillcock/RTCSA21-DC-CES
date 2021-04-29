
# Imports
#   RWS Classes
import gfClasses
#   RWS Tools
import gfRwsMaeTool
#   Exp, e
import math

#Print Experiment
print("\nExperiment: Case Study Experiment")

#Create Driving function (derived from control law / tracking error)
f_radix = math.e
f_scalar = 120
f_offset = -0.01881285
f_emp = lambda a : f_scalar * math.pow(f_radix,f_offset*a)

#Create sampling period (ms)
p_emp = 18

#WCET Boundaries and Values
C_emp = [14.0,6.0,5] #ms
B_emp = [0,10,45,180] #degrees

#Create WCET Boundary Class
W_emp = gfClasses.randomRwsTaskWcet(C_emp,B_emp)

#Create Starting Values, Reset Times, Super Period
S_emp = [0,0]  #degrees
A_emp = [0,60*18]   #ms
P_emp = (60+90)*18 #ms Why? (120+180+80)*18ms

#Create Super Schedule
SpSched_emp = gfClasses.superSchedule(S_emp,A_emp,P_emp)

#Create offset, window size
a_emp = 0
delta_emp = P_emp #Demand window is one hyperperiod

#Create Demand Window
w_emp = gfClasses.demandWindow(a_emp,delta_emp)

#Create RWS Tool using period, driving function, WCET Function, Super Schedule, demand window, diagnistic parameters about driving function
empRwsMaeTool = gfRwsMaeTool.gfRwsMaeTool(p_emp,f_emp,W_emp,SpSched_emp,w_emp,f_scalar,f_radix,f_offset,1000)

#Create WCD array
dbf = [0]*2

#Calculate DBF using GMF and RWS-MAE-DBF
dbf[0] = empRwsMaeTool.calcDbf(0,True)
dbf[1] = empRwsMaeTool.calcDbf(1,True)

#Assert calculation is correct to 4 decimals
assert(round(dbf[0],4) == round(dbf[1],4))

#Print parameters
empRwsMaeTool.printParams()

#Print stats
print("Algorithm (type) - Table Build Time - Search Time - Asymp. - Average Computation Times (ms): ",)
print("-----------------------------------")
print("GMF         (dbf)   - O(H^2 lg H)        - O(1)               : ",empRwsMaeTool.getComputationTime()[0])
print("RWS-MAE-DBF (dbf)   - O(nH) + O(H lg H)) - O(1)               : ",empRwsMaeTool.getComputationTime()[1])
print("===================================")
print("Algorithm (type) - Average % Improvement: ",)
print("-----------------------------------")
print("GMF         (dbf)   : ",-1*((empRwsMaeTool.getComputationTime()[0] - empRwsMaeTool.getComputationTime()[0])/empRwsMaeTool.getComputationTime()[0])*100)
print("RWS-MAE-DBF (dbf)   : ",-1*((empRwsMaeTool.getComputationTime()[1] - empRwsMaeTool.getComputationTime()[0])/empRwsMaeTool.getComputationTime()[0])*100)
print("===================================")