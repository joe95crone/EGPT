# runs error analysis code for GPT

# DEPENDENCIES
# GPT
# numpy
# re
# itertools
# os
# munch
# pyyaml

import numpy as np

# GUI/user input 
import sys
import os
import time 

# GPT error files (missing analysis package)
import GPTin_error_modifier as GPTinmod # import the GPT lattice file (.in file) modifier
import GPT_input_runner as GPTrun

if __name__ == "__main__":

    # read the initial GPT file
    init_GPT_file = sys.argv[1]
    GPT_lat_err = GPTinmod.GPT_error_mod(init_GPT_file)

    # try and except on sys.argv[2] (YAML tolerance file) to see if this is a template generation run or an error run
    # if successful it is an error run 
    # need some kind of catch to determine if the error file has been generated 
    
    if len(sys.argv) < 3:
        # generate YAML template and errored lattice
        print("Template Generation Run")
        time.sleep(1)
        GPT_lat_err.lattice_replacer_template()
    elif len(sys.argv) == 3:
        print("Error Run")
        time.sleep(1)
        if os.path.exists(sys.argv[2]) == True:
            GPTrunner = GPTrun.GPT_input_runner(sys.argv[1], sys.argv[2])
            GPTrunner.GPT_run()
        else:
            print("Failed: YAML tolerance file not found.")