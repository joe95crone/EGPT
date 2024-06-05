# test code for modifying a GPT .in file

import re
from itertools import chain
import munch
import yaml

class GPT_error_mod:
    def __init__(self, filename):
        # read file
        self.infile = str(filename)
        self.file = open(self.infile, 'r')
        self.file_lines = self.file.readlines()
        # possible GPT element types, with no. maximum expected arguments
        self.ECSargs = 11
        self.GPT_command = ['map1D_TM', 'map1D_B', 'quadrupole', 'sectorbend']
    
    def line_return(self):
        return self.file_lines
    
    def supported_elements(self):
        return 
    
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

    # takes in the lines of the .in file and GPT name of the element e.g. map1D_B, quadrupole, sectorbend etc.
    def element_index(self, ele_name):
        ele_indexes = [self.file_lines.index(line) for line in self.file_lines if line.startswith(ele_name)]
        return ele_indexes
             
    # takes in a line of the .in file and splits this into parts to access GPT element arguments
    # we can look at the possible instances of the element  
    def element_splitter(self, ele_name, instance):
        # splits string based on delimiters ( , ) plus any additional white space
        ele_split = re.split(r"[(),#]\s*", self.file_lines[self.element_index(ele_name)[instance-1]])
        # remove any comments past ; - this may need some work to be more robust
        try:
            ele_split = ele_split[:ele_split.index(";\n")]
        except ValueError:
            ele_split = ele_split[:ele_split.index("; ")]
        ele_split.append(";\n")
        return ele_split
    
    # input misalignment based on GPT ECS format i.e. ECS replacer
    #! this will need modifying for any bending elements
    #! eventually change the end part of full_ECS to deal with rotations   
    def ECS_replacer(self, ele_name, instance, ele_num):
        ele_split = self.element_splitter(ele_name, instance)
        if ele_split[2] == '"z"':
            # full ECS with misalignment and ccs label, z position ported over
            full_ECS = [ele_split[1], "0 + dx{0}".format(ele_num), "0 + dy{0}".format(ele_num), ele_split[3] + " + dz{0}".format(ele_num), "1", "0", "0","0","1","0"]
            # remove old ECS
            del ele_split[1:4]
            # add new ECS
            ele_split[1:1] = full_ECS
            return ele_split
        else:
            # full ECS with misalignment and ccs label, all othe x, y, z offsets ported
            full_ECS = [ele_split[1], ele_split[2] + " + dx{0}".format(ele_num), ele_split[3] + " + dy{0}".format(ele_num), ele_split[4] + " + dz{0}".format(ele_num), "1", "0", "0","0","1","0"]
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
        for params in range(self.ECSargs, len(param_rep)-1):
            #if self.is_number(param_rep[params]) == True:
            #    param_rep[params] = "f_{0}_{1}*{2} + d_{0}_{1}".format(params, ele_num, param_rep[params])
            if '"' not in param_rep[params]:
                param_rep[params] = "f_{0}_{1}*{2} + d_{0}_{1}".format(params, ele_num, param_rep[params])
                err_param_ident.append("{0}_{1}".format(params, ele_num))
        return [param_rep, err_param_ident]

    # does element replacing then re-writes string
    def element_replace(self, ele_name, instance, ele_num):
        #ele_replace = self.ECS_replacer(ele_name, instance, ele_num) # for ECS only
        ele_dat = self.param_replacer(ele_name, instance, ele_num)
        ele_replace = ele_dat[0]
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
        # sort using regex splitting on element number
        err_param = sorted(misalignparams + fparams + dparams, key = lambda sub : int(re.split(r'\D+',sub)[-1]))
        return err_param

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

        filename = self.infile.split('.')[0] + '_ERR' + '.' + self.infile.split('.')[-1]
        # write out the lattice file 
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
                if error_param_names[ele][param][0] == 'd':
                    ele_param_dict[error_param_names[ele][param]] = [0, 0, 'gaussian', 3]
                else:
                    ele_param_dict[error_param_names[ele][param]] = [1, 0, 'gaussian', 3]
            setattr(ele_err_dict, element_names_yaml[ele], ele_param_dict)
        # create YAML tolerance template
        with open('GPTin_tolerance_temp.yml', 'w') as tempfile:
            yaml.dump(munch.unmunchify(ele_err_dict), tempfile, sort_keys=False)


# test space!
#if __name__ == "__main__":
    # class initialization 
#    GPTerr = GPT_error_mod('200fC.in')

#    GPTerr.lattice_replacer_template()

    # get element_names + numbers
    #names = [GPTerr.element_types()[0][i] + "-" + str(GPTerr.element_types()[1][i]) for i in range(len(GPTerr.element_types()[0]))]
    #print(names)

    # write lattice to file (currently just misalignments)
    #GPTerr.lattice_replacer() 

    #print(GPTerr.param_replacer('map1D_TM', 3, 1))
    #print(GPTerr.element_replace('map1D_TM', 3, 1))

   

