#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 * @Date: 2020-11-18 21:28:28
 * @LastEditors: Hwrn
 * @LastEditTime: 2020-11-25 21:02:55
 * @FilePath: /phylophlan/phylophlan/utils.py
 * @Description:
"""


__author__ = ('Francesco Asnicar (f.asnicar@unitn.it), '
              'Francesco Beghini (francesco.beghini@unitn.it), '
              'Mattia Bolzan (mattia.bolzan@unitn.it), '
              'Nicola Segata (nicola.segata@unitn.it) '
              'contributer (hwrn.aou@sjtu.edu.cn)'
              )
__version__ = '3.0.1'
__date__ = '18 Nov 2020'


import argparse as ap
import os
import sys
import time
from functools import wraps
from typing import Callable
from urllib.request import urlretrieve


DATABASES_FOLDER = 'phylophlan_databases/'
SUBMAT_FOLDER = 'phylophlan_substitution_matrices/'
SUBMOD_FOLDER = 'phylophlan_substitution_models/'
CONFIGS_FOLDER = 'phylophlan_configs/'
OUTPUT_FOLDER = ''


def read_params(p: ap.ArgumentParser):
    p = ap.ArgumentParser(description=(""),
                          formatter_class=ap.ArgumentDefaultsHelpFormatter)

    p.add_argument('--databases_folder', type=str, default=DATABASES_FOLDER,
                   help="Path to the folder containing the database files")
    p.add_argument('--output_folder', type=str, default=OUTPUT_FOLDER,
                   help="Path to the output folder where to save the results")

    p.add_argument('-o', '--output', type=str, default=None,
                   help=("Output folder name, otherwise it will be the name of the input folder concatenated with the name of "
                         "the database used"))
    p.add_argument('-f', '--config_file', type=str, default=None,
                   help=('The configuration file to use. Four ready-to-use configuration files can be generated using the '
                         '"phylophlan_write_default_configs.sh" script'))
    p.add_argument('--clean_all', action='store_true', default=False,
                   help="Remove all installation and database files automatically generated")
    p.add_argument('--nproc', type=int, default=1,
                   help="The number of cores to use")

    p.add_argument('--update', action='store_true',
                   default=False, help="Update the databases file")
    p.add_argument('--citation', action='version',
                   version=('Asnicar, F., Thomas, A.M., Beghini, F. et al. '
                            'Precise phylogenetic analysis of microbial isolates and genomes from metagenomes using PhyloPhlAn 3.0. '
                            'Nat Commun 11, 2500 (2020). '
                            'https://doi.org/10.1038/s41467-020-16366-7'),
                   help="Show citation")
    p.add_argument('--verbose', action='store_true',
                   default=False, help="Makes PhyloPhlAn verbose")
    p.add_argument('-v', '--version', action='version', version='PhyloPhlAn version {} ({})'.format(__version__, __date__),
                   help="Prints the current PhyloPhlAn version and exit")

    return p.parse_args()


def info(s, init_new_line=False, exit=False, exit_value=0):
    if init_new_line:
        sys.stdout.write('\n')

    sys.stdout.write('{}'.format(s))
    sys.stdout.flush()

    if exit:
        sys.exit(exit_value)


def error(s, init_new_line=False, exit=False, exit_value=1):
    if init_new_line:
        sys.stderr.write('\n')

    sys.stderr.write('[e] {}\n'.format(s))
    sys.stderr.flush()

    if exit:
        sys.exit(exit_value)


class ReportHook():

    def __init__(self):
        self.start_time = time.time()

    def report(self, blocknum, block_size, total_size):
        """
        Print download progress message
        """

        if blocknum == 0:
            self.start_time = time.time()

            if total_size > 0:
                info("Downloading file of size: {:.2f} MB\n".format(
                    self.byte_to_megabyte(total_size)))
        else:
            total_downloaded = blocknum * block_size
            status = "{:3.2f} MB ".format(self.byte_to_megabyte(total_downloaded))

            if total_size > 0:
                percent_downloaded = total_downloaded * 100.0 / total_size
                # use carriage return plus sys.stderr to overwrite stderr
                download_rate = total_downloaded / \
                    (time.time() - self.start_time)
                estimated_time = (
                    total_size - total_downloaded) / download_rate
                estimated_minutes = int(estimated_time / 60.0)
                estimated_seconds = estimated_time - estimated_minutes * 60.0
                status += ("{:3.2f} %  {:5.2f} MB/sec {:2.0f} min {:2.0f} sec "
                           .format(percent_downloaded, self.byte_to_megabyte(download_rate),
                                   estimated_minutes, estimated_seconds))

            status += "        \r"
            info(status)

    def byte_to_megabyte(self, byte):
        """
        Convert byte value to megabyte
        """

        return (byte / 1048576)


def download(url, download_file, overwrite=False, verbose=False):
    """
    Download a file from a url
    """

    if (not os.path.isfile(download_file)) or overwrite:
        try:
            if verbose:
                info('Downloading "{}" to "{}"\n'.format(url, download_file))

            urlretrieve(url, download_file, reporthook=ReportHook().report)
            info('\n')
        except EnvironmentError:
            error('unable to download "{}"'.format(url), exit=True)
    elif verbose:
        info('File "{}" present\n'.format(download_file))


class clock:
    def __init__(self, _exit=False) -> None:
        self.start = None
        self.exit = _exit

    def __call__(self, func: Callable):
        """
        * @description: It is studpid, be careful when using this feature.
        * @param {*} self
        * @param {Callable} func
        * @return {*}
        """
        @wraps(func)
        def wrappedFunction(*args, **kwargs):
            with self:
                _ = func(*args, **kwargs)
            return _
        return wrappedFunction

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        end = time.time()
        info('Total elapsed time {}s\n'.format(int(end - self.start)),
             init_new_line=True)
        if self.exit:
            sys.exit(0)
