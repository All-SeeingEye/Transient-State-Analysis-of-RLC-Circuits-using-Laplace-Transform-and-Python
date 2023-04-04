# Transient State Analysis of RLC Circuits using Laplace Transform and Python

## Introduction

I have made this code  from the jupyter notebook of week2 assigment (documetaion is provided for it in pdf), the code in the jupyter notebook was an attempt on solving steady state circuit analysis, this repository is for transient state analysis of the novice electric circuit containg rlc elements.

## Usage:
run the python-script `python3 circuit_solve.py <netlist> .tran` for transient analysis.
The user will then be given list of nodes voltages and branch currents to plot the wave form of and user should input the node or branch name from to list to see the plot.

Test cases are given in form of .txt format but can also be used if .netlist format is used

run the python-script `python3 circuit_solve.py <netlist> .draw` for circuit diagram.

## Scripts info
There are 3 python files used for making this this program, the `parsing_circuit.py` file is used as library to parse the netlist given as input, this library contais functions to clear the netlist of unwanted comments and also functions to load the data form netlist for equation analysis and drwaing the circuit.

Second file `circuit_solve.py` is the main working file where the python script on the input given either solves the transient analysis or calls the draw.py script to draw the circuit.
I am using Laplace Transform to perform the transient analysis on the circuit. To to do I am using Symbolic Python, to handle the equations and inverse lapace transform function in the library, and also matplotlib to plot the graphs of the transient analysis. Certain other open source libraies such as sys and subproces are used in order to make a user friendly progem to some extent

Third python `script draw.py` uses `networkx` library to draw the nodes and branches and names them according to the data of the netlist, also used the `matplotlib` library to show the plot and the circuit diagram.

## Long term plan
There are serval scopes of improvement here, 
* Firstly being fix the bug for cases where inverse laplace transform do not exsist then use some intellegnt methods or approximations.
* Improve the draw.py file to incude the values of the componets used, add feature of adding the time scale the user want to perform transient analysis for.
* Upgrade the code from novice circuit analysis to advance circuit analysis of controlled sources, opamps etc...
* Add fuctionality of doing steaty state or transient analysis on user given input
* Add an interface to change the components values rather then loading a new netlist
* Include necessary package installation function for ready to use.

## Conclusion
The program is free of use and can be used by installing the neccesary libraies, sympy,numpy,matplotlib,re,netwrokx. The project is open source,feel free to contribute to the project or give suggestions. You can write me email to this mail id 99jainam@gmail.com for conatct

Currently the program is still in its devloping state and cannot be used for professional  usage, and to make it used in professional pratice I need your help to conribute in this project, I am open to all sugesstions and recomedation for this project and hope that it is helpful to you.

The project is under MIT License.



