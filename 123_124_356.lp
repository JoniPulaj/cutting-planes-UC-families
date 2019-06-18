\ SCIP STATISTICS
\   Problem name     : model
\   Variables        : 6 (0 binary, 6 integer, 0 implicit integer, 0 continuous)
\   Constraints      : 7
\   Obj. scale       : 1
\   Obj. offset      : 0
Minimize
 Obj: +1 Weight_0 +1 Weight_1 +1 Weight_2 +1 Weight_3 +1 Weight_4 +1 Weight_5
Subject to
 sum_one: +1 Weight_1 +1 Weight_5 +1 Weight_4 +1 Weight_0 +1 Weight_3 +1 Weight_2 >= +1
 nogoodcut: -20 Weight_1 +12 Weight_0 +4 Weight_3 +4 Weight_2 >= +0
 nogoodcut: +12 Weight_1 -20 Weight_0 +4 Weight_3 +4 Weight_2 >= +0
 nogoodcut: +8 Weight_1 +8 Weight_0 -24 Weight_3 >= +0
 nogoodcut: +8 Weight_5 -24 Weight_4 +8 Weight_2 >= +0
 nogoodcut: +6 Weight_1 +6 Weight_5 +6 Weight_4 +6 Weight_0 -18 Weight_2 >= +0
 nogoodcut: -24 Weight_5 +8 Weight_4 +8 Weight_2 >= +0
Bounds
Generals
 Weight_0 Weight_1 Weight_2 Weight_3 Weight_4 Weight_5
End
