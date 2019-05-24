Smart grid
==========
For this case we start with a neighbourhood containing a set of houses and
batteries with a set capacity. The houses produce power, which has to be stored
in the batteries. Cables to the batteries cost money, so the goal is to connect
all houses with a battery for the least amount of money
=============
Team Duracell
=============
Niek Slemmmer 12639184
Tim de Boer 11202351
Joost Bankras 12377775

## algorithms
* Connect random: an algorithm that connects each house to whatever battery
still has capacity
* Connect greedy: sorts all houses based on distance to each battery, and
connect whichever is closest, as long as it has capacity
* Constraint relaxation: connects all houses to their closest battery,
disregarding capacity entirely, than keeps switching houses until constraints
are satisfied
* Hillclimb: tries to find the local optimum, by switching batteries around
if it leads to lower costs
* A-star: in the advanced part of the assignment it costs money to lay cable
under houses. By using a-star for the pathfinding the algorithm is able to avoid
doing this by going around if necessary

## Requirements
Install matplotlib, numpy and scikit_learn, as per requirements.txt

## Usage
```
  Usage:
    python app.py [map] [algorithm] [hillclimb] [runs] [pathfinding]

  map:
    There are 3 maps available, choose "1", "2" or "3"
  algorithm:
    "1" : connect houses with a random algorithm
    "2" : connect houses using a greedy algorithm
    "3" : connect houses using constraint relaxation
  hillclimb:
    "0" : Don't use hillclimb
    "1" : Use hillclimb on top of the solution from the other algorithm
  runs:
    Specify the number of runs to do. We advise keeping this number under x
  pathfinding:
    "0" : standard pathfinding, straight up and horizontally
    "1" : A* pathfinding, avoids houses if necessary (almost always)
```
