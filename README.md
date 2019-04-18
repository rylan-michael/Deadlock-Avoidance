# Exploring Operating System Deadlocks

## Objectives & Overview

Get familiarized with the basic concepts of deadlocks, the Banker's algorithm
for deadlock avoidance and recovery from deadlocks. Simulate deadlock avoidance
and deadlock recovery. [1] Operating Systems Concepts 9th Edition by Silberscharz, Yale, and Gagne, Wiley

## How to Run

This program was written with Python 3.7 in path. For help run

    \bankers-alogorithm>python main.py -h

otherwise specify the file as you run the command.

    \bankers-algorithm>python main.py sys_config.txt

The program should read the system configuration information from a data file (i.e., sys_config.txt). More specifically, this data file contains the **Available** vector, **Max** matrix, **Allocation** matrix. (See the included test files for the format.) NOTE: this program can take a variable number of process and resource types, as long as they are consisten within the file.

    \bankers-algorithm>python main.py sys_config.txt
    SAFE

The program takes a **Request** vector as user input and prints out either **GRANTED** or **NOT GRANTED** to indicate whether the resource request can be granted or not. Assume that the requesting process is *Process 0*. For example,

    \bankers-algorithm>python main.py sys_config.txt
    SAFE
    If you'd like to exit reading input, enter 'c'.
    Please enter a request vector: 1 0 2
    NOT GRANTED
    Please enter a request vector: 1 0 1
    GRANTED

The program also implements a simple deadlock recovery mechanism. If request resources cannot be granted, then it identifies the minimum number of processes that should be forced to terminate such that the request can be granted.