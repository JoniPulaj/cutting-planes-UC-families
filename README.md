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


The files ```Proposition7.lp```, ```Proposition8_x0_zero.lp```, ```Proposition8_x0_one.lp```, ```Proposition11.lp``` and ```Proposition12.lp``` contain the linear and integer programs used in the proofs of Propositions 7, 8, 11 and 12, respectively. The integer program in Proposition 8 is reduced to two linear programs as elaborated in the appendix of the paper mentioned above by branching on the variable ```x0```. 

An interested reader can independently verify these results by submitting the files to the [NEOS Server](https://neos-server.org/neos/) a free and easy to use internet-based service for numerical optimization problems. In particular, ```Proposition7.lp```, ```Proposition8_x0_zero.lp```, ```Proposition8_x0_one.lp``` and ```Proposition12.lp``` can be directly submitted to
[CPLEX](https://neos-server.org/neos/solvers/lp:CPLEX/LP.html), [Gurobi](https://neos-server.org/neos/solvers/lp:Gurobi/LP.html) and [MOSEK](https://neos-server.org/neos/solvers/lp:MOSEK/LP.html) in their respective short priority queues as LP files. Furthermore the exact solvers [SoPlex80bit](https://neos-server.org/neos/solvers/lp:SoPlex80bit/LP.html) and [QSopt_EX](https://neos-server.org/neos/solvers/milp:qsopt_ex/LP.html) (rational/integer input data format) can be used to safeguard against possible floating-point issues. ```Proposition11.lp``` is a feasible integer program that can be checked directly in [SCIP](https://neos-server.org/neos/solvers/milp:scip/CPLEX.html).  
