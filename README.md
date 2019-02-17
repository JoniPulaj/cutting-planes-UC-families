# cutting-planes-UC-families
A cutting plane method for Poonen's Theorem implemented in python that makes use of commercial integer programming software (CPLEX) and open source integer programming software (SCIP). Output can be checked separately with exact rational programming software http://scip.zib.de/#exact and VIPR https://github.com/ambros-gleixner/VIPR. 
User will need Cplex (available for free for academics), Scip (available for free) and finally igraph (available for free) for finding isomorphic families of sets. 
Part of the code in this project supports computations in the following paper: [Cutting Planes for Families implying Frankl's Conjecture](https://arxiv.org/abs/1702.05947). 

To check if a specific family of sets A on a ground set of, for example, ten elements is FC or Non-FC: 
```
import scipfamily10general as s
A = [[0,1,1,1,0,1,0,0,0,0],[1,0,0,1,1,0,0,0,0,0],[0,0,1,1,0,1,0,0,1,1],[0,0,0,1,0,1,1,1,0,0]]
s.scipfamily10general([A])
```
If A is in FC-family the proof is the infeasibility of the integer program contained in the file ```checkIP.lp```, else if A is a Non-FC-family, the proof is the infeasibility of the integer/linear program contained in ```check.lp```.


For families of smaller ground sets the corresponding modules have to imported. In future versions of the code, the size of the ground set will not be hard-coded. The code in general contains many auxilliary functions that help with printing and formatting text in latex and generating nonisomorphic families of sets, which are not of direct interest to the paper quoted above. In this regard module ``` scipfamily10general.py``` contains only the necessary functions (facilitating the reading of the code) needed for the computations in the aforementioned paper, which are identical to the necessary functions in the rest of the modules, except for the size of the ground set.
