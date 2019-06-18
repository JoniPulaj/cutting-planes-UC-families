\ SCIP STATISTICS
\   Problem name     : model
\   Variables        : 7 (0 binary, 7 integer, 0 implicit integer, 0 continuous)
\   Constraints      : 8
\   Obj. scale       : 1
\   Obj. offset      : 0
Minimize
 Obj: +1 Weight_0 +1 Weight_1 +1 Weight_2 +1 Weight_3 +1 Weight_4 +1 Weight_5 +1 Weight_6
Subject to
 sum_one: +1 Weight_1 +1 Weight_4 +1 Weight_6 +1 Weight_2 +1 Weight_0 +1 Weight_3 +1 Weight_5 >= +1
 nogoodcut: +16 Weight_1 +16 Weight_0 -48 Weight_3 >= +0
 nogoodcut: +16 Weight_1 -48 Weight_2 +16 Weight_0 >= +0
 nogoodcut: -40 Weight_1 +8 Weight_2 +24 Weight_0 +8 Weight_3 >= +0
 nogoodcut: +24 Weight_1 +8 Weight_2 -40 Weight_0 +8 Weight_3 >= +0
 nogoodcut: +16 Weight_4 +16 Weight_6 -48 Weight_5 >= +0
 nogoodcut: -48 Weight_4 +16 Weight_6 +16 Weight_5 >= +0
 nogoodcut: +16 Weight_4 -48 Weight_6 +16 Weight_5 >= +0
Bounds
Generals
 Weight_0 Weight_1 Weight_2 Weight_3 Weight_4 Weight_5 Weight_6
End
