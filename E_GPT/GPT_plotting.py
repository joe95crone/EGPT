# analyse the GDF file from the error analysis

# GDF reader for GPT created by C. Pierce
# https://github.com/electronsandstuff/easygdf/tree/master
import easygdf
import munch
from matplotlib import pyplot as plt
from scipy import constants
import numpy as np
import os

 
# plotting & analysis functions
class GPT_plotting:
    def __init__(self, run_data, infile):
        self.run_data = run_data
        
        self.ntrials = len(run_data.keys())
        self.run_keys = list(run_data.keys())

        self.EGPTpath = os.path.dirname(os.path.realpath(__file__)) + '\\'

        if '\\' in r'%r' % infile:
            self.GPTinfile = infile.split('\\')[-1]
            self.wdEGPTpath = '\\'.join(infile.split('\\')[:-1]) + '\\'
        elif '/' in infile:
            self.GPTinfile = infile.split('/')[-1]
            self.wdEGPTpath = '/'.join(infile.split('/')[:-1]) + '/'
        else:
            self.GPTinfile = str(infile)
            self.wdEGPTpath = ''

        # create a directory for plots
        if os.path.exists(self.EGPTpath + self.wdEGPTpath + "FIGS") == False:
            os.mkdir(self.EGPTpath + self.wdEGPTpath + "FIGS")
    # ANALYSIS FUNCTIONS
    #def mean_analysis_value(self, analysis_param):
    #    # step over each timestep
    #    mean_analysis = []
    #    for step in range(self.trial_1.time.avgz.value):
    #        # for each trial
    #        mean_analysis_step = []
    #        for i in range(1,self.ntrials+1):
    #            mean_analysis_step.append(getattr(getattr(self.run_data, self.run_keys[i-1]).time, analysis_param).value[step])

    # get Lorentz speed Factor - position based only
    # only required for position analysis
    def Lorentz_speed_fac_pos(self):
        return self.run_data.trial_1.pos.avgBz.value

    # Sorting function based on position - returns an ordered list of the indexes
    def position_sort(self):
        # sorts using avgt
        indexes = sorted(range(len(self.run_data.trial_1.pos.avgt.value)), key=lambda k: self.run_data.trial_1.pos.avgt.value[k])
        return indexes

    # calculates the energy and energy spread jitter parameters at the end position of the line
    #! WARNING: this assumes that the furthest position value is the end of the line (can be false for many co-ordinate systems)
    def trial_energy(self):
        pos_index = np.argmax(self.run_data.trial_1.pos.position.value)
        energy_vals = []
        energy_spread_vals = []
        for i in range(1, self.ntrials+1):
            energy_vals.append(getattr(self.run_data, self.run_keys[i-1]).pos.avgG.value[pos_index])
            energy_spread_vals.append(getattr(self.run_data, self.run_keys[i-1]).pos.stdG.value[pos_index])
        rel_energy_spread_vals = np.array(energy_spread_vals)/np.array(energy_vals)
        energy_vals = np.array(energy_vals)*constants.value('electron mass energy equivalent in MeV') - constants.value('electron mass energy equivalent in MeV')
        rms_energy_deviation = np.sqrt(np.mean((np.mean(energy_vals) - energy_vals)**2))
        rms_rel_energy_spread_deviation = np.sqrt(np.mean((np.mean(rel_energy_spread_vals) - rel_energy_spread_vals)**2))

        print('Mean Energy: {0:.3f} MeV'.format(np.mean(energy_vals)))
        print('Rms Energy Deviation: {0:.3f} keV'.format(rms_energy_deviation/(constants.kilo/constants.mega)))
        print('Mean Rel. Energy Spread: {0}'.format(np.mean(rel_energy_spread_vals)))
        print('Rms Rel. Energy Spread Variation: {0}'.format(rms_rel_energy_spread_deviation))

    # plots energy spread and energy jitter through the beamline
    #! assumes the beamline is straight (uses junky position ordering)
    def trial_energy_plot(self):
        indexes = self.position_sort()
        position = np.array(self.run_data.trial_1.pos.position.value)[indexes]

        energy_vals = [[getattr(self.run_data, self.run_keys[i-1]).pos.avgG.value[pos_index] for i in range(1, self.ntrials+1)] for pos_index in indexes]
        energy_vals = np.array(energy_vals)*constants.value('electron mass energy equivalent in MeV') - constants.value('electron mass energy equivalent in MeV')
        
        energy_spread_vals = [[getattr(self.run_data, self.run_keys[i-1]).pos.stdG.value[pos_index] for i in range(1, self.ntrials+1)] for pos_index in indexes]
        rel_energy_spread_vals = np.array(energy_spread_vals)/np.array(energy_vals)

        mean_energy_vals = np.array([np.mean(energy_vals[i,:]) for i in range(len(indexes))])
        rms_energy_deviation = np.array([np.sqrt(np.mean((np.mean(energy_vals[i,:]) - energy_vals[i,:])**2)) for i in range(len(indexes))])
        rel_energy_deviation = (rms_energy_deviation/mean_energy_vals)*100

        mean_rel_energy_spread_vals = np.array([np.mean(rel_energy_spread_vals[i,:]) for i in range(len(indexes))])
        rms_rel_energy_spread_variation = (np.array([np.sqrt(np.mean((np.mean(rel_energy_spread_vals[i,:]) - rel_energy_spread_vals[i,:])**2)) for i in range(len(indexes))])/mean_rel_energy_spread_vals)*100

        plt.figure(1)
        plt.plot(position, mean_energy_vals, c='red')
        plt.title('Mean Energy (Position-like)')
        plt.xlabel('s [m]')
        plt.ylabel('Mean Energy [MeV]')
        plt.savefig(self.EGPTpath + self.wdEGPTpath + 'FIGS/RUEDI_Imaging_Mean_Energy.png')
        
        plt.figure(2)
        plt.plot(position, rel_energy_deviation, c='blue')
        plt.title('Rel. Energy Deviation  (Position-like)')
        plt.xlabel('s [m]')
        plt.ylabel('Rel. Rms (1$\mathregular{\sigma}$) Energy Deviation [%]')
        plt.savefig(self.EGPTpath + self.wdEGPTpath + 'FIGS/RUEDI_Imaging_Rel_Energy_Deviation.png')

        plt.figure(3)
        plt.plot(position, mean_rel_energy_spread_vals, c='red')
        plt.title('Mean Rel. Energy Spread (Position-like)')
        plt.xlabel('s [m]')
        plt.ylabel('Mean Rms Rel. Energy Spread [%]')
        plt.savefig(self.EGPTpath + self.wdEGPTpath + 'FIGS/RUEDI_Imaging_Mean_Energy_Spread.png')

        plt.figure(4)
        plt.plot(position, rms_rel_energy_spread_variation, c='blue')
        plt.title('Rms Rel. Energy Spread Deviation (Position-like)')
        plt.xlabel('s [m]')
        plt.ylabel('Rms (1$\mathregular{\sigma}$) Rel. Energy Spread Deviation [%]')
        plt.savefig(self.EGPTpath + self.wdEGPTpath + 'FIGS/RUEDI_Imaging_Rel_Energy_Spread_Deviation.png')
        plt.show()

    # PLOTTING FUNCTIONS
    # beam size plot
    def beam_size(self, TP_flag='time'):    
        plt.figure()
        plt.xlabel("s [m]")
        plt.ylabel("Beam Size [$\mathregular{\mu}$m]")
        if TP_flag == 'time': 
            for i in range(1,self.ntrials+1):
                plt.plot(getattr(self.run_data, self.run_keys[i-1]).time.avgz.value, getattr(self.run_data, self.run_keys[i-1]).time.stdx.value/constants.micro, label="$\mathregular{\sigma_{x}}$ " + self.run_keys[i-1])
                plt.plot(getattr(self.run_data, self.run_keys[i-1]).time.avgz.value, getattr(self.run_data, self.run_keys[i-1]).time.stdy.value/constants.micro, label="$\mathregular{\sigma_{y}}$ " + self.run_keys[i-1])
            plt.legend()
            plt.title("Time-like")
            plt.savefig(self.EGPTpath + self.wdEGPTpath + 'FIGS\Beamsize_time.png')
        elif TP_flag == 'pos':
            indexes = self.position_sort()
            beta_fac = self.Lorentz_speed_fac_pos()
            for i in range(1,self.ntrials+1):
                plt.plot(getattr(self.run_data, self.run_keys[i-1]).pos.avgt.value[indexes]*constants.c*beta_fac[indexes], getattr(self.run_data, self.run_keys[i-1]).pos.stdx.value[indexes]/constants.micro, label="$\mathregular{\sigma_{x}}$ " + self.run_keys[i-1])
                plt.plot(getattr(self.run_data, self.run_keys[i-1]).pos.avgt.value[indexes]*constants.c*beta_fac[indexes], getattr(self.run_data, self.run_keys[i-1]).pos.stdy.value[indexes]/constants.micro, label="$\mathregular{\sigma_{y}}$ " + self.run_keys[i-1])
            plt.legend()
            plt.title('Position-like')
            plt.savefig(self.EGPTpath + self.wdEGPTpath + 'FIGS\Beamsize_pos.png')        
        plt.show()

    def trajectory(self, TP_flag='time'):    
        plt.figure()
        plt.xlabel("s [m]")
        plt.ylabel("Trajectory [$\mathregular{\mu}$m]")
        if TP_flag == 'time':
            for i in range(1,self.ntrials+1):
                plt.plot(getattr(self.run_data, self.run_keys[i-1]).time.avgz.value, getattr(self.run_data, self.run_keys[i-1]).time.avgx.value/constants.micro, label="X " + self.run_keys[i-1])
                plt.plot(getattr(self.run_data, self.run_keys[i-1]).time.avgz.value, getattr(self.run_data, self.run_keys[i-1]).time.avgy.value/constants.micro, label="Y " + self.run_keys[i-1])
            plt.title("Time-like")
            plt.legend()
            plt.savefig(self.EGPTpath + self.wdEGPTpath + 'FIGS\Trajectory_time.png')
        elif TP_flag == 'pos':
            indexes = self.position_sort()
            beta_fac = self.Lorentz_speed_fac_pos()
            for i in range(1, self.ntrials+1):
                plt.plot(getattr(self.run_data, self.run_keys[i-1]).pos.avgt.value[indexes]*constants.c*beta_fac[indexes], getattr(self.run_data, self.run_keys[i-1]).pos.avgx.value[indexes]/constants.micro, label="X " + self.run_keys[i-1])
                plt.plot(getattr(self.run_data, self.run_keys[i-1]).pos.avgt.value[indexes]*constants.c*beta_fac[indexes], getattr(self.run_data, self.run_keys[i-1]).pos.avgy.value[indexes]/constants.micro, label="Y " + self.run_keys[i-1])
            plt.title("Position-like")
            plt.legend()
            plt.savefig(self.EGPTpath + self.wdEGPTpath + 'FIGS\Trajectory_pos.png')
        plt.show()