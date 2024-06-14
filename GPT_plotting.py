# analyse the GDF file from the error analysis

# GDF reader for GPT created by C. Pierce
# https://github.com/electronsandstuff/easygdf/tree/master
import easygdf
import munch
from matplotlib import pyplot as plt
from scipy import constants

# plotting & analysis functions
# when doing multiple trials I need to change this
# this is now out of date!!
class GPT_plotting:
    def __init__(self, run_data):
        self.run_data = run_data
        
        self.ntrials = len(run_data.keys())
        self.run_keys = list(run_data.keys())

    # ANALYSIS FUNCTIONS

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
        

