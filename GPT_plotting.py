# analyse the GDF file from the error analysis

# GDF reader for GPT created by C. Pierce
# https://github.com/electronsandstuff/easygdf/tree/master
import easygdf
import munch
from matplotlib import pyplot as plt
from scipy import constants
import numpy as np

# plotting & analysis functions
# when doing multiple trials I need to change this
# this is now out of date!!
class GPT_plotting:
    def __init__(self, run_data):
        self.run_data = run_data
        
        self.ntrials = len(run_data.keys())
        self.run_keys = list(run_data.keys())

    # ANALYSIS FUNCTIONS
    #def mean_analysis_value(self, analysis_param):
    #    # step over each timestep
    #    mean_analysis = []
    #    for step in range(self.trial_1.time.avgz.value):
    #        # for each trial
    #        mean_analysis_step = []
    #        for i in range(1,self.ntrials+1):
    #            mean_analysis_step.append(getattr(getattr(self.run_data, self.run_keys[i-1]).time, analysis_param).value[step])
            
    def trial_energy(self):
        pos_index = np.argmax(self.run_data.trial_1.pos.position.value)
        energy_vals = []
        for i in range(1, self.ntrials+1):
            energy_vals.append(getattr(self.run_data, self.run_keys[i-1]).pos.avgG.value[pos_index])
        energy_vals = np.array(energy_vals)*constants.value('electron mass energy equivalent in MeV') - constants.value('electron mass energy equivalent in MeV')
        print(energy_vals)

    # PLOTTING FUNCTIONS
    # beam size plot
    def beam_size(self):    
        plt.figure()
        for i in range(1,self.ntrials+1):
            plt.plot(getattr(self.run_data, self.run_keys[i-1]).time.avgz.value, getattr(self.run_data, self.run_keys[i-1]).time.stdx.value/constants.micro, label="$\mathregular{\sigma_{x}}$ " + self.run_keys[i-1])
            plt.plot(getattr(self.run_data, self.run_keys[i-1]).time.avgz.value, getattr(self.run_data, self.run_keys[i-1]).time.stdy.value/constants.micro, label="$\mathregular{\sigma_{y}}$ " + self.run_keys[i-1])
        plt.title("Time-like")
        plt.xlabel("s [m]")
        plt.ylabel("Beam Size [$\mathregular{\mu}$m]")
        #plt.legend()
        plt.savefig('FIGS\Beamsize.png')
        plt.show()

    def trajectory(self):    
        plt.figure()
        for i in range(1,self.ntrials+1):
            plt.plot(getattr(self.run_data, self.run_keys[i-1]).time.avgz.value, getattr(self.run_data, self.run_keys[i-1]).time.avgx.value/constants.micro, label="X " + self.run_keys[i-1])
            plt.plot(getattr(self.run_data, self.run_keys[i-1]).time.avgz.value, getattr(self.run_data, self.run_keys[i-1]).time.avgy.value/constants.micro, label="Y " + self.run_keys[i-1])
        plt.title("Time-like")
        plt.xlabel("s [m]")
        plt.ylabel("Trajectory [$\mathregular{\mu}$m]")
        #plt.legend()
        plt.savefig('FIGS\Trajectory.png')
        plt.show()
        

