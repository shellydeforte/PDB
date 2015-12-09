# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import pandas as pd

from pdb.lib.pdb_tools import read_pdb_chain_uniprot_uniIDs
from pdb.lib.progress_bar import ProgressBar


def create_uni_struct(pdb_df):
    """ Creates a DataFrame that has UniProt ID and composite
    structure for UniProt.

    Args:
        pdb_df (DataFrame): A DataFrame produced by create_composite.

    Returns:
        df (DataFrame): A new DataFrame with UniProt ID and
        composite UniProt structure.

    """
    uni_struct = {'SP_PRIMARY': [], 'STRUCT': []}
    uni_list = read_pdb_chain_uniprot_uniIDs(pdb_df)
    progress = ProgressBar(
        len(uni_list),
        approx_percentage=1,
        start_msg="Creating DataFrame with ID and composite structure.",
        end_msg="Done creating DataFrame with ID and composite structure."
    )
    for uni in uni_list:
        pdbs = pdb_df[pdb_df.SP_PRIMARY == uni]
        struct_list = []
        assert len(pdbs.index) > 1
        for i, row in pdbs.iterrows():
            struct_list.append(row.SEC_STRUCT)
        assert len(struct_list) > 1
        for struct in struct_list:
            assert len(struct) > 0
            assert len(struct) == len(struct_list[0])
        assert len(struct_list) == len(pdbs.index)
        comp_struct = _uni_struct(struct_list)
        uni_struct['SP_PRIMARY'].append(uni)
        uni_struct['STRUCT'].append(comp_struct)
        progress.inc()

    df = pd.DataFrame(uni_struct)
    return df


def _uni_struct(struct_list):
    """Create composite UniProt structure.

    Given a list of pdb secondary structures, create a composite UniProt
    structure of the form '----OOOOXXXOOOO...'

    This will validate that all the structure strings are the same length
    before proceeding. It returns 'None' if the structure list is empty.

    Args:
        struct_list (list of strings): This is a list of all the associated
            PDB secondary structure strings associated with a single
            UniProt ID (i.e., ['---XXHHH', 'XXXHHHHH', 'PPPHHIIP'])

    Returns:
        comp_struct (string): Of the form 'XXXXXOOOO'.
        None: If the len(struct_list) == 0.

    """
    comp_struct = ''
    for i in range(len(struct_list[0])):
        one_pos_struct = []
        for j in range(len(struct_list)):
            one_pos_struct.append(struct_list[j][i])
        comp_struct += _eval_one_pos_struct(one_pos_struct)
    return comp_struct


def _eval_one_pos_struct(one_pos_struct):
    """ Evaluates the UniProt structure for one column position.

    Returns the correct designation based on this list.
    If There are any 'X', then it is 'X'.
    If it is all '-', then '-'.
    If there are no 'X', and is not all '-', then 'O'.

    Args:
        one_pos_struct (list): Of the form ['X', 'X', 'P', 'H', '-', ...]

    Returns:
        A single letter, either 'X', '-' or 'O'.

    """
    if 'X' in one_pos_struct:
        return 'X'
    elif ''.join(set(one_pos_struct)) == '-':
        return '-'
    else:
        return 'O'
