# -*- coding: utf-8 -*-
""""Fetch a list of pdb entries that use x-ray crystallography
    on proteins or proteins + nucleic acids."""
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import os

from ftplib import FTP
from os.path import isfile, basename
from pdb.lib.file_io import write_yaml


def fetch_xray(xray_fp, force_download=False):
    """Fetch list of pdb entries, process, and write results to a yaml file.

    List of all PDB entries, identification of each as a protein,
    nucleic acid, or protein-nucleic acid complex and whether
    the structure was determined by diffraction or NMR.

    Reference:
    http://www.rcsb.org/pdb/static.do?p=general_information/about_pdb/summaries.html

    Args:
        xray_fp (Unicode): The destination yaml file to be written.
        force_download (bool): If true, download the file even it
            the path already exists locally.

    Returns:
        None

    """
    # Manually unit tested.
    if isfile(xray_fp) and not force_download:
        print(
            "Found local copy of \"{}.\" Using file:\n\t{}".format(
                basename(xray_fp),
                xray_fp
            )
        )
        return None

    assert os.path.isabs(xray_fp)

    remote_directory = '/pub/pdb/derived_data/'
    remote_file = 'pdb_entry_type.txt'
    domain = 'ftp.wwpdb.org'

    ftp = FTP(domain)
    ftp.login()
    ftp.cwd(remote_directory)

    lines = []
    ftp.retrlines('RETR {}'.format(remote_file), lambda l: lines.append(l))

    xray = []
    for line in lines:
        columns = line.split()

        x_type = columns[2].strip()
        p_type = columns[1]
        pdb = columns[0]

        if p_type == 'prot' or p_type == 'prot-nuc':
            if x_type == 'diffraction':
                xray.append(pdb.upper())

    write_yaml(xray, xray_fp)
    assert isfile(xray_fp)
    return None
