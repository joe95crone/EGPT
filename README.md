# EGPT

EGPT is a package in-development to automatically perform error analysis on any existing GPT.in file. Developed initially for a RUEDI user case. The EGPT package takes in a GPT .in file, writes an errored version, takes in user-defined tolerances in a self-generated YAML template, runs the error analysis (sepcified by the user) and analyses the result.  

Repository held at https://gitlab.stfc.ac.uk/fgg55738/egpt.git

See TECH_NOTES repository for further documentation on the function and purpose of this code.

## Dependencies

EGPT is dependent upon several existing pacakages
- re
- itertools
- subprocess
- pyyaml
- munch 
- numpy
- sys
- os
- easygdf - an external package for handling GDF files in python at https://github.com/electronsandstuff/easygdf]

## Python Version & Known issues

Currently uses python 3.10

- THE CODE CURRENTLY IS NOT FINISHED
- Errors in the initial conditions are currently not supported
- Handling of errored beams and errored fieldmaps is not implemented
- 
- All GPT commands are supported but handling for dipoles is only applied to sectormagnet not isectormagnet. Some GPT commands are unsupported because they should not be errored (for example, erroring the acceptable z limits of the simulation is meaningless and bad practice). 

## User Run Guide

The user must supply a configuration file with the GPT location and the users GPT license.

The EGPT code must be ran twice to get a full output, once in Template run mode which generates YAML templates for tolerances and settings 

- The user specifies their GPT .in file 
- Template runs are ran as python GPT_error_run.py <infile>.in which generates a setting template, errored lattice (<infile>_ERR.in) and a YAML tolerance template of the form below 
- The user specifies their tolerances in the YAML tolerance template file 
- Error runs are specified via python GPT_error_run.py <infile>.in <tolerance_file>.yml <settings_file>.yml  
- The GPT_err code runs the error analysis and provides analysis

An example of how to run the code is specified in GPT_error_run, which shows how to setup the various template creation and running stages as well as specifying the analysis.

## Existing Test Cases

- EGPT has been used for energy jitter studies for the RUEDI Imaging line