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
import GPT_run_analyse as GPTrun
import GPT_plotting as GPTplt

if __name__ == "__main__":

    # read the initial GPT file
    init_GPT_file = sys.argv[1]
    GPT_lat_err = GPTinmod.GPT_error_mod(init_GPT_file)

    # run as python GPT_error_run.py <GPT_infile>.in for template generation
    # run as python GPT_error_run.py <GPT_infile>.in <tolerance_file>.yml (<trials>) for error run - no trials argument results in a single error run
 
    if len(sys.argv) < 3:
        # generate YAML template and errored lattice
        print("Template Generation Run")
        time.sleep(1)
        GPT_lat_err.lattice_replacer_template()
    elif len(sys.argv) >= 3:
        print("Error Run")
        time.sleep(1)
        if os.path.exists(sys.argv[2]) == True:
            # run the GPT file using the yaml tolerance file - use sys.argv[3] for the no. trials
            try:
                GPT_run = GPTrun.GPT_run_analyse(sys.argv[1], sys.argv[2], sys.argv[3])
                run_data = GPT_run.GPT_run_get_analysis()
                print(run_data.keys())
            except IndexError: 
                GPT_run = GPTrun.GPT_run_analyse(sys.argv[1], sys.argv[2])
                # running and analysing the results of the single error run
                run_data = GPT_run.GPT_run_get_analysis()
                #GPT_plots = GPTplt.GPT_plotting(GPTtime, GPTpos, GPTtouts, GPTscreens)
                #GPT_plots.beam_size()
        else:
            print("Failed: YAML tolerance file not found.")
    else:
        print("Incorrect no. arguments")
    