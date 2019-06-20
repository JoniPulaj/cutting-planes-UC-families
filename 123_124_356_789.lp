\ SCIP STATISTICS
\   Problem name     : model
\   Variables        : 9 (0 binary, 9 integer, 0 implicit integer, 0 continuous)
\   Constraints      : 10
\   Obj. scale       : 1
\   Obj. offset      : 0
Minimize
 Obj: +1 Weight_0 +1 Weight_1 +1 Weight_2 +1 Weight_3 +1 Weight_4 +1 Weight_5 +1 Weight_6 +1 Weight_7
      +1 Weight_8
Subject to
 sum_one: +1 Weight_1 +1 Weight_5 +1 Weight_3 +1 Weight_7 +1 Weight_0 +1 Weight_2 +1 Weight_4 +1 Weight_6
  +1 Weight_8 >= +1
 nogoodcut: +64 Weight_1 -192 Weight_3 +64 Weight_0 >= +0
 nogoodcut: -192 Weight_5 +64 Weight_2 +64 Weight_4 >= +0
 nogoodcut: +48 Weight_1 +48 Weight_5 +48 Weight_0 -144 Weight_2 +48 Weight_4 >= +0
 nogoodcut: +64 Weight_5 +64 Weight_2 -192 Weight_4 >= +0
 nogoodcut: -160 Weight_1 +32 Weight_3 +96 Weight_0 +32 Weight_2 >= +0
 nogoodcut: +96 Weight_1 +32 Weight_3 -160 Weight_0 +32 Weight_2 >= +0
 nogoodcut: -192 Weight_7 +64 Weight_6 +64 Weight_8 >= +0
 nogoodcut: +64 Weight_7 -192 Weight_6 +64 Weight_8 >= +0
 nogoodcut: +64 Weight_7 +64 Weight_6 -192 Weight_8 >= +0
Bounds
Generals
 Weight_0 Weight_1 Weight_2 Weight_3 Weight_4 Weight_5 Weight_6 Weight_7 Weight_8
End
