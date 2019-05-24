Smart grid
=======
Team Duracell
======
Niek Slemmmer 12639184
Tim de Boer 11202351
Joost Bankras 12377775

## Requirements
Install matplotlib, numpy and scikit_learn, as per requirements.txt

## Usage
```
  Usage:
    python app.py [map] [algorithm] [hillclimb] [runs]

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
```
