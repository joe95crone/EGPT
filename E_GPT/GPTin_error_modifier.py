# test code for modifying a GPT .in file

import re
from itertools import chain
import munch
import yaml

import os

class GPT_error_mod:
    def __init__(self, filename):
        # read file
        self.EGPTpath = os.path.dirname(os.path.realpath(__file__)) + '\\'

        if '\\' in r'%r' % filename:
            self.infile = filename.split('\\')[-1]
            self.wdEGPTpath = '\\'.join(filename.split('\\')[:-1]) + '\\'
        elif '/' in filename:
            self.infile = filename.split('/')[-1]
            self.wdEGPTpath = '/'.join(filename.split('/')[:-1]) + '/'
        else:
            self.infile = str(filename)
            self.wdEGPTpath = ''

        self.file = open(self.EGPTpath + self.wdEGPTpath + self.infile, 'r')
        self.file_lines = self.file.readlines()

        # possible GPT element types, with no. maximum expected arguments
        self.ECSargs = 11
        # sectormagnets use other coord system, not in-element explicitly stated ones
        self.ECSargs_dip = 3
        # added parameters and added lines expected for one dipole, for spacing of the lattice file only
        self.dipole_param_add = 9
        self.dipole_ccs_add = 4
        self.dipole_add = self.dipole_param_add + self.dipole_ccs_add
        # Contains all elements in the GPT User Manual V3.43. Only elements with ECS are included. The custom coordinate system (CCS) and associated elements (CCSflip) are also excluded.
        # excluding the limitation elements which set the maximum and minimum limits of Lorentz factor and spatial values ('Gminmax','rmax','xymax','zminmax') because these shouldn't be errored upon (doesn't make physical sense)
        # isectormagnet, sectormagnet have fromCCS toCCS format - requires special handling
        self.GPT_command = ['TE011cylcavity','TE011gauss','TE110gauss','TErectcavity','TM010cylcavity','TM110gauss','TM110cylcavity','TM010gauss','TMrectcavity','trwcell','trwlinac','trwlinbm','circlecharge','ecyl','ehole','erect','linecharge','platecharge','pointcharge','barmagnet','Bmultipole','bzsolenoid','isectormagnet','linecurrent','magline','magplane','magdipole','magpoint','quadrupole','rectcoil','rectmagnet','sectormagnet','sextupole','solenoid','map1D_B','map1D_E','map1D_TM','map2D_B','map2D_E','map2D_Et','map2Dr_E','map2D_V','map25D_E','map25D_B','map25D_TM','map3D_E','map3D_TM','map3D_Ecomplex','map3D_Hcomplex','map3D_V','map3D_B','map3D_remove','scatterbitmap','scattercone','scatteriris','scatterpipe','scatterplate','scattersphere','scattertorus','multislit','drift','gauss00mf','undueqfo','unduplan','wakefield']
    
    # helper function
    # returns lattice file
    def line_return(self):
        return self.file_lines
    
    # helper function
    # returns the elements supported by GPT_err
    def supported_elements(self):
        return self.GPT_command
    
    # find the element types that are in the list and their number of instances
    # first instance is the zeroth instance (python numbering)
    def element_types(self):
        # ele_types is [names, instances, index, ele_num]
        ele_types = [[], [], [], []]
        ele_num = 1
        for i in range(len(self.file_lines)):
            # takes first part i.e. element name
            ele_name = re.split(r"[(),#]\s*", self.file_lines[i])[0]
            if ele_name in self.GPT_command:
                ele_types[0].append(ele_name)
                ele_types[1].append(ele_types[0].count(ele_name))
                ele_types[2].append(i)
                ele_types[3].append(ele_num)
                ele_num += 1
        return ele_types
    
    # helper function to get the no. elements
    def element_tabulate(self):
        return self.element_types()[-1][-1]

    # for definiing if the passed line is an element
    def iselement(self, line, ele_name):
        if line.startswith(ele_name):
            if "scatter=" in line or "scatter =" in line:
                return True
            elif "=" not in line:
                return True
            else:
                return False
        else:
            return False


    # takes in the lines of the .in file and GPT name of the element e.g. map1D_B, quadrupole, sectorbend etc.
    def element_index(self, ele_name):
        #ele_indexes = [self.file_lines.index(line) for line in self.file_lines if line.startswith(ele_name) and "=" not in line]
        ele_indexes = [self.file_lines.index(line) for line in self.file_lines if self.iselement(line, ele_name)]
        return ele_indexes

    # takes in a line of the .in file and splits this into parts to access GPT element arguments
    # we can look at the possible instances of the element  
    def element_splitter(self, ele_name, instance):
        # splits string based on delimiters ( , ) plus any additional white space
        #ele_split = re.split(r"[(),#]\s*", self.file_lines[self.element_index(ele_name)[instance-1]])

        if '#' in self.file_lines[self.element_index(ele_name)[instance-1]]:
            ele_split = [self.file_lines[self.element_index(ele_name)[instance-1]].split('(', 1)[0]] + re.split(r"[,]\s*", self.file_lines[self.element_index(ele_name)[instance-1]].split('(', 1)[1].rsplit(')', 1)[0]) + [self.file_lines[self.element_index(ele_name)[instance-1]].split('(', 1)[1].rsplit(')', 1)[1].split('#', 1)[0]] 
        elif 'scatter=' in self.file_lines[self.element_index(ele_name)[instance-1]] or 'scatter =' in self.file_lines[self.element_index(ele_name)[instance-1]]:
            ele_split = [self.file_lines[self.element_index(ele_name)[instance-1]].split('(', 1)[0]] + re.split(r"[,]\s*", self.file_lines[self.element_index(ele_name)[instance-1]].split('(', 1)[1].rsplit(')', 1)[0]) + [self.file_lines[self.element_index(ele_name)[instance-1]].split('(', 1)[1].rsplit(')', 1)[1]]
            ele_split = ele_split[:-1] + [ele_split[-1].split(';')[0], ';' + ele_split[-1].split(';')[-1]]
        else:
            ele_split = [self.file_lines[self.element_index(ele_name)[instance-1]].split('(', 1)[0]] + re.split(r"[,]\s*", self.file_lines[self.element_index(ele_name)[instance-1]].split('(', 1)[1].rsplit(')', 1)[0]) + [self.file_lines[self.element_index(ele_name)[instance-1]].split('(', 1)[1].rsplit(')', 1)[1]]
        # remove any comments past ; - this may need some work to be more robust
        try:
            ele_split = ele_split[:ele_split.index(";\n")]
        except ValueError:
            try: 
                ele_split = ele_split[:ele_split.index(" ;\n")]
            except ValueError:
                ele_split = ele_split[:ele_split.index("; ")]
        ele_split.append(";\n")
        return ele_split

    # input misalignment based on GPT ECS format i.e. ECS replacer
    #! this will need a special case for any bending elements
    # end part of full_ECS deal with rotations about the z axis. Other rotations are not supported, yet! This carries over any other rotations
    def ECS_replacer(self, ele_name, instance, ele_num):
        ele_split = self.element_splitter(ele_name, instance)
        # 'z'-type and full-type ECS are of different length and split differently because 'wcs','z',oz against 'wcs',ox,oy,oz (extra character)
        if ele_split[2] == '"z"':
            # full ECS with misalignment and ccs label, z position ported over
            full_ECS = [ele_split[1], "0 + dx{0}".format(ele_num), "0 + dy{0}".format(ele_num), ele_split[3] + " + dz{0}".format(ele_num), "cos(th{0})".format(ele_num), "-sin(th{0})".format(ele_num), "0", "sin(th{0})".format(ele_num), "cos(th{0})".format(ele_num), "0"]
            # # remove old ECS
            del ele_split[1:4]
            # add new ECS
            ele_split[1:1] = full_ECS
            return ele_split
        # identity matrix placement ECS replacement (not actually sure if this is needed...)
        elif ele_split[2] == "I":
            # full ECS with misalignment and ccs label
            full_ECS = [ele_split[1], "0 + dx{0}".format(ele_num), "0 + dy{0}".format(ele_num),  "0 + dz{0}".format(ele_num), "cos(th{0})".format(ele_num), "-sin(th{0})".format(ele_num), "0", "sin(th{0})".format(ele_num), "cos(th{0})".format(ele_num), "0"]
            # # remove old ECS
            del ele_split[1:4]
            # add new ECS
            ele_split[1:1] = full_ECS
            return ele_split
        # here is the dipole modification
        # saying that is the element constants
        elif ele_split[0] == 'sectormagnet': 
            if len(ele_split[1].split('"')[1].split('_')) == 1:
                ele_split[1] = '"' + ele_split[1].split('"')[1] + '_err' + '"'
            else:
                ele_split[1] ='"' + ele_split[1].split('"')[1].split('_')[0] + '_err_ent_' + ele_split[1].split('"')[1].split('_')[1] + '"'
            if len(ele_split[2].split('"')[1].split('_')) == 1:
                ele_split[2] = '"' + ele_split[2].split('"')[1] + '_err' + '"'
            else:
                ele_split[2] ='"' + ele_split[2].split('"')[1].split('_')[0] + '_err_ext_' + ele_split[2].split('"')[1].split('_')[1] + '"'
            return ele_split 
        else:
            # full ECS with misalignment and ccs label, all other x, y, z offsets and rotations ported
            full_ECS = [ele_split[1], ele_split[2] + " + dx{0}".format(ele_num), ele_split[3] + " + dy{0}".format(ele_num), ele_split[4] + " + dz{0}".format(ele_num), ele_split[5] + "+ cos(th{0})".format(ele_num), ele_split[6] + " -sin(th{0})".format(ele_num), ele_split[7] + " + 0", ele_split[8] + "+ sin(th{0})".format(ele_num), ele_split[9] + " + cos(th{0})".format(ele_num), ele_split[10] + " + 0"]
            #remove old ECS 
            del ele_split[1:11]
            # add new ECS
            ele_split[1:1] = full_ECS
            return ele_split

    # replaces errored parameters with f_param*param + d_param
    #! add filenames etc. for potentially erroring maps by more than amplitude at a later date
    def param_replacer(self, ele_name, instance, ele_num):
        # first get the ECS replaced/standardised version
        param_rep = self.ECS_replacer(ele_name, instance, ele_num)
        # list of the parameter tags for specifying input (f_<param>_<ele_num>, d_<param>_<ele_num>)
        err_param_ident = []
        # from the end of the ECS to the semi-colon/line end 
        if param_rep[0] == 'sectormagnet':
            # currently just changes the names of the dipole parameters in the lattice file
            #! all dipole parameters must be passed as variables
            for params in range(self.ECSargs_dip, len(param_rep)-1):
                if '"' not in param_rep[params]:
                    param_rep[params] = "{0}".format(param_rep[params].split('_')[0] + "_err_" + param_rep[params].split('_')[1])
            return [param_rep, err_param_ident]
        else:
            for params in range(self.ECSargs, len(param_rep)-1):
                if '"' not in param_rep[params]:
                    param_rep[params] = "f_{0}_{1}*{2} + d_{0}_{1}".format(params, ele_num, param_rep[params])
                    err_param_ident.append("{0}_{1}".format(params, ele_num))
            return [param_rep, err_param_ident]

    # does element replacing then re-writes string
    def element_replace(self, ele_name, instance, ele_num):
        #ele_replace = self.ECS_replacer(ele_name, instance, ele_num) # for ECS only
        ele_dat = self.param_replacer(ele_name, instance, ele_num)
        ele_replace = ele_dat[0]
        # handling if there is a scatter="sm" outside of the parenthesis
        if any("scatter=" in rec_param for rec_param in ele_replace) or any("scatter =" in rec_param for rec_param in ele_replace):
            ele_recomb = ele_replace[0] + "(" + ','.join(ele_replace[1:-2]) + ")" + ele_replace[-2] + ele_replace[-1]
        else:
            ele_recomb = ele_replace[0] + "(" + ','.join(ele_replace[1:-1]) + ")" + ele_replace[-1]
        return [ele_recomb, ele_dat[1]]
    
    # formatting of the error parameters required
    def error_param_format(self, err_param):
        err_param = list(chain.from_iterable(err_param))
        fparams = ['f_' + s for s in err_param]
        dparams = ['d_' + s for s in err_param]
        # get number of elements
        no_eles = self.element_tabulate()
        misalignparams = []
        for i in range(1,no_eles+1):
            misalignparams.append('dx' + str(i))
            misalignparams.append('dy' + str(i))
            misalignparams.append('dz' + str(i))
            misalignparams.append('th' + str(i))
        # sort using regex splitting on element number
        err_param = sorted(misalignparams + fparams + dparams, key = lambda sub : int(re.split(r'\D+',sub)[-1]))
        return err_param

    # generate the dipole ccs's that are in the lattice and add these to the lattice 
    def add_dipole_ccs(self, new_lattice):
        # gets all the element numbers, lines etc. of dipole
        dipole_dat = [list(map(list, zip(*self.element_types())))[i] for i, x in enumerate(self.element_types()[0]) if x == "sectormagnet"]
        # gets the dipole end co-ordinate system
        for dip_no in range(len(dipole_dat)): 
            for line in self.file_lines:
                if 'ccs' in line and self.element_splitter(dipole_dat[dip_no][0], dipole_dat[dip_no][1])[2] in line:
                    if '#' in line:
                        orig_ccs = [line.split('(', 1)[0]] + re.split(r"[,]\s*", line.split('(', 1)[1].rsplit(')', 1)[0]) + [line.split('(', 1)[1].rsplit(')', 1)[1].split('#', 1)[0]]
                    else:
                        orig_ccs = [line.split('(', 1)[0]] + re.split(r"[,]\s*", line.split('(', 1)[1].rsplit(')', 1)[0]) + [line.split('(', 1)[1].rsplit(')', 1)[1]]
                    #creating the new ccs & ccsflip elements - some have to have special handling for wcs to bend_# style co-ord systems for the first dipole 
                    if dip_no == 0:
                        misaligned_start_ccs = orig_ccs[0] + "(" + orig_ccs[1] + ',' + orig_ccs[2] + " + dx{0}".format(dipole_dat[dip_no][-1]) + ',' + orig_ccs[3] + " + dy{0}".format(dipole_dat[dip_no][-1]) + ',' + orig_ccs[4].split('+', 1)[0] + " + dz{0}".format(dipole_dat[dip_no][-1]) + ',' + '1, 0, 0, 0, 1, 0,' + '"' + orig_ccs[1].split('"')[1] + '_err"' + ')' + orig_ccs[-1]
                        misaligned_start_ccsflip = orig_ccs[0] + "flip" + "(" + orig_ccs[1] + ',' + '"z"' + ',' + orig_ccs[4].split('+', 1)[0] + " + dz{0}".format(dipole_dat[dip_no][-1]) + ',' + '"' + orig_ccs[1].split('"')[1] + '_err"' + ')' + orig_ccs[-1]
                    else:
                        misaligned_start_ccs = orig_ccs[0] + "(" + orig_ccs[1] + ',' + orig_ccs[2] + " + dx{0}".format(dipole_dat[dip_no][-1]) + ',' + orig_ccs[3] + " + dy{0}".format(dipole_dat[dip_no][-1]) + ',' + orig_ccs[4].split('+', 1)[0] + " + dz{0}".format(dipole_dat[dip_no][-1]) + ',' + '1, 0, 0, 0, 1, 0,' + orig_ccs[1].split('_', 1)[0] + '_err_ent_' + orig_ccs[1].split('_', 1)[1] + ')' + orig_ccs[-1]
                        misaligned_start_ccsflip = orig_ccs[0] + "flip" + "(" + orig_ccs[1] + ',' + '"z"' + ',' + orig_ccs[4].split('+', 1)[0] + " + dz{0}".format(dipole_dat[dip_no][-1]) + ',' + orig_ccs[1].split('_', 1)[0] + '_err_ent_' + orig_ccs[1].split('_', 1)[1] + ')' + orig_ccs[-1]
                    misaligned_dipole_ccs = orig_ccs[0] + "(" + orig_ccs[1] + ',' + orig_ccs[2] + " + dx{0}".format(dipole_dat[dip_no][-1]) + ',' + orig_ccs[3] + " + dy{0}".format(dipole_dat[dip_no][-1]) + ',' + orig_ccs[4] + " + dz{0}".format(dipole_dat[dip_no][-1]) + ',' + orig_ccs[5] +  " + cos(th{0})".format(dipole_dat[dip_no][-1]) + ',' + orig_ccs[6] + " -sin(th{0})".format(dipole_dat[dip_no][-1]) + ',' + orig_ccs[7] + " + 0" + ',' + orig_ccs[8] + " + sin(th{0})".format(dipole_dat[dip_no][-1]) + ',' + orig_ccs[9] + " + cos(th{0})".format(dipole_dat[dip_no][-1]) + ',' + orig_ccs[10] + " + 0" + ',' + orig_ccs[11].split('_')[0] + '_err_ext_' + orig_ccs[11].split('_')[1] + ")" + orig_ccs[-1]
                    misaligned_dipole_ccsflip = orig_ccs[0] + "flip" + "(" + orig_ccs[11].split('_')[0] + '_err_ext_' + orig_ccs[11].split('_')[1] + ',' + '"z"' + ',' + 'Ldip_err_{0} - intersect_err_{0}'.format(dipole_dat[dip_no][1]) + ',' + orig_ccs[11] + ")" + orig_ccs[-1]
                    break
                    # adding the new ccs & ccsflip elements to the lattice
            new_lattice.insert(dipole_dat[dip_no][2] + dip_no*self.dipole_ccs_add, misaligned_dipole_ccs)
            new_lattice.insert(dipole_dat[dip_no][2] + dip_no*self.dipole_ccs_add, misaligned_start_ccsflip)
            new_lattice.insert(dipole_dat[dip_no][2] + dip_no*self.dipole_ccs_add, misaligned_start_ccs)
            new_lattice.insert(dipole_dat[dip_no][2] + (dip_no+1)*self.dipole_ccs_add, misaligned_dipole_ccsflip)   
        return new_lattice

    def replace_dipole_params(self, text, dic):
        for i, j in dic.items():
            text = text.replace(i, j)
        return text

    def add_dipole_err_params(self, new_lattice):
        dipole_dat = [list(map(list, zip(*self.element_types())))[i] for i, x in enumerate(self.element_types()[0]) if x == "sectormagnet"]
        # list of params
        dip_var_params = {'Ldip': 'Ldip_err', 'bendang': 'bendang_err', 'phiin': 'phiin_err', 'phiout': 'phiout_err', 'dl': 'dl_err', 'b1': 'b1_err', 'b2': 'b2_err'}
        dip_params = dip_var_params | {'Bfield': 'Bfield_err', 'Rbend': 'Rbend_err', 'intersect': 'intersect_err'}
        # generate the new dipole parameter definitions and their errorable parameters
        err_params = []
        for dip_no in range(len(dipole_dat)):
            param_no = 1
            new_lines = []
            line_indexes = []
            for line in new_lattice:
                # find just the dipole parameters to error in the lattice fil (exclude already errored elements and screens)
                if any(i in line for i in list(dip_params.keys())) and '_{0}'.format(dip_no+1) in line and 'err' not in line and 'ccs' not in line and 'screen' not in line and all(i not in line for i in self.GPT_command) and line[0] != '#':
                    new_line = self.replace_dipole_params(line, dip_params)
                    # loop to put the f_ and d_ into the dependent parameters 
                    if any(i in new_line.split('=')[0] for i in list(dip_var_params.keys())):
                        new_lines.append(new_line.split('=')[0] + '=' + 'f_{0}_{1}*('.format(param_no, dipole_dat[dip_no][-1]) + new_line.split('=')[1].split(';')[0] + ') + d_{0}_{1}'.format(param_no, dipole_dat[dip_no][-1]) + ';' + new_line.split('=')[1].split(';')[1])
                        err_params.append('{0}_{1}'.format(param_no, dipole_dat[dip_no][-1]))
                        param_no += 1 
                    else:
                        new_lines.append(new_line)
                    line_indexes.append(new_lattice.index(line))
            # write the new parameter definitions to the lattice file        
            for i in range(len(new_lines)):
                new_lattice.insert(line_indexes[i] + 1 + i, new_lines[i])
        # partition err_params for each dipole
        err_params = [err_params[i:i + len(dip_var_params.keys())] for i in range(0, len(err_params), len(dip_var_params.keys()))]
        return new_lattice, err_params

    # applies element replace to all identified elements then writes the errored lattice file
    # also returns the identifiers of the element parameters
    def lattice_replacer(self):
        ident_eles = self.element_types()
        new_lattice = []
        err_param_ident = []
        for i in range(len(self.file_lines)):
            if i in ident_eles[2]:   
                new_lattice.append(self.element_replace(ident_eles[0][ident_eles[2].index(i)], ident_eles[1][ident_eles[2].index(i)], ident_eles[3][ident_eles[2].index(i)])[0])
                err_param_ident.append(self.element_replace(ident_eles[0][ident_eles[2].index(i)], ident_eles[1][ident_eles[2].index(i)], ident_eles[3][ident_eles[2].index(i)])[1])
            else:
                new_lattice.append(self.file_lines[i])
        # only run if dipoles in lattice
        if 'sectormagnet' in ident_eles[0]:
            # add dipole misalignments
            new_lattice = self.add_dipole_ccs(new_lattice)
            # add dipole parameters
            new_lattice, dip_err_params = self.add_dipole_err_params_new(new_lattice)
            # pre-dipole lattice (temporary)
            #filename_postdip = self.EGPTpath + self.wdEGPTpath + self.infile.split('.')[0] + '_ERR_POSTDIP' + '.' + self.infile.split('.')[-1]
            #GPTwrite_postdip = open(filename_postdip, "w") # overwrites if previously generated!
            #GPTwrite_postdip.writelines(new_lattice)
            # modify ident_eles to include dipole parameters
            for ele in range(len(err_param_ident)):
                if ident_eles[0][ele] == 'sectormagnet':
                    err_param_ident[ele] = dip_err_params[ident_eles[1][ele]-1]
        # write out the lattice file
        filename = self.EGPTpath + self.wdEGPTpath + self.infile.split('.')[0] + '_ERR' + '.' + self.infile.split('.')[-1]
        GPTwrite = open(filename, "w") # overwrites if previously generated!
        GPTwrite.writelines(new_lattice)
        GPTwrite.close()
        return self.error_param_format(err_param_ident)

    def parameter_name_sorter(self, error_param_names):
        sorted_params = []
        sort_ele = []
        ele_no = 1
        for param in error_param_names:
            # regex splitting on element numb
            if int(re.split(r'\D+',param)[-1]) == ele_no:
                sort_ele.append(param)
            else:
                sorted_params.append(sort_ele)
                sort_ele = []
                sort_ele.append(param) 
                ele_no +=1
        sorted_params.append(sort_ele)
        return sorted_params

    def lattice_replacer_template(self):
        # run lattice replacer
        error_param_names = self.parameter_name_sorter(self.lattice_replacer())
        element_names_yaml = [self.element_types()[0][i] + "_" + str(self.element_types()[1][i]) for i in range(len(self.element_types()[0]))]
        # creating the template dictionary
        ele_err_dict = munch.Munch()
        for ele in range(len(element_names_yaml)):
            ele_err_dict.update({element_names_yaml[ele]: {}})
            ele_param_dict = munch.Munch()
            for param in range(len(error_param_names[ele])):
                # mean, tolerance, error type, truncation (no. sigma)
                if error_param_names[ele][param][0] == 'd' or error_param_names[ele][param][0] == 't':
                    ele_param_dict[error_param_names[ele][param]] = [0, 0, 'gaussian', 3]
                else:
                    ele_param_dict[error_param_names[ele][param]] = [1, 0, 'gaussian', 3]
            setattr(ele_err_dict, element_names_yaml[ele], ele_param_dict)
        # create YAML tolerance template
        filename = self.EGPTpath + self.wdEGPTpath + 'GPTin_tolerance_temp.yml'
        with open(filename, 'w') as tempfile:
            yaml.dump(munch.unmunchify(ele_err_dict), tempfile, sort_keys=False)
