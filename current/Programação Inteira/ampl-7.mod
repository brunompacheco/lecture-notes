param n integer;

param s integer;
param t integer;

set V := 1..n;

set E within {i in V, j in V};

set TS_arc := {(t,s)};
set E_ := E union TS_arc;

var x {E union E_} integer;

maximize Paths: x[t,s];

subject to Flow {i in V}:
    sum {k in V: (i,k) in E_} (x[i,k]) - sum {k in V: (k,i) in E_} (x[k,i]) = 0;

subject to Lower_bound {(i,j) in E_}:
    x[i,j] >= 0;

subject to Upper_bound {(i,j) in E}:
    x[i,j] <= 1;