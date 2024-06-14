# code for reading in YAML template, getting error values and running GPT

import numpy.random as npr
import munch
import yaml
from itertools import chain
import subprocess
import easygdf

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

class GPT_run_analyse:
    # defaults to single trial error analysis
    def __init__(self, GPTin, inyaml, ntrial=1):
        # no trials
        self.ntrial = int(ntrial)

        # yaml tolerance file
        self.inyaml = str(inyaml)
        
        # initial GPT in file
        self.GPTin = str(GPTin)
        self.GPTinfile = 'D:\\GPT_err\\' + self.GPTin.split('.')[0] + '_ERR' + '.' + self.GPTin.split('.')[-1]

        self.path = 'D:\\GPT_err\\'
        self.GDFfile = 'temp.gdf'
        
        self.GPToutfile = self.path + self.GDFfile
        self.GPT_time_file = self.GPToutfile.split('.')[0] + "_time." + self.GPToutfile.split('.')[1]
        self.GPT_pos_file = self.GPToutfile.split('.')[0] + '_pos.' + self.GPToutfile.split('.')[1]

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
        return ["{0}={1}".format(tol_keys_keys_, err_vals_) for tol_keys_keys_, err_vals_ in zip(tol_keys_keys, err_vals)]
    
    # function for running GPT
    #! careful of the GPT path and GPT license - how to set these properly??
    def GPT_run(self, trial):
        # function to get the error values in the correct pattern
        err_struct = self.error_val_structure()
        # get the output file name
        trial_outfile = self.GPToutfile.split('.')[0] + "_" +  str(trial) + "." + self.GPToutfile.split('.')[1]
        # run GPT command
        GPT_cmd = [r'C:/Program Files/General Particle Tracer/bin/gpt.exe'] + ['-v'] + ['-o', trial_outfile] + [self.GPTinfile] + err_struct + ['GPTLICENSE=1384567269']
        subprocess.call(GPT_cmd)

        # run the analysis of the GDF output file (time & position)
    def run_GDF_analysis(self, trial):
        # paths
        time_trial_outfile = self.GPT_time_file.split('.')[0] + "_" + str(trial) + "." + self.GPT_time_file.split('.')[1]
        pos_trial_outfile = self.GPT_pos_file.split('.')[0] + "_" + str(trial) + "."  + self.GPT_pos_file.split('.')[1]
        trial_outfile = self.GPToutfile.split('.')[0] + "_" + str(trial) + "."  + self.GPToutfile.split('.')[1]

        # time-like analysis
        time_output = ['time', 'avgx', 'avgy', 'avgz', 'stdx', 'stdBx', 'stdy', 'stdBy', 'stdz', 'nemixrms', 'nemiyrms', 'nemizrms', 'numpar', 'nemirrms', 'avgG', 'avgp', 'stdG', 'avgBx', 'avgBy', 'avgBz', 'CSalphax', 'CSalphay', 'CSbetax', 'CSbetay', 'avgfBx', 'avgfEx', 'avgfBy', 'avgfEy', 'avgfBz', 'avgfEz']
        GPT_time_analysis_cmd = [r'C:/Program Files/General Particle Tracer/bin/gdfa.exe'] + ['-v'] + ['-o', time_trial_outfile] + [trial_outfile] + time_output
        subprocess.call(GPT_time_analysis_cmd)

        # position-like analysis
        pos_output = ['position', 'avgx', 'avgy', 'avgz', 'stdx', 'stdBx', 'stdy', 'stdBy', 'stdz', 'stdt', 'nemixrms', 'nemiyrms', 'nemizrms', 'numpar', 'nemirrms', 'avgG', 'avgp', 'stdG', 'avgt', 'avgBx', 'avgBy', 'avgBz', 'CSalphax', 'CSalphay', 'CSbetax', 'CSbetay']
        GPT_pos_analysis_cmd = [r'C:/Program Files/General Particle Tracer/bin/gdfa.exe'] + ['-v'] + ['-o', pos_trial_outfile] + [trial_outfile] + pos_output
        subprocess.call(GPT_pos_analysis_cmd)

    # gets the time analysis file and returns as a series of munch dictionaries
    # use as time, pos, tout, screens = GPT_analyse.get_GDF_anaysis()
    def get_GDF_analysis(self, trial):
        self.run_GDF_analysis(trial)
        
        #paths
        time_trial_outfile = self.GPT_time_file.split('.')[0] + "_" + str(trial) + "."  + self.GPT_time_file.split('.')[1]
        pos_trial_outfile = self.GPT_pos_file.split('.')[0] + "_" + str(trial) + "."  + self.GPT_pos_file.split('.')[1]
        trial_outfile = self.GPToutfile.split('.')[0] + "_" + str(trial) + "."  + self.GPToutfile.split('.')[1]

        # data given using <dict>.<param>.value
        GDFtime = easygdf.load(time_trial_outfile)
        # sort the data (originally as a list of dictionaries) into a munched nested dictionary (keyed on names) 
        GDFtime = munch.munchify({item['name']:item for item in GDFtime['blocks']})

        GDFpos = easygdf.load(pos_trial_outfile)
        # sort the data (originally as a list of dictionaries) into a munched nested dictionary (keyed on names) 
        GDFpos = munch.munchify({item['name']:item for item in GDFpos['blocks']})

        # data given using <dict>[pos].<param>
        GDFbeam = easygdf.load_screens_touts(trial_outfile)
        GDFscreens = munch.munchify(GDFbeam['screens'])
        GDFtouts = munch.munchify(GDFbeam['touts'])
        GDF_analysis = munch.munchify({'time': GDFtime, 'pos': GDFpos, 'touts': GDFtouts, 'screens': GDFscreens})
        return GDF_analysis

    # run multiple or single error runs
    # returns data in an array the length of the no. trials
    def GPT_run_get_analysis(self):
            #multi_analysis = []
            multi_analysis = {}
            for i in range(1, self.ntrial+1):
                self.GPT_run(i)
                multi_analysis['trial_{0}'.format(i)] = self.get_GDF_analysis(i)
                #multi_analysis.append(self.get_GDF_analysis(i))            
            return munch.munchify(multi_analysis)


# test space!
#if __name__ == "__main__":

    # class initialization 
#    GPTrunner = GPT_input_runner('200fC.in', 'GPTin_tolerance.yml')
#    GPTrunner.GPT_run()

    

    


