# data params
param N integer;

param lb_inj {1..N} >= 0;
param ub_inj {1..N} >= 0;

param WCut {1..N} >= 0;
param WCut_ {n in 1..N} = (WCut[n] / (1 - WCut[n]));
param GOR {1..N} >= 0;

param Qinj_max >= 0;
param Qliq_max >= 0;
param Qgas_max >= 0;

param K {1..N} > 0 integer;

param Qinj_data {n in 1..N,1..K[n]} >= 0;
param Qoil_data {n in 1..N,1..K[n]} >= 0;

# CC vars
var lambda {n in 1..N,1..K[n]} >= 0;
var z {n in 1..N,2..K[n]} binary;
var Qoil_CC {1..N} >= 0;

# problem vars
var Qinj {1..N} >= 0;
var Qoil {1..N} >= 0;
var Qwat {1..N} >= 0;
var Qgas {1..N} >= 0;

var y {1..N} binary;

maximize OilProduction:
    sum{n in 1..N} Qoil[n]
;

subject to InjectionLimit:
    sum{n in 1..N} Qinj[n] <= Qinj_max
;
subject to LiquidLimit:
    sum{n in 1..N} (Qoil[n] + Qwat[n]) <= Qliq_max
;
subject to GasLimit:
    sum{n in 1..N} (Qinj[n] + Qgas[n]) <= Qgas_max
;
# Not necessary as CC already guarantees this (actually, this breaks the opt)
# subject to OilLimits {n in 1..N}:
#     Qoil[n] <= y[n] * Qoil_data[n,K[n]]
# ;

subject to InjectionUpperBound {n in 1..N}:
    Qinj[n] <= y[n] * ub_inj[n]
;
subject to InjectionLowerBound {n in 1..N}:
    Qinj[n] >= y[n] * lb_inj[n]
;

subject to GasPhase {n in 1..N}:
    Qgas[n] = GOR[n] * Qoil[n]
;
subject to WaterPhase {n in 1..N}:
    Qwat[n] = WCut_[n] * Qoil[n]
;

# as CC restricts Qoil to be on the range of the points, we need to remove this
# "offset" in case a well is not being used for production
subject to Well {n in 1..N}:
    Qoil[n] = Qoil_CC[n] - (1 - y[n]) * Qoil_data[n,1]
;

## CC constraints
subject to CC_X {n in 1..N}:
    sum{i in 1..K[n]} (lambda[n,i] * Qinj_data[n,i]) = Qinj[n]
;

subject to CC_Y {n in 1..N}:
    sum{i in 1..K[n]} (lambda[n,i] * Qoil_data[n,i]) = Qoil_CC[n]
;

subject to CC_lambda {n in 1..N}:
    sum{i in 1..K[n]} lambda[n,i] = 1
;

subject to CC_z {n in 1..N}:
    sum{i in 2..K[n]} z[n,i] = 1
;

subject to CC_lambda_z {n in 1..N, i in 2..K[n]-1}:
    lambda[n,i] <= z[n,i] + z[n,i+1]
;
subject to CC_lambda_z_start {n in 1..N}:
    lambda[n,1] <= z[n,2]
;
subject to CC_lambda_z_end {n in 1..N}:
    lambda[n,K[n]] <= z[n,K[n]]
;
