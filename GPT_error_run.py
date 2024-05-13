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
import GPTin_error_modifier as GPTinmod # import the GPT lattice file (.in file) modifier

if __name__ == "__main__":

    # read the initial GPT file
    init_GPT_file = sys.argv[1]
    GPT_lat_err = GPTinmod.GPT_error_mod(init_GPT_file)

    # try and except on sys.argv[2] (YAML tolerance file) to see if this is a template generation run or an error run 
    try:
        # users pass tolerances - YAML file, modified from template
        print(sys.argv[2])
    except IndexError:
        # generate YAML template and errored lattice
        GPT_lat_err.lattice_replacer_template() 
    
    # settings for error analysis
    #trunc = 3 # truncate all error distributions to 3 standard deviations 

    # generate error value (example of an additive error)
    #dx1 =  gen.gaussian_error(0, toldx1, trunc)
    #print(dx1)

   


