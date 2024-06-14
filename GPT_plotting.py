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
    def __init__(self, time, pos, touts, screens):
        self.time = time
        self.pos = pos
        self.touts = touts
        self.screens = screens

    # example plotting function - beam sizes
    def beam_size(self):    
        plt.figure()
        plt.plot(self.time.avgz.value, self.time.stdx.value/constants.micro, label="$\mathregular{\sigma_{x}}$")
        plt.plot(self.time.avgz.value, self.time.stdy.value/constants.micro, label="$\mathregular{\sigma_{x}}$")
        plt.title("Time-like")
        plt.xlabel("s [m]")
        plt.ylabel("Beam Size [$\mathregular{\mu}$m]")
        plt.legend()
        plt.show()

