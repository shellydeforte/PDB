# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals)
import pandas as pd
from io import open
from Bio import SeqIO
from pdb.lib.data_paths import build_abs_path
from pdb.lib.progress_bar import ProgressBar


def create_pdb_composite(df, ss_dis, uni_folder):
    """ Creates a secondary structure composite and outputs a new DataFrame.

    1. Goes through the DataFrame row by row, and creates interval_dict.
    2. Uses this dictionary to create a composite structure.
    3. Creates a new dataframe with PDB_CHAIN, UNIPROT, SEC_STRUCT.

    Notes:
        Multiple UniProt IDs can be attached to a single PDB_CHAIN.
        Therefore, the only unique key for a given ss sequence is
        the PDB ID, the PDB chain and the UniProt ID. That's why
        the dictionary is keyed with pdb_chain_uni.

    Args:
        df (DataFrame): A pre-filtered dataframe from pdb_chain_uniprot.tsv.
        ss_dis (dictionary): A dictionary extracted from ss_dis.txt.
            ss_dis has the following form:
                ss_dis[pdb_A] = {
                    'sequence': '',
                    'secstr': '',
                    'disorder': ''
                }
        uni_folder (Unicode): a directory path to the folder that has single
        UniProt fasta files.

    Returns:
        A new DataFrame with PDB_CHAIN, UNIPROT, SEC_STRUCT.

    """
    interval_dict = _create_interval_dict(df)
    structure_dict = _create_struct_dict(interval_dict, ss_dis, uni_folder)
    df = pd.DataFrame(structure_dict)
    return df


def _create_interval_dict(df):
    """Create a dictionary of intervals.

    The first interval corresponds with RES_BEG, RES_END, which are the
    indexes (starting from 1) for the PDB chain. Note that this is
    required because the PDB chain is not always fully composed of the
    UniProt entry. The second interval corresponds to SP_BEG, SP_END,
    this is the corresponding interval on the full UniProt entry,
    starting with an index of 1.

    Args:
        df (DataFrame): A pre-filtered dataframe from pdb_chain_uniprot.tsv.

    Returns:
        interval_dict (dictionary): A dictionary in the following form:
            {
                    '11BG_A_Q3E840':
                        [
                            [
                                [1, 124],
                                [27, 150]
                            ]
                        ]
                }

    """
    interval_dict = {}
    progress = ProgressBar(
        len(df.index),
        start_msg="Creating interval dictionary..",
        end_msg="Done creating interval dictionary."
    )
    for i, row in df.iterrows():
        uni_id = row.SP_PRIMARY
        pdb_chain_uni = ''.join([
            row.PDB,
            '_',
            row.CHAIN,
            '_',
            uni_id
        ])
        intervals = [[row.RES_BEG, row.RES_END], [row.SP_BEG, row.SP_END]]
        if pdb_chain_uni in interval_dict.keys():
            interval_dict[pdb_chain_uni].append(intervals)
        else:
            interval_dict[pdb_chain_uni] = [intervals]
        progress.inc()
    return interval_dict


def _create_struct_dict(interval_dict, ss_dis, uni_folder):
    """ Creates the structure dictionary.

    Args:
        interval_dict (dict): A dictionary in the following form:
                {
                        '11BG_A_Q3E840':
                            [
                                [
                                    [1, 124],
                                    [27, 150]
                                ]
                            ]
                    }
        uni_folder (Unicode): A path to the folder that has single
            UniProt fasta files.
        ss_dis: a dictionary extracted from ss_dis.txt, in the following form:
            ss_dis[pdb_A] = {
                'sequence': '',
                'secstr': '',
                'disorder': ''
            }

    Returns:
        A dictionary in the following form:
        {
            'PDB_CHAIN': [],
            'UNIPROT': [],
            'SEC_STRUCT': []
        }

    """
    structure_dict = {'PDB_CHAIN': [], 'SP_PRIMARY': [], 'SEC_STRUCT': []}
    for pdb_chain_uni in interval_dict:
        pdb_chain = ''.join([
            pdb_chain_uni.split('_')[0],
            '_',
            pdb_chain_uni.split('_')[1]
        ])
        uni_id = pdb_chain_uni.split('_')[2]

        uni_fp = build_abs_path(uni_folder, uni_id)
        len_uni_seq = len(
            (SeqIO.read(open(uni_fp), "fasta")).seq
        )

        disorder = ss_dis[pdb_chain]['disorder']
        ss = ss_dis[pdb_chain]['secstr']
        intervals = interval_dict[pdb_chain_uni]
        pdb_struct = _create_pdb_struct(intervals, disorder, ss, len_uni_seq)

        structure_dict['PDB_CHAIN'].append(pdb_chain)
        structure_dict['SP_PRIMARY'].append(uni_id)
        structure_dict['SEC_STRUCT'].append(pdb_struct)
    return structure_dict


def _create_pdb_struct(intervals, disorder, ss, uni_seq_len):
    """Create PDB structure.

    1. Creates a sequence that is all '-'.
    2. Iterate through the PDB indexes, add the distance between the
        PDB interval and the UniProt interval to get the UniProt index.
    3. If there is a ss, substitutes that value. If there is a disorder
        value ('X'), substitutes that value. If neither is present,
        substitutes a 'P'.

    Example:
        Given the follow arguments (these don't go together):
            disorder = 'XX----------------------'
            ss = '     TT  EE   SS HHHHHHHHHHHT  TEEEEEEEE  SGGG    '
            intervals = [[[3, 197], [296, 490]], [[200, 367], [765, 932]]]
            uni_seq_len = 963

        Something like this is created:
            [-,-,-,-,'P','P','X','E','E','H','H','H'...]

        And something like this is returned:
            '---PPXEEHH'
        The return string is the same length as the Uniprot sequence.

    Args:
        intervals (list): A list of interval information. (Interval
            numbering starts at 1, so must be adjusted down 1.)
        disorder (Unicode): The missing regions from ss_dis.
        ss (Unicode): The secondary structure from ss_dis.
        uni_seq_len (int): The length of the UniProt sequence.

    Returns:
        A string that represents the secondary structure elements.

    """
    def interval_map(x):
        return x + (interval[1][0] - interval[0][0])
    structure = ['-'] * uni_seq_len
    for interval in intervals:
        for i in range(interval[0][0] - 1, interval[0][1]):
            j = interval_map(i)
            if ss[i] != ' ':
                structure[j] = ss[i]
            if disorder[i] != '-':
                structure[j] = disorder[i]
            if structure[j] == '-':
                structure[j] = 'P'
    assert len(structure) == uni_seq_len
    assert ' ' not in structure
    return ''.join(structure)
