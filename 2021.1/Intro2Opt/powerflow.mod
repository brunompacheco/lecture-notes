set N;
set N_ {N} within N;

param n {N,N};

param theta_k {0..8};
param P_k {N,N,0..8};

param P_g_max {N};
param P_d {N};


var theta {N} >= -1.5707963268, <= 1.5707963268;
var P_g {N} >= 0;
var P {N};
var P_plus {N} >= 0;
var P_minus {N} >= 0;
var P_ {N,N};

var lambda {N,N,0..8} >= 0;
var z {N,N,1..8} binary;

minimize Power: sum{i in N} (P_plus[i] + P_minus[i]);

subject to Gen_Power {i in N}:
    P_g[i] = P_d[i] + P[i];

subject to Power_in {i in N}:
    P[i] = sum{j in N_[i]} (n[i,j] * P_[i,j]);

subject to Gen_Power_lim {i in N}:
    P_g[i] <= P_g_max[i];

subject to PL_theta {i in N, j in N_[i]}:
    theta[i] - theta[j] = sum{k in 0..8} (lambda[i,j,k] * theta_k[k]);

subject to PL_Power_ij {i in N, j in N_[i]}:
    P_[i,j] = sum{k in 0..8} (lambda[i,j,k] * P_k[i,j,k]);

subject to One_Hot_lambda {i in N, j in N_[i]}:
    sum{k in 0..8} lambda[i,j,k] = 1;

subject to One_Hot_z {i in N, j in N_[i]}:
    sum{k in 1..8} z[i,j,k] = 1;

subject to lambda_Consecutiveness {i in N, j in N_[i], k in 1..7}:
    lambda[i,j,k] <= z[i,j,k] + z[i,j,k+1];

subject to lambda_first {i in N, j in N_[i]}:
    lambda[i,j,0] <= z[i,j,1];

subject to lambda_last {i in N, j in N_[i]}:
    lambda[i,j,8] <= z[i,j,8];

subject to Power_absolute {i in N}:
    P_plus[i] - P_minus[i] = P[i];