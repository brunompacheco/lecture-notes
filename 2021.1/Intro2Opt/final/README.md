# Production Optimization of Gas-Lifted Oil Wells

The files in this directory contain the implementation of the reformulation proposed for the final project of DAS410062 - Introduction to Optimization.

The reformulations of the problems are in both `glows-cc.mod` and `glows-sos2.mod` and it is recommended to use the respective `.run` files to run the solver (mainly for SOS2). Both of these run files store detailed results in a `result.out` file. The `result_*.out` contain the detailed results for different Qinj_max values.

`range-solve.run` uses the SOS2 reformulation to iterate over Qinj_max values and stores the corresponding objective value in `range_results.csv`, which was used to generate the graph on the report.

Lastly, `p1.dat` has a slight modification on the namings of Qinj and Qoil to Qinj_data and Qoil_data, that is why it is also included.