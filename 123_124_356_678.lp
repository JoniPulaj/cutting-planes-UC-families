\ SCIP STATISTICS
\   Problem name     : model
\   Variables        : 8 (0 binary, 8 integer, 0 implicit integer, 0 continuous)
\   Constraints      : 9
\   Obj. scale       : 1
\   Obj. offset      : 0
Minimize
 Obj: +1 Weight_0 +1 Weight_1 +1 Weight_2 +1 Weight_3 +1 Weight_4 +1 Weight_5 +1 Weight_6 +1 Weight_7
Subject to
 sum_one: +1 Weight_1 +1 Weight_6 +1 Weight_0 +1 Weight_3 +1 Weight_5 +1 Weight_4 +1 Weight_7 +1 Weight_2
  >= +1
 nogoodcut: +32 Weight_5 -96 Weight_4 +32 Weight_2 >= +0
 nogoodcut: +32 Weight_1 +32 Weight_0 -96 Weight_3 >= +0
 nogoodcut: +24 Weight_1 +24 Weight_0 +24 Weight_5 +24 Weight_4 -72 Weight_2 >= +0
 nogoodcut: -80 Weight_1 +48 Weight_0 +16 Weight_3 +16 Weight_2 >= +0
 nogoodcut: +48 Weight_1 -80 Weight_0 +16 Weight_3 +16 Weight_2 >= +0
 nogoodcut: -96 Weight_6 +32 Weight_5 +32 Weight_7 >= +0
 nogoodcut: +24 Weight_6 -72 Weight_5 +24 Weight_4 +24 Weight_7 +24 Weight_2 >= +0
 nogoodcut: +32 Weight_6 +32 Weight_5 -96 Weight_7 >= +0
Bounds
Generals
 Weight_0 Weight_1 Weight_2 Weight_3 Weight_4 Weight_5 Weight_6 Weight_7
End
