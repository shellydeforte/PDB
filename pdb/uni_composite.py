# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import os
import re
from os.path import isfile

import pandas as pd

from pdb.lib.create_delimiter import create_delimiter
from pdb.lib.create_pdb_intervals import create_intervals
from pdb.lib.data_paths import ProjectFolders
from pdb.lib.datetime_info import now_utc
from pdb.lib.file_io import write_yaml, read_json
from pdb.lib.pdb_tools import uni_pdb_validation
from pdb.lib.uni_tools import create_uni_struct


def _create_composite_file_names():
    file_names = {}
    names = [
        ('tsv_file', '.tsv'),
        ('yaml_file', '.yaml'),
        ('json_file', '.json')
    ]

    time_stamp = now_utc()
    time_stamped_base = ''.join([
        'uni_composite.',
        time_stamp
    ])

    for name, ext in names:
        file_names[name] = ''.join([
            time_stamped_base,
            ext
            ])

    return file_names


def _create_composite_file_paths(dir_path, file_names):
    """

    Args:
        dir_path (Unicode):
        file_names (dict):
    """
    file_paths = {}

    for name in file_names:
        file_paths[name] = os.path.join(
            dir_path,
            file_names[name]
        )

    return file_paths


def _get_local_file_names(directory):
    local_file_names = [
        name
        for name in os.listdir(directory)
        if isfile(os.path.join(directory, name))
        ]
    return local_file_names


def _compile_uni_composite_regex():
    uniprot_composite_expression = """
        (                      # Start Group 1
        uni_composite          # Base name
        \.                     # Literal period.

        (?:                    # Optional non-capturing group.
        \d{8,}                 # Date
        T                      # "T" (indicate time)
        \d{6,}                 # Time
        Z                      # "Z" (indicate GMT)
        )?

        )                      # End Group 1

        \.?                    # Optional period.

        (tsv)                  # Group 3: "tsv" extension

    """
    uniprot_composite_pat = re.compile(
        uniprot_composite_expression, re.VERBOSE)
    return uniprot_composite_pat


def _uni_composite_file_exists(directory):
    valid = _compile_uni_composite_regex()
    file_exists = False
    existing_files = _get_local_file_names(directory)
    for existing in existing_files:
        if valid.search(existing):
            file_exists = True
            break
    return file_exists


def uniprot_composite(dirs):
    """Creates final UniProt DataFrame.

    Create final UniProt DataFrame where the
    UniProt ID provides a unique key.

    Args:
        dirs (ProjectFolders): A named tuple of directory paths.

    """
    pdb_initial_composite_fp = os.path.join(
        dirs.tsv_data,
        'pdb_initial_composite_df.tsv'
    )
    assert os.path.isfile(pdb_initial_composite_fp)

    uni_folder_path = dirs.uni_data
    file_names = _create_composite_file_names()
    paths = _create_composite_file_paths(uni_folder_path, file_names)

    uni_composite_tsv = paths['tsv_file']
    uni_composite_yaml = paths['yaml_file']
    uni_composite_json = paths['json_file']

    if _uni_composite_file_exists(uni_folder_path):
        print(
            "A final uni_composite file already exists. Composite "
            "function complete. (Note: remove existing uni_composite "
            "files in the \"{}\" directory to have them "
            "regenerated.".format(uni_folder_path)
        )
        return None

    pdb_df = pd.read_csv(
        pdb_initial_composite_fp,
        sep='\t',
        header=0,
        encoding='utf-8',
        keep_default_na=False,
        na_values=['NULL', 'N/A'])

    print("Creating the UniProt composite structure.")
    uni_df = create_uni_struct(pdb_df)
    print("Done creating UniProt composite structure.")

    print("Validating UniProt composite structure.")
    uni_pdb_validation(uni_df, pdb_df)
    print("Validation complete.")

    print("Assigning missing region designations.")
    uni_df = create_intervals(pdb_df, uni_df)
    print("Done assigning missing regions.")

    assert isinstance(uni_df, pd.DataFrame)
    delimiter = create_delimiter('\t')
    uni_df.to_csv(uni_composite_tsv, sep=delimiter, encoding='utf-8')
    uni_df.to_json(uni_composite_json, force_ascii=False)

    json_data = read_json(uni_composite_json)
    write_yaml(json_data, uni_composite_yaml)

    print("Done writing UniProt composite files:")
    print("\t{}".format(uni_composite_tsv))
    print("\t{}".format(uni_composite_yaml))
    print("\t{}".format(uni_composite_json))
    print("This is the final UniProt ID DataFrame.")

    return None
