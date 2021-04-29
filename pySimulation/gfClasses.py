# Generic Function RWS MAE Classes

# These classes are taken from definitions in the paper

#Imports
import copy

#WCET vs Tracking Error Class
class randomRwsTaskWcet:

    def __init__(self,wcets,boundaries):
        self.C = copy.deepcopy(wcets)
        self.B = copy.deepcopy(boundaries)

#Super Schedule Class
class superSchedule:

    def __init__(self,seqOfSetpoints,seqOfOffsets,hyperPeriod):
        self.S = copy.deepcopy(seqOfSetpoints)
        self.R = copy.deepcopy(seqOfOffsets)
        self.P = copy.deepcopy(hyperPeriod)

#Demand Window Class
class demandWindow:

    def __init__(self,offset,windowSize):
        self.a = copy.deepcopy(offset)
        self.delta = copy.deepcopy(windowSize)