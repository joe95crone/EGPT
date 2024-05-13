# code for reading in YAML template, getting error values and running GPT

import numpy.random as npr
import munch
import yaml

# generator for errors
# rejection sampling to impose cut-off
class generators:
    def __init__(self, mean, std, trunc):
        self.mean = mean
        self.std = std
        self.trunc = trunc

    # Gaussian error generation
    def gaussian_error(self):
        if self.std == 0:
            return self.mean
        else:
            lims = [self.mean - (self.trunc*self.std), self.mean + (self.trunc*self.std)]
            sample = npr.normal(self.mean, self.std)
            while lims[0] >= sample >= lims[1]:
                sample = npr.normal(self.mean, self.std) 
            return sample

# take in tolerances
# get the values (using the generators)
# put them into the string format required for GPT run macro
# run GPT  

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

    # function for running GPT
    #! careful of the GPT path and GPT license - how to set these properly??
    def GPT_run(self):
        GPTinfile = self.GPTin.split('.')[0] + '_ERR' + '.' + self.GPTin.split('.')[-1]
        # function to get the tol vals from the tolerance structure

        # code to write tolerance values correctly dx1=val etc.
        GPT_cmd = '"C:/Program Files/General Particle Tracer/bin/gpt.exe" -j 4 -o {0} {1} {2} GPTLICENSE=1384567269'
        #os.system(GPT_cmd.format(GPT, infile, err_vals))
