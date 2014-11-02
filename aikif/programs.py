# program.py	written by Duncan Murray 18/4/2014
# part of AIKIF
# standard set of programs used for each interface in ccd
# each having the same functions (at this stage for proof
# of concept) which allow you to call things as a normal
# command

import os
import cls_log as mod_log
import config as mod_cfg
import cls_file_mapping as mod_filemap 
import aikif.lib.cls_filelist as mod_fl
import aikif.lib.cls_file as mod_file

root_folder = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.sep  ) 


def TEST():
    """
    local test function - see \tests\test_programs.py for full coverage
    """
    prg = Programs('AIKIF Programs', root_folder)
    prg.list_all_python_programs()
    print(prg)

class Programs(object):
    """
    Class to manage a list of programs for AIKIF
    """
    def __init__(self, name, fldr):
        self.name = name
        self.fldr = fldr
        self.lstPrograms = [] 
        self.log_folder = mod_cfg.fldrs['log_folder']    
        self.lg = mod_log.Log(self.log_folder)
        self.lg.record_command('program', 'generating program list in - ' + self.log_folder)
        self.list_all_python_programs()
        
    def __str__(self):
        """
        return a summary of programs
        """
        return 'list of programs in AIKIF'
        
    
    def list_all_python_programs(self):
        """
        collects a filelist of all .py programs
        """
        self.tot_lines = 0
        self.tot_bytes = 0
        self.tot_files = 0
        self.tot_loc = 0
        fl = mod_fl.FileList([self.fldr], ['*.py'], ["__pycache__", ".git"])
        for file in fl.get_list():
            self.add(file, 'TODO - add comment')
            f = mod_file.TextFile(file)
            self.tot_lines += f.count_lines_in_file()
            self.tot_loc += f.count_lines_of_code()
            self.tot_bytes += f.size
            self.tot_files += 1
 
        print('All Python Program Statistics')
        print('Files = ', self.tot_files, ' Bytes = ', self.tot_bytes, ' Lines = ', self.tot_lines, ' Lines of Code = ', self.tot_loc)
            
        self.save('all_programs.csv')

        
        
    def add(self, nme, desc):
        """
        Adds a program to the list, with default desc
        """
        self.lstPrograms.append([nme,desc])
        #self.lg.record_process('program - generating program list in - ' + self.log_folder)

    def comment(self, nme, desc):
        """
        Adds a comment to the existing program in the list, 
        logs the reference and TODO - adds core link to processes
        """
        
        if nme != '':
            program_exists = False
            for i in self.lstPrograms:
                print(i)
                if nme in i[0]:
                    i[1] = desc
                    #print(nme, i)
                    program_exists = True
            
            if program_exists == False: # not there?
                self.lstPrograms.append([nme,desc + ' - FILE DOESNT EXIST'])
            
            self.lg.record_process('adding description to - ' + nme)


        
    def list(self):
        """
        Display the list of items 
        """
        for i in self.lstPrograms:
            print (i)
        return self.lstPrograms
        
    def save(self, fname=''):
        """
        Save the list of items to AIKIF core and optionally to local file fname
        """
        if fname != '':
            with open(fname, 'w') as f:
                for i in self.lstPrograms:
                    f.write(i[0] + ',' + i[1] + '\n')

        
        # save to standard AIKIF structure
        filemap = mod_filemap.FileMap(mod_filemap.dataPath)
        location_fileList = filemap.get_full_filename(filemap.find_type('LOCATION'), filemap.find_ontology('FILE-PROGRAM')[0])   	
        object_fileList = filemap.get_full_filename(filemap.find_type('OBJECT'), filemap.find_ontology('FILE-PROGRAM')[0])   	
        print('object_fileList = ' + object_fileList + '\n')
        os.remove(object_fileList)
        self.lstPrograms.sort()
        
        with open(object_fileList, 'a') as f:
            f.write('\n'.join([i[0] for i in self.lstPrograms]))

    def collect_program_info(self, fname):
        """
        gets details on the program, size, date, list of functions
        and produces a Markdown file for documentation
        """
        md = '#AIKIF Technical details\n'
        md += 'Autogenerated list of programs with comments and progress\n'
        md += '\nFilename | Size | Comment\n'
        md += '--- | --- | ---\n'
        for i in self.lstPrograms:
            f = mod_file.File(i[0])
            md += f.name + ' | ' + str(f.size) + ' | ' + i[1] + '\n'
        
        
        # save the details an Markdown file 
        with open(fname, 'w') as f:
            f.write(md)
 
if __name__ == '__main__': 
    TEST()