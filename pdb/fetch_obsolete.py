# -*- coding: utf-8 -*-
"""Fetching and Parsing"""
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import requests
import xml.etree.ElementTree as ETree

from os.path import isfile, basename
from pdb.lib.file_io import write_yaml


def fetch_obsolete(
        obs_file_path,
        url='http://www.rcsb.org/pdb/rest/getObsolete',
        force_download=False
):
    """Fetch list of obsolete entries.

    Fetch list of obsolete entries, process, and write
    results to a yaml file.

    Args:
        obs_file_path (Unicode): The destination yaml file to be written.
        url (Unicode):  The url address of the data.
        force_download (bool): If true, download the file even it
            the path already exists locally.

    Returns:
        None

    """
    if isfile(obs_file_path) and not force_download:
        print(
            "Found local copy of \"{}.\" Using file:\n\t{}".format(
                basename(obs_file_path),
                obs_file_path
            )
        )
    else:
        obs = []
        obs_req = requests.get(url)
        root = ETree.fromstring(obs_req.text)
        for child in root:
            obs.append(child.attrib['structureId'].upper())
        obs_req.close()
        write_yaml(obs, obs_file_path)
    return None
