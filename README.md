# AIMA 2020 Assignment 2 - Hunt the Wumpus

This repository contains the group work submitted for the Assignment 2 of the [AIMA 2020](https://ole.unibz.it/course/view.php?id=6841) course from the Free University of Bozen-Bolzano.

## Problem description

The problem introduced by the assignment is to find the **best sequence of actions** (if one is available) to make the *agent* (a hunter) grabbing the gold in the given environment and eventually climbing out of the world.

In this case the world is modeled as a *grid map* with some pits, where the agent would die if entering them. 
The agent also has an orientation (either North, East, South or West) and can only move following the direction he is heading to.
To make the agent change direction there is a Left and Right action to make the agent rotate.
The agent also has one arrow he can use to kill the wumpus, if necessary, in order to shoot the monster and move inside its location without dying.

An example of the **game** is shown below:

<img src="/images/hunt_wumpus.gif"  width="300">

## Technical description

For a complete description of the solution we developed, you can have a look at the documentation available [here](https://github.com/giannpelle/AI-lab2-HuntWumpus/tree/master/documentation/documentation.pdf).

## Solution outputs

If you want to see the results (outputs) we got from running the different kind of search techniques and heuristics below there is the full list of outputs:

* Uniform cost search:
  * [UCS search - world1](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/UCS-world1-output.ipynb)
  * [UCS search - world2](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/UCS-world2-output.ipynb)
  * [UCS search - world3](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/UCS-world3-output.ipynb)
  * [UCS search - world4](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/UCS-world4-output.ipynb)
  * [UCS search - world5](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/UCS-world5-output.ipynb)
  * [UCS search - world6](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/UCS-world6-output.ipynb)
  * [UCS search - world7](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/UCS-world7-output.ipynb)
  * [UCS search - world8](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/UCS-world8-output.ipynb)

* A* search (best-neighbour heuristic):
  * [A* search - world1](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/AStar-best-neighbour-world1-output.ipynb)
  * [A* search - world2](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/AStar-best-neighbour-world2-output.ipynb)
  * [A* search - world3](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/AStar-best-neighbour-world3-output.ipynb)
  * [A* search - world4](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/AStar-best-neighbour-world4-output.ipynb)
  * [A* search - world5](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/AStar-best-neighbour-world5-output.ipynb)
  * [A* search - world6](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/AStar-best-neighbour-world6-output.ipynb)
  * [A* search - world7](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/AStar-best-neighbour-world7-output.ipynb)
  * [A* search - world8](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/AStar-best-neighbour-world8-output.ipynb)

* A* search (smart-manhattan heuristic):
  * [A* search - world1](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/AStar-smart-manhattan-world1-output.ipynb)
  * [A* search - world2](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/AStar-smart-manhattan-world2-output.ipynb)
  * [A* search - world3](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/AStar-smart-manhattan-world3-output.ipynb)
  * [A* search - world4](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/AStar-smart-manhattan-world4-output.ipynb)
  * [A* search - world5](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/AStar-smart-manhattan-world5-output.ipynb)
  * [A* search - world6](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/AStar-smart-manhattan-world6-output.ipynb)
  * [A* search - world7](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/AStar-smart-manhattan-world7-output.ipynb)
  * [A* search - world8](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/AStar-smart-manhattan-world8-output.ipynb)

* A* search (best-neighbour-smart-manhattan heuristic):
  * [A* search - world1](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/AStar-best-neighbour-smart-manhattan-world1-output.ipynb)
  * [A* search - world2](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/AStar-best-neighbour-smart-manhattan-world2-output.ipynb)
  * [A* search - world3](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/AStar-best-neighbour-smart-manhattan-world3-output.ipynb)
  * [A* search - world4](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/AStar-best-neighbour-smart-manhattan-world4-output.ipynb)
  * [A* search - world5](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/AStar-best-neighbour-smart-manhattan-world5-output.ipynb)
  * [A* search - world6](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/AStar-best-neighbour-smart-manhattan-world6-output.ipynb)
  * [A* search - world7](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/AStar-best-neighbour-smart-manhattan-world7-output.ipynb)
  * [A* search - world8](https://github.com/giannpelle/AI-lab2-HuntWumpus/blob/master/sample-outputs/AStar-best-neighbour-smart-manhattan-world8-output.ipynb)

## Running requirements

To run the code you have to create an *anaconda* environment with the configuration file found in *environment.yml* and then activate it to run the code.  
The required commands to make it work are the following:
1. `conda create env -f environment.yml`
2. `conda activate wumpus`
3. `jupyter lab`

To run the sample code you just need to run the code cells in the files *hunt_wumpus_UCS_sample.ipynb* and *hunt_wumpus_AStar_sample.ipynb*.
