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

if __name__ == "__main__":

    # read the initial GPT file
    init_GPT_file = sys.argv[1]
    GPT_lat_err = GPTinmod.GPT_error_mod(init_GPT_file)

    # try and except on sys.argv[2] (YAML tolerance file) to see if this is a template generation run or an error run
    # if successful it is an error run 
    # need some kind of catch to determine if the error file has been generated 
    
    print(sys.argv[2])

    if len(sys.argv) < 2:
        # generate YAML template and errored lattice
        print("Template Generation Run")
        time.sleep(1)
        GPT_lat_err.lattice_replacer_template()
    elif len(sys.argv) == 2:
        print("Error Run")
        time.sleep(1)
        if os.path.exists(sys.argv[2]) == True:
            print(sys.argv[2])
        else:
            print("Failed: YAML tolerance file not found.")