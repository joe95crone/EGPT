# runs error analysis code for GPT

# DEPENDENCIES
# GPT
# numpy
# re
# itertools

import numpy as np

# GUI/user input 
import sys
import os

# GPT error files (missing analysis package)
import generators as gen # import the error generators
import GPTin_error_modifier as GPTinmod # import the GPT lattice file (.in file) modifier

# function for running GPT
#! careful of the GPT path and GPT license
def GPT_run(outfile, infile, tol_vals):
    # code to write tolerance values correctly dx1=val etc.
    GPT_cmd = '"C:/Program Files/General Particle Tracer/bin/gpt.exe" -j 4 -o {0} {1} {2} GPTLICENSE=1384567269'
    os.system(GPT_cmd.format(outfile, infile, tol_struct))


if __name__ == "__main__":

    # create errored lattice + get error identifiers
    GPT_lat_err = GPTinmod.GPT_error_mod('200fC.in')
    err_idents = GPT_lat_err.lattice_replacer() 
    print(err_idents)
    
    # settings for error analysis
    trunc = 3 # truncate all error distributions to 3 standard deviations 

    # users pass tolerances - could be passed in some kind of GUI form
    toldx1 = float(sys.argv[1])
    tolf1 = float(sys.argv[2])

    # generate error value (example of an additive error)
    dx1 =  gen.gaussian_error(0, toldx1, trunc)
    print(dx1)

    # generate error value (example of a fractional error)
    f1 = gen.gaussian_error(1, tolf1, trunc)
    print(f1)

    test0 = gen.gaussian_error(0,0,trunc)
    print(test0)

    # next task here is to write a GUI which creates a Table of errors and their tolerances for input
    # |element_name + instance| tolerance1_name | tolerance2_name | ...
    # | identifier | dx    |  dy    |  dz  | f1Bfac | dBfac |
    # | map1D_B#1 | 100 um | 60 um | 60 um|        |        |



