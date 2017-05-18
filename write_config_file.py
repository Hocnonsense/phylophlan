#!/usr/bin/env python3


import configparser as cp


config = cp.ConfigParser()
config_folder_files = 'configs/'

# AVAILABLE OPTIONS:
# program_name: name of the executable to use
# program_name_parallel: name of the parallel (or multi-core) version of the executable
# params: params to use
# threads: specify the option to use to pass the number of threads
# input: specify the option to use for the input file
# database: specify the option to use for setting the database
# output_path: specify the to option to use to set the path of the folder that will contains the output file
# output: specify the option to use for the output file
# version: specify the option to use to get the version of the sotware, used to verify the software installation
# command_line: specify the command line to generate with the position of each argument

progs = {
    # 'db_dna': {'program_name': 'makeblastdb',
    #            'params': '-dbtype prot',
    #            'input': '-in',
    #            'output': '-out',
    #            'version': '-version',
    #            'command_line': '#program_name# #params# #input# #output#'},
    'db_aa': {'program_name': 'usearch9.2.64_i86linux32',
                   'params': '-quiet',
                   'input': '-makeudb_ublast',
                   'output': '-output',
                   'version': '-version',
                   'command_line': '#program_name# #params# #input# #output#'},
    'map_dna': {'program_name': 'tblastn',
                'params': '-outfmt "6 saccver qaccver pident length mismatch gapopen sstart send qstart qend evalue bitscore" -evalue 1e-50',
                'input': '-subject',
                'database': '-query',
                'output': '-out',
                'version': '-version',
                'command_line': '#program_name# #params# #input# #database# #output#'},
    # 'map_dna': {'program_name': 'blastx',
    #             'params': '-outfmt 6 -evalue 1e-30',
    #             'input': '-query',
    #             'database': '-subject',
    #             'output': '-out',
    #             'version': '-version',
    #             'command_line': '#program_name# #params# #input# #database# #output#'},
    'map_aa': {'program_name': 'usearch9.2.64_i86linux32',
               'params': '-quiet -evalue 1e-10 -maxaccepts 8 -maxrejects 32',
               'threads': '-threads',
               'input': '-ublast',
               'database': '-db',
               'output': '-blast6out',
               'version': '-version',
               'command_line': '#program_name# #params# #threads# #input# #database# #output#'},
    'msa': {'program_name': 'muscle3.8.1551',
            'params': '-quiet -maxiters 2',
            'input': '-in',
            'output': '-out',
            'version': '-version',
            'command_line': '#program_name# #params# #input# #output#'},
           # {'program_name': 'mafft', 'params': '--anysymbol --quiet', 'version': '--version'},
    'trim': {'program_name': 'trimal',
             'params': '-gappyout',
             'input': '-in',
             'output': '-out',
             'version': '--version',
             'command_line': '#program_name# #params# #input# #output#'},
    'gene_tree1': {'program_name': 'FastTree-2.1.9-SSE3',
                   'program_name_parallel': 'FastTreeMP-2.1.9-SSE3',
                   'params': '-quiet -mlacc 2 -slownni -spr 4 -fastest -mlnni 4 -no2nd',
                   'output': '-out',
                   'command_line': '#program_name# #params# #output# #input#'},
    # 'gene_tree2': {'program_name': 'raxmlHPC',
    #                'params': '-m ',
    #                'database': '-t', # starting tree
    #                'input': '-s',
    #                'output_path':'-w',
    #                'output': '-n',
    #                'version': '-v',
    #                'command_line': '#program_name# #params# #output_path# #input# #output#'}
    'tree1': {'program_name': '/CM/tools/astral-4.10.12/astral.4.10.12.jar',
              'params': 'java -jar',
              'input': '-i',
              'output': '-o',
              'version': '--help',
              'command_line': '#params# #program_name# #input# #output#'},
    # 'tree1': {'program_name_parallel': 'FastTreeMP-2.1.9-SSE3',
    #           'params': '-quiet -mlacc 2 -slownni -spr 4 -fastest -mlnni 4 -no2nd',
    #           'output': '-out',
    #           'command_line': '#program_name_parallel# #params# #output# #input#'},
    # 'tree2': {'program_name_parallel': 'raxmlHPC-PTHREADS-SSE3',
    #           'params': '-m ',
    #           'threads': '-T'
    #           'database': '-t', # starting tree
    #           'input': '-s',
    #           'output_path':'-w',
    #           'output': '-n',
    #           'version': '-v',
    #           'command_line': '#program_name_parallel# #params# #threads# #database# #output_path# #input# #output#'}
}

for prog, options in progs.items():
    config[prog] = {}

    for option, value in options.items():
        config[prog][option] = value

with open(config_folder_files+'supertree.cfg', 'w') as f:
    config.write(f)
