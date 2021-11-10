set C;
set T;
set R;
set L;
set P;

set L_c {C} within L;
set R_p {P} within R;
set P_l {L} within P;
set P_rt {R,T} within P;

set P_c {C} within P;
set R_c {C} within R;

# these (below and above) pairs of lines must be commented/uncommented when
# submitting the job to NEOS server as the AMPLPy API already writes the R_c
# and P_c sets when exporting the data file

# set P_c {c in C} = union {l in L_c[c]} P_l[l];
# set R_c {c in C} = union {p in P_c[c]} R_p[p];


# param w {P,R};
param w {P};

var x {P,R} <= 1;

# maximize AssignmentQuality: sum {p in P, r in R} (w[p,r] * x[p,r]);
maximize AssignmentQuality: sum {p in P, r in R} (w[p] * x[p,r]);

subject to RoomOverbooking {r in R, t in T}:
    sum {p in P_rt[r,t]} (x[p,r]) <= 1;

subject to LectureOverbooking {l in L}:
    sum {p in P_l[l]} (sum {r in R_p[p]} (x[p,r])) <= 1;

subject to PatternUnity {c in C, r in R_c[c]}:
    sum{p in P_c[c]} (x[p,r]) <= 1;

subject to InfeasibleRooms {p in P}:
    sum {r in R diff R_p[p]} x[p,r] = 0;
subject to LowerBound {p in P, r in R}:
    x[p,r] >= 0;
