# generator for Errors
# rejection sampling to impose cut-off

import numpy.random as npr

# Gaussian error generation
def gaussian_error(g_mean, g_std, g_trunc):
    if g_std == 0:
        return g_mean
    else:
        lims = [g_mean-(g_trunc*g_std), g_mean+(g_trunc*g_std)]
        sample = npr.normal(g_mean, g_std)
        while lims[0] >= sample >= lims[1]:
            sample = npr.normal(g_mean, g_std) 
        return sample
    

