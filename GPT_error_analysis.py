# analyse the GDF file from the error analysis

# GDF reader for GPT created by C. Pierce
# https://github.com/electronsandstuff/easygdf/tree/master
import easygdf
import subprocess
import munch
from matplotlib import pyplot as plt
from scipy import constants

# plotting & analysis functions
# when doing multiple trials I need to change this
class GPT_analyse:
    def __init__(self, GDFfile='temp.gdf'):
        self.GDFfile = GDFfile 
        self.path = 'D:\\GPT_err\\'
        self.GPToutfile = self.path + self.GDFfile

        self.GPT_time_file = self.GPToutfile.split('.')[0] + "_time." + self.GPToutfile.split('.')[1]
        self.GPT_pos_file = self.GPToutfile.split('.')[0] + '_pos.' + self.GPToutfile.split('.')[1]

    # run the analysis of the GDF output file (time & position)
    def run_GDF_analysis(self):
       # time-like analysis
        time_output = ['time', 'avgx', 'avgy', 'avgz', 'stdx', 'stdBx', 'stdy', 'stdBy', 'stdz', 'nemixrms', 'nemiyrms', 'nemizrms', 'numpar', 'nemirrms', 'avgG', 'avgp', 'stdG', 'avgBx', 'avgBy', 'avgBz', 'CSalphax', 'CSalphay', 'CSbetax', 'CSbetay', 'avgfBx', 'avgfEx', 'avgfBy', 'avgfEy', 'avgfBz', 'avgfEz']
        GPT_time_analysis_cmd = [r'C:/Program Files/General Particle Tracer/bin/gdfa.exe'] + ['-v'] + ['-o', self.GPT_time_file] + [self.GPToutfile] + time_output
        subprocess.call(GPT_time_analysis_cmd)

        # position-like analysis
        pos_output = ['position', 'avgx', 'avgy', 'avgz', 'stdx', 'stdBx', 'stdy', 'stdBy', 'stdz', 'stdt', 'nemixrms', 'nemiyrms', 'nemizrms', 'numpar', 'nemirrms', 'avgG', 'avgp', 'stdG', 'avgt', 'avgBx', 'avgBy', 'avgBz', 'CSalphax', 'CSalphay', 'CSbetax', 'CSbetay']
        GPT_pos_analysis_cmd = [r'C:/Program Files/General Particle Tracer/bin/gdfa.exe'] + ['-v'] + ['-o', self.GPT_pos_file] + [self.GPToutfile] + pos_output
        subprocess.call(GPT_pos_analysis_cmd)

    # gets the time analysis file and returns as a series of munch dictionaries
    # use as time, pos, tout, screens = GPT_analyse.get_GDF_anaysis()
    def get_GDF_analysis(self):
        # run the analysis
        self.run_GDF_analysis()
        # data given using <dict>.<param>.value
        GDFtime = easygdf.load(self.GPT_time_file)
        # sort the data (originally as a list of dictionaries) into a munched nested dictionary (keyed on names) 
        GDFtime = munch.munchify({item['name']:item for item in GDFtime['blocks']})

        GDFpos = easygdf.load(self.GPT_pos_file)
        # sort the data (originally as a list of dictionaries) into a munched nested dictionary (keyed on names) 
        GDFpos = munch.munchify({item['name']:item for item in GDFpos['blocks']})

        # data given using <dict>[pos].<param>
        GDFbeam = easygdf.load_screens_touts(self.GPToutfile)
        GDFscreens = munch.munchify(GDFbeam['screens'])
        GDFtouts = munch.munchify(GDFbeam['touts'])
        return GDFtime, GDFpos, GDFtouts, GDFscreens
    
    # should plotting functions be a child class?
    # do I want to let a user define their own plotting? 

    # example plotting function - beam sizes #sssdsd
    def example_plot(self):    
        time, pos, touts, screens = self.get_GDF_analysis()
        
        plt.figure()
        plt.plot(time.avgz.value, time.stdx.value/constants.micro, label="$\mathregular{\sigma_{x}}$")
        plt.plot(time.avgz.value, time.stdy.value/constants.micro, label="$\mathregular{\sigma_{x}}$")
        plt.title("Time-like")
        plt.xlabel("s [m]")
        plt.ylabel("Beam Size [$\mathregular{\mu}$m]")
        plt.legend()
        plt.show()

