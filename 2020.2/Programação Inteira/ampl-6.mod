param n integer;

set V := 1..n;

param w {V};
param p {V};

set E within {V,V};

param M := 10 * n;

var x {V} integer;
var y {V,V} binary;  # y[i,j] = 1 => task i comes before task j
                     # probably can be optimized to a triangular matrix
var s {V};

maximize Cost: sum {i in V} (w[i] * s[i]);

subject to Posteriority {i in V, j in V: i != j}:
    x[i] - x[j] >= 1 - M * y[i,j];

subject to Anteriority {i in V, j in V: i != j}:
    x[i] - x[j] <= -1 + M * (1 - y[i,j]);

subject to Precedence {(i,j) in E}:
    y[i,j] = 1;

subject to Start_time {j in V}:
    s[j] = sum {i in V} (p[i] * y[i,j]);

subject to Upper_bound {i in V}:
    x[i] <= n;

subject to Lower_bound {i in V}:
    x[i] >= 1;
