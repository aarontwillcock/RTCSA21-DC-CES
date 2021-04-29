# Demand Characterization of CPS with Conditionally-Enabled Sensors

## A Fast Overview

1. This repository contains supporting material for the paper "Demand Characterization of CPS with Conditionally-Enabled Sensors".
2. The information in this repository covers, at a high level, the simulator and robot arm used to support the paper.
3. The information in this repository is not intended to be comprehensive - not all function descriptions or experiments are described due to time limitations.

## Acknowledgments

<table width="100%" style="text-align: center" cellpadding="20">
  <tr>
    <td style="vertical-align:middle">
        <a href="https://www.nsf.gov">
            <img src="https://www.nsf.gov/images/logos/NSF_4-Color_bitmap_Logo.png" alt="NSF" height="100px"/>
        </a>
    </td>
    <td style="vertical-align:middle">
        <a href="https://vt.edu">
            <img src="https://www.assets.cms.vt.edu/images/HorizontalStacked/HorizontalStacked_RGB.svg" height="63px"/>
        </a>
    </td>
    <td style="vertical-align:middle">
        <a href="https://wayne.edu">
            <img src="https://mac.wayne.edu/images/wsu_primary_horz_color.png" height="50px"/>
        </a>
    </td>
  </tr>
</table> 

