# -*- coding: utf-8 -*-
"""Fetch pdb_chain_uniprot.tsv from ebi servers and write to file."""
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import os
import re
import gzip

from ftplib import FTP
from io import open
from os.path import isfile, basename


def _unzip_file(compressed_fp):
    assert os.path.isabs(compressed_fp)
    dir_path, compressed_fn = os.path.split(compressed_fp)
    tsv_fn = _uncompressed_name(compressed_fn)
    tsv_fp = os.path.join(dir_path, tsv_fn)

    with gzip.open(compressed_fp, 'rb') as ori_fh, \
            open(tsv_fp, 'wb') as new_fh:
        new_fh.write(ori_fh.read())
    assert isfile(tsv_fp)
    return None


def _uncompressed_name(compressed_fn):
    """Remove the trailing '.gz' from a file name."""
    assert not os.path.isabs(compressed_fn)
    uncompressed_fn = re.search(r'(.+?)(\.gz)', compressed_fn)
    if not uncompressed_fn:
        raise RuntimeError("Invalid file name.")
    return uncompressed_fn.group(1)


def fetch_pdb_chain_uniprot(chain_file_path, force_download=False):
    """Fetch pdb_chain_uniprot.tsv from ebi servers and write to file."""

    # Unit tested manually.
    if isfile(chain_file_path) and not force_download:
        print(
            "Found local copy of \"{}.\" Using file:\n\t{}".format(
                basename(chain_file_path),
                chain_file_path
            )
        )
        return None

    assert os.path.isabs(chain_file_path)
    dir_name, base_name = os.path.split(chain_file_path)
    compressed_fn = ''.join([base_name, '.gz'])
    compressed_fp = os.path.join(dir_name, compressed_fn)
    with open(compressed_fp, 'wb') as fh:
        ftp = FTP('ftp.ebi.ac.uk')
        ftp.login()
        ftp.cwd('/pub/databases/msd/sifts/flatfiles/tsv/')
        ftp.retrbinary(
            'RETR {}'.format(compressed_fn),
            lambda data: fh.write(data)
        )
    assert isfile(compressed_fp)
    _unzip_file(compressed_fp)

    return None
