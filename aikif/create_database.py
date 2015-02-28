# create_data_base.py
import sys, os
import datetime

if sys.version[0:1] != '3':
    print ("Python Version = " + sys.version)
    print('==== WARNING - use Python 3 ======')
    exit(1)

import aikif.dataTools.cls_datatable as mod_table
from aikif.dataTools.cls_sql_code_generator import SQLCodeGenerator
import aikif.config as cfg
fldr = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.sep + ".." + os.sep + 'data') 
build_all_file = fldr + os.sep + '_BUILD_ALL.SQL'

def main():
    f_all = open(build_all_file, 'w')
    f_all.write('/* ' + build_all_file + '\n')
    f_all.write('Auto generated by AIKIF create_database.py  ' + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + '\n')
    f_all.write('\n')
    f_all.write('Script to build the database for AIKIF\n')
    f_all.write('https://github.com/acutesoftware/AIKIF\n')
    f_all.write('*/\n\n')
    f_all.write('-- CREATE TABLES -- \n')
    print('Creating database script in ' + fldr)
    make_table(f_all, 'CORE_EVENTS', ['id', 'name', 'key', 'value'])
    make_table(f_all, 'CORE_OBJECTS', ['id', 'name', 'key', 'value'])
    make_table(f_all, 'CORE_LOCATIONS', ['id', 'name', 'key', 'value'])
    make_table(f_all, 'CORE_PEOPLE', ['id', 'name', 'key', 'value'])
    make_table(f_all, 'CORE_FACTS', ['id', 'name', 'key', 'value'])
    make_table(f_all, 'CORE_PROCESSES', ['id', 'name', 'key', 'value'])
    f_all.close()
    print('Done..')
    
def make_table(f_all, tbl, cols):
    tname = 'CREATE_' + tbl
    t = mod_table.DataTable(tbl, fldr + tbl + '.csv', cols)
    #t.save_csv(fldr + os.sep + tbl + '.csv')   

    # create the SQL of a file
    t = SQLCodeGenerator(tbl)
    t.set_column_list(cols)
    t.create_script_fact()
    t.create_index(tbl, cols)
    t.save_ddl(fldr + os.sep + tname + '.SQL')
    f_all.write('@' + tname + '.SQL;\n')

if __name__ == '__main__':
    main()        