This research has been supported in part by the [US National Science  Foundation](https://www.nsf.gov/).

## Authors - Contact

| Author | Department | University | Location | Email |
| ------ | ---------- | ---------- | -------- | ----- |
| [Aaron Willcock](https://www.linkedin.com/in/aaronwillcock/) | Computer Science | [Wayne State University](https://wayne.edu/) | Detroit, MI, USA | aaron.willcock@wayne.edu |
| [Nathan Fisher](https://engineering.wayne.edu/profile/dx3281) | Computer Science | [Wayne State University](https://wayne.edu/) | Detroit, MI, USA | fishern@wayne.edu |
| [Thidapat Chantem](https://ece.vt.edu/people/profile/chantem) | Electrical and Computer Engineering | [Virginia Tech](https://vt.edu/index.html) | Arlington, VA, USA | tchantem@vt.edu |

## Table of Contents
- [Demand Characterization of CPS with Conditionally-Enabled Sensors](#demand-characterization-of-cps-with-conditionally-enabled-sensors)
  - [A Fast Overview](#a-fast-overview)
  - [Acknowledgments](#acknowledgments)
  - [Authors - Contact](#authors---contact)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Dependencies](#dependencies)
  - [Quickstart: Simulation + Robot](#quickstart-simulation--robot)
    - [Quickstart: Run Simulation](#quickstart-run-simulation)
      - [10k Task Simulation](#10k-task-simulation)
      - [Case Study Simulation](#case-study-simulation)
  - [How to Use This Repository](#how-to-use-this-repository)
    - [Reviewing Source Code](#reviewing-source-code)
    - [Executing Source Code](#executing-source-code)
    - [Folder and File Explanation](#folder-and-file-explanation)
  - [Customizing Simulation](#customizing-simulation)
    - [Enabling Other Experiments](#enabling-other-experiments)
    - [Changing Experiment Values](#changing-experiment-values)

## Features

1. A Python3 implementation of:
   1. the Repeating WCET Sequence of Monotonic Ascending Execution DBF function presented in the paper (`pySimulation/gfRwsMaeTool.py` function `RWS_MAE_DBF()`).
   2. the Generalized Multiframe Model applied to Repeating WCET Sequences of Monotonic Ascending Execution (`pySimulation/gfRwsMaeTool.py` function `GMF_DBF()`).
2. An Arduino implementation of:
   1. a robot arm demonstrating conditionally-enabled sensors (`ceras/ceras.ino`).
3. The source data used in the paper submission (`pubdata/*`)

## Dependencies

The following libraries and programs are required to execute the simulation or robot code:

1. Programs
   1. [Arduino IDE](https://www.arduino.cc/en/software) - Deploying Arduino code for the robot arm
   2. [Python 3.8.5](https://www.python.org/downloads/) - Running simulations
2. Libraries (Arduino)
   1. [MPU6050](https://github.com/ZHomeSlice/Simple_MPU6050) - Interfacing with the MPU6050 and its onboard Digital Motion Processor (DMP)
   2. [FreeRTOS Arduino Library](https://www.arduino.cc/reference/en/libraries/freertos/) a port of [FreeRTOS](https://www.freertos.org/) - Enabling Real-Time control on Arduino
   3. [i2cdevlib](https://github.com/jrowberg/i2cdevlib) - Interfacing with the MPU6050 over Inter-Integrated Circuit (I2C)

## Quickstart: Simulation + Robot

Reviewers are encouraged to:

1. read and execute the `gfRwsExperimentDriver.py` file to simulate 10,000 tasks and
2. read the `ceras.ino` file to see how the Aruino was programmed.

If you wish to customize experiments to run, please see [Customizing Simulation](#customizing-simulation).

### Quickstart: Run Simulation

#### 10k Task Simulation

The 10k task simulation may be run by executing `python3 gfRwsExperimentDriver.py` in the `pySimulation/` directory.

The simulation will print to terminal:
1. indications for the number of tasks generated (runs), and
2. the approximate frame number being calculated when executing the GMF DBF. 

The results will be stored in a `*.csv` file located in `pySimulation/data`.

#### Case Study Simulation

The repeating WCET sequence generated by the conditionally-enabled sensors on the robot arm may be created and have its DBF calculated by executing `python3 gfRwsMaeCaseStudy.py` in the `pySimulation/` directory.

The results will be printed to the terminal.

## How to Use This Repository

### Reviewing Source Code

The various tasks used to generate the paper figures and support the claim of RWS-MAE-DBF being faster than the GMF DBF are supported by the code contained within.
We encourage reviewers to read through the `pySimulation/` folder especially the files:

1. `gfClasses.py` which defines the properties of the repeating WCET sequence tasks as provided by the paper,
2. `gfRwsExperimentDriver.py` which sets up and executes the experiments, placing logged data in the `pySimulation/data/` folder,
3. `gfRwsMaeRandGen.py` which provides function for generating random tasks (composed of driving functions, WCET boundaries, etc.) and determines whether they break constraints established in the paper before testing them,
4. `gfRwsMaeTool.py` which lists various functions to store and calculate the DBF of generated tasks, and
5. `gfRwsMaeGeneral.py` which provides the interface for generating tasks with different conditions

### Executing Source Code

The source code may be run by either:
1. following the [Quickstart: Run Simulation](#quickstart-run-simulation) steps OR
2. following the [Customizing Simulation](#customizing-simulation) steps

### Folder and File Explanation

```txt
Demand Characterization of CPS with Conditionally-Enabled Sensors
├── ceras                                               Folder for Arduino implementation  
│   └── ceras.ino                                           Arduino implementation of conditionally-enabled sensors
├── pubData                                             Folder for data used in the paper  
|   └── gfRwsMaeCaseStudy-2021-03-03-08-12-50.txt           Provides output values for the case study
│   └── gfRwsMaeExpInf0-2021-04-28-18-11-00.csv             Provides output values for the 10,000 simulated tasks
├── pySimulation                                        Folder for Python3 Simulation files
│   └── gfClasses.py                                        Defines classes representing equations in the paper (i.e. WCET boundaries and WCET values) 
│   └── gfRwsExperimentDriver.py                            Initializes and executes experiments
│   └── gfRwsMaeCaseStudy.py                                Creates a repeating WCET sequence representing the Arduino robot arm and executes the RWS-MAE-DBF and GMF DBF calculations using the task
│   └── gfRwsMaeExperimentClassesAndSetup.py                Lists configurations for different experiments
│   └── gfRwsMaeGeneral.py                                  Provides functions for generating random, feasible repeatable WCET sequence tasks
│   └── gfRwsMaeInflationComparison.py                      Standalone experiment for calculating scaling ratios of repeatable WCET sequence tasks alongside periodic tasks generated using UUNIFAST.
│   └── gfRwsMaeRandGen.py                                  Provides functions for generating random repeatable WCET sequence tasks and assessing feasibility
│   └── gfRwsMaeTool.py                                     Provides tools for calculating DBF of repeatable WCET sequence tasks and logging information about the tasks
├── README.md                                           This document (a README)
```

## Customizing Simulation

The simulation may be customized by editing the files `gfRwsExperimentDriver.py` and `gfRwsMaeExperimentClassesAndSetup.py` as follows:

### Enabling Other Experiments

Lines 21-23 of `gfRwsExperimentDriver.py` provide arrays of _flags_ that indicate which experiments will be run when calling `python3 gfRwsExperimentDriver.py` in the `pySimulation/` folder.

The lines, by default, are:

```python3
wcdExperimentRunFlags = [1,0,0,0,0,0,0]
inflationExperimentRunFlags = [0,0,0]
slightVariationExperimentRunFlags = [0]
```
By changing any of the `0`s in the arrays to `1`s, the corresponding experiment listed in `gfRwsMaeExperimentClassesAndSetup.py` will be configured and run when calling `python3 gfRwsExperimentDriver.py` in the `pySimulation/`.

The experiment descriptions for each flag are provided in comments inside `gfRwsExperimentDriver.py` and repeated here:

1. wcdExperimentRunFlags
   1. Flag 0 - Experiment #1: 10k randomly generated tasks with default params (no periodic tasks generated alongside)
   2. Flag 1 - Experiment #2: 10 randomly generated tasks for each fixed value of n from 10 to 16 (no periodic tasks generated alongside)
   3. Flag 2 - Experiment #3: Fixed parameters with increasing P (deltaP = 100 each time) (distributing the extra time randomly across reset times) (no periodic tasks generated alongside)
   4. Flag 3 - Experiment #4: Fixed parameters with increasing P (deltaP = 50 each time) (distributing the extra time randomly across reset times) (no periodic tasks generated alongside)
   5. Flag 4 - Experiment #5: Fixed parameters with increasing P (deltaP = 5 each time) (distributing the extra time randomly across reset times) (no periodic tasks generated alongside)
   6. Flag 5 - Experiment #6: Fixed values of P with randomized other values (no periodic tasks generated alongside)
   7. Flag 6 - Experiment #7: 10k random. Requires f(x) to reach value of 1/2 the highest WCET range (no periodic tasks generated alongside)
2. inflationExperimentRunFlags
   1. Flag 0 - #Experiment #8: Generate RWS task with larger num reset times. Calculate scaling ratio of random RWS Task with UUNIFAST-generated periodic tasks with varying utilization [1-c_{m-1},1-c_0]. Perform schedulability analysis.
   2. Flag 1 - #Experiment #9: Generate RWS task with smaller num reset times. Calculate scaling ratio of random RWS Task with UUNIFAST-generated periodic tasks with varying utilization [1-c_{m-1},1-c_0].  Perform schedulability analysis.
   3. Flag 2 - #Experiment #10: Generate RWS task with varied num reset times. Calculate scaling ratio of random RWS Task with UUNIFAST-generated periodic tasks with varying utilization [1-c_{m-1},1-c_0]
3. slightVariationExperimentRunFlags
   1. Flag 0 - Experiment #11: Generate random, feasible RWS task whose parameters may be slightly varied and still represent a feasible RWS task. Compare DBF calculations.

### Changing Experiment Values

To edit the experiments and introduce your own values, the file `gfRwsMaeExperimentClassesAndSetup.py` must be edited as follows.

Consider the default Experiment #1 configuration:

```python3
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
```
The parameters listed are described below:
1.  `numSamples` indicates how many tasks will be generated
2.  `numResetTimesLowerBound` indicates the minimum number of jobs allowed between consecutive reset times. Lowering this number produces shorter WCET sequences on average. 
    1.  A value of `-1` adopts the default value provided by the generator, `numResetTimesLowerBound = 1`.
3.  `numResetTimesUpperBound` indicates the maximum number of jobs allowed between consecutive reset times. Raising this number produces longer WCET sequences on average. A value of `-1` adopts the default value provided by the generator, `numResetTimesUpperBound = 10`.
4.  `numWcetsLowerBound` indicates the minimum number of unique WCETs in the task definition.
    1.  A value of `-1` adopts the default value provided by the generator, `numWcetsLowerBound = 1`.
5.  `numWcetsUpperBound` indicates the maximum number of unique WCETs in the task definition. 
    1.  A value of `-1` adopts the default value provided by the generator, `numWcetsUpperBound = 10`.
6.  `utilizationLowerBound` indicates the minimum utilization of an individual WCET compared to a period `p=1`.
    1.  A value of `-1` adopts the default value provided by the generator, `utilizationLowerBound = 1`.
7.  `utilizationUpperBound` indicates the minimum utilization of an individual WCET compared to a period `p=1`.
    1.  A value of `-1` adopts the default value provided by the generator, `utilizationUpperBound = 100`.
8.  `fileName` indicates the base file name. The date and time of the experiment run will be appended to the file name such as `fileName-2021-03-03.csv` for a simulation run on March 3rd, 2021.
9.  `fixedVars` indicates whether the experiment requires fixing particular variables.
    1.  A value of `0` indicates no variables are fixed.
    2.  A value of `1` instructs the generator to run only a fixed set of values defined by `startP` and `endP`. The generator will select a RWS MAE task with super period `P = startP` with all other parameters randomized. The generator then repeatedly increases the value of `P` by `deltaP` until `endP` is reached, randomizing other parameters each time.
    3.  A value of `2` instructs the generator to run only a fixed set of values defined by `startP` and `endP`. The generator will select a RWS MAE task with super period `P = startP` with all other parameters randomized. _Unlike `fixedVars = 1`, while repeatedly increasing the value of `P` by `deltaP`, the other parameters (besides `R`) are __not changed__. This allows the user to identify how P changes other task properties while remaining parameters remain constant. 
10. `startP` specifies the initial super period when `fixedVars != 1`
11. `endP` specifies the ending super period when `fixedVars != 1`
12. `deltaP` specifies the change in super period when `fixedVars != 1`
13. `maximumValueAtReset` specifies the maximum value `f(t)` may be when a reset occurs.
    1.  A value of `-1` instructs the generator to deem any task where `f(t)` does not reach 50% of the value of `B[1]` to be infeasible.
    2.  This kind of requirement is useful when a user wishes to guarantee that `f(t)` reaches the highest WCET before resetting - such as a control system whose error must be driven to zero before another setpoint is provided.

To change any experiment, simply edit the values of the parameters.

_A WORD OF CAUTION: Completion time for simulating 10,000 tasks with an upper bound of `P=1000` can take at **15 hours** on single core at 3.5 GHz._
_<<<<<<<<<>>>>>>>: We explicitly classify P > 1000 as "infeasible" in the code to prevent excessive runtimes._