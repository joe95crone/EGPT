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

    def uniform_error(self):
        if self.std == 0:
            return self.mean
        else:
            sample = npr.uniform(self.mean - (self.trunc*self.std), self.mean + (self.trunc*self.std))
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

# test space!
if __name__ == "__main__":

    # class initialization 
    GPTrunner = GPT_input_runner('200fC.in', 'GPTin_tolerance.yml')

    tol_vals =  GPTrunner.input_reader()
    
    tol_vals_keys = list(tol_vals.keys())
    print(tol_vals_keys)
    map1D_TM_1_keys = list(getattr(tol_vals, tol_vals_keys[0]))
    print(map1D_TM_1_keys)
    map1D_TM_1_dx1_items = getattr(tol_vals.map1D_TM_1, map1D_TM_1_keys[0])
    print(map1D_TM_1_dx1_items)

    gen1 = generators(map1D_TM_1_dx1_items[0], map1D_TM_1_dx1_items[1], map1D_TM_1_dx1_items[3])
    print(gen1.gaussian_error())

    # loop over element keys, parameter keys and generate the errors then put them in the error_name=error_vale format string


