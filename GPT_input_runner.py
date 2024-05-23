# code for reading in YAML template, getting error values and running GPT

import numpy.random as npr
import munch
import yaml
from itertools import chain
import os

# generator for errors
# rejection sampling to impose cut-off
# Gaussian error generation
def gaussian_error(mean, std, trunc):
    if std == 0:
        return mean
    else:
        lims = [mean - (trunc*std), mean + (trunc*std)]
        sample = npr.normal(mean, std)
        while lims[0] >= sample >= lims[1]:
            sample = npr.normal(mean, std) 
        return sample

def uniform_error(mean, std, trunc):
    if std == 0:
        return mean
    else:
        sample = npr.uniform(mean - (trunc*std), mean + (trunc*std))
    return sample

class GPT_input_runner:
    def __init__(self, GPTin, inyaml):
        # yaml tolerance file
        self.inyaml = str(inyaml)
        # initial GPT in file
        self.GPTin = str(GPTin)

    # read in the yaml file
    def input_reader(self):
        with open(self.inyaml, 'r') as infile:
            tolerance = munch.munchify(yaml.safe_load(infile))
            return tolerance

    # function for getting the errors and creating the structure
    def error_val_structure(self):
        tol_vals = self.input_reader()
        tol_vals_keys = list(tol_vals.keys())
        tol_keys_keys = []
        err_vals = []
        # get out a list of magnets, magnet parameters and error values (from tolerances)
        for i in range(len(tol_vals_keys)):
            tol_keys_keys.append(list(getattr(tol_vals, tol_vals_keys[i])))
            for j in range(len(tol_keys_keys[i])):
                tol_param = eval("tol_vals"+"."+tol_vals_keys[i]+"."+tol_keys_keys[i][j])
                if tol_param[2] == 'gaussian':
                    err_vals.append(gaussian_error(tol_param[0], tol_param[1], tol_param[3]))
                elif tol_param[2] == 'uniform':
                    err_vals.append(uniform_error(tol_param[0], tol_param[1], tol_param[3]))
        # flatten tol_keys_list
        tol_keys_keys = list(chain.from_iterable(tol_keys_keys))
        # two arrays which I pattern as they'd appear in a GPT command then return 
        return ','.join(["{0}={1}".format(tol_keys_keys_, err_vals_) for tol_keys_keys_, err_vals_ in zip(tol_keys_keys, err_vals)])
        
    # function for running GPT
    #! careful of the GPT path and GPT license - how to set these properly??
    def GPT_run(self):
        # filenames
        GPToutfile = 'temp.gdf'
        GPTinfile = self.GPTin.split('.')[0] + '_ERR' + '.' + self.GPTin.split('.')[-1]
        # function to get the error values in the correct pattern
        err_struct = self.error_val_structure()
        # run GPT command
        GPT_cmd = '"C:/Program Files/General Particle Tracer/bin/gpt.exe" -j 4 -o {0} {1} {2} GPTLICENSE=1384567269'
        os.system(GPT_cmd.format(GPToutfile, GPTinfile, err_struct))

# test space!
#if __name__ == "__main__":

    # class initialization 
#    GPTrunner = GPT_input_runner('200fC.in', 'GPTin_tolerance.yml')
#    print(GPTrunner.error_val_structure())

    


