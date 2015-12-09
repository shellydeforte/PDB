# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import os
from logging import getLogger
from os.path import basename
from sys import version_info

import pandas as pd

from pdb.fetch_ss_dis import fetch_ss_dis
from pdb.lib.create_delimiter import create_delimiter
from pdb.lib.file_io import read_yaml
from pdb.lib.pdb_tools import filter_single
from pdb.lib.progress_bar import ProgressBar

PYTHON2 = version_info[0] == 2


def initial_filtering(dirs):
    """Creates a dataframe from pdb_chain_uniprot.tsv.

    Perform initial filtering with pdb_chain_uniprot.tsv
    and supplementary files.

    Supplementary file processing steps:
        1. Removes the PDB_BEG, PDB_END columns.
        2. Converts all PDB IDs to upper case.
        3. Removes any rows where the PDB ID isn't in the xray list.
        4. Removes any rows where the PDB ID is in the obs list.
        5. Removes any rows where the RES_BEG or SP_BEG are < 1.
        6. Removes any rows where the length of the intervals doesn't match.
        7. Removes any rows where the length of the interval is <= 3.
        8. Removes any rows for pdb_chains not in ss_dis.
        9. Removes uniIDs with < 2 pdb chains.
        10. Adds a column called 'PDB_SEQ' that has the section of the PDB
            chain corresponding to the interval in RES_BEG:RES_END.

    Args:
        dirs (ProjectFolders): A named tuple of directory paths.

    Returns:
        None

    """
    # Return used_local for unittest because of problems capturing stdout
    # with logging instance.
    used_local = False
    pdb_seq_fp = os.path.join(dirs.working, 'pdb_seq.tsv')
    msg = getLogger('root')

    if not os.path.exists(pdb_seq_fp):
        obs_fp = os.path.join(dirs.working, 'obs.yaml')
        xray_fp = os.path.join(dirs.working, 'xray.yaml')
        chain_fp = os.path.join(dirs.tsv_data, 'pdb_chain_uniprot.tsv')

        msg.info('START: Initial filtering.')

        msg.debug("START: Fetch ss_dis.tsv.")
        ss_dis = fetch_ss_dis(dirs.working)
        msg.debug("COMPLETE: Fetch ss_dis.tsv.")

        msg.debug("START: Read obs.yaml.")
        obs = read_yaml(obs_fp)
        msg.debug("COMPLETE: Read obs.yaml.")

        msg.debug("START: Read xray.yaml.")
        xray = read_yaml(xray_fp)
        msg.debug("COMPLETE: Read xray.yaml.")

        msg.debug("START: Create initial DataFrame.")
        df = pd.read_csv(
            chain_fp,
            sep='\t',
            header=1,
            encoding='utf-8',
            keep_default_na=False,
            na_values=['NULL', 'N/A'])
        msg.debug("COMPLETE: Create initial DataFrame.")
        msg.debug("Initial DataFrame has {} rows.".format(len(df.index)))

        msg.debug("START: Remove rows where "
                  "the PDB ID is not in the xray list.")
        df = filter_pdb_chain_uniprot(df, obs, xray)
        msg.debug("COMPLETE: Remove rows where "
                  "the PDB ID is not in the xray list.")
        msg.debug("DataFrame now has {} rows.".format(len(df.index)))

        msg.debug("START: Remove entries not in ss_dis "
                  "and add the PDB peptide.")
        df = add_pdbseq_to_df(df, ss_dis)
        msg.debug("COMPLETE: Remove entries not in ss_dis "
                  "and add the PDB peptide.")
        msg.debug("DataFrame now has {} rows.".format(len(df.index)))

        msg.debug("START: Remove UniProt IDs with < 2 pdb chains.")
        df = filter_single(df)
        msg.debug("COMPLETE: Remove UniProt IDs with < 2 pdb chains.")
        msg.debug("DataFrame now has {} rows.".format(len(df.index)))

        msg.debug("START: Writing DataFrame to TSV file.")
        delimiter = create_delimiter('\t')
        df.to_csv(pdb_seq_fp, sep=delimiter, encoding='utf-8')
        msg.debug("COMPLETE: Writing DataFrame to TSV file.")
        msg.info(
            "Wrote {} to:\n\t{}".format(basename(pdb_seq_fp), pdb_seq_fp)
        )
        msg.info('COMPLETE: Initial filtering.')

    else:
        used_local = True
        msg.info(
            "Found and using local {filename}: \n"
            "\t{filepath}".format(
                filename=basename(pdb_seq_fp),
                filepath=pdb_seq_fp
            )
        )
        msg.info('COMPLETE: Initial filtering.')

    return used_local


def filter_pdb_chain_uniprot(df, obs, xray):
    """Step 1 filtering of the DataFrame from pdb_chain_uniprot.tsv.

    Removes the PDB_BEG, PDB_END columns.
    Converts all PDB IDs to upper case.
    Removes any rows where the PDB ID isn't in the xray list.
    Removes any rows where the PDB ID is in the obs list.
    Removes any rows where the RES_BEG or SP_BEG are < 0.
    Removes any rows where the length of the intervals doesn't match.
    Removes any rows where the length of the interval is <= 3.

    Args:
        df (DataFrame): A pandas DataFrame read from pdb_chain_uniprot.tsv.
        obs (list of Unicode): A list of PDB IDs that are obsolete entries.
        xray (list of Unicode): A list of PDB IDs that are xray entries.

    Returns:
        A filtered DataFrame

    """
    df.drop('PDB_BEG', axis=1, inplace=True)
    df.drop('PDB_END', axis=1, inplace=True)
    df.PDB = df.PDB.str.upper()
    df = df[df.PDB.isin(xray)]
    df = df[-df.PDB.isin(obs)]
    df = df[(df.RES_BEG > 0) & (df.SP_BEG > 0)]
    df = df[(df.RES_END-df.RES_BEG) == (df.SP_END-df.SP_BEG)]
    df = df[(df.RES_END-df.RES_BEG) > 3]
    df = filter_single(df)
    return df


def add_pdbseq_to_df(df, ss_dis):
    """ Removes rows not in ss_dis, adds a column with PDB peptide sequence.

    Removes any rows for pdb_chains not in ss_dis.
    Adds a column called 'PDB_SEQ' that has the section of the PDB
    chain corresponding to the interval in RES_BEG:RES_END.

    Notes:
        Download Uniprot files after this step.

        RES_BEG, RES_END start with a numbering of 1.

        This function adds the a section of the PDB sequence to the
        DataFrame. This is later removed after comparison. My reasoning
        for adding this now was that I have to go through and remove
        rows anyways, so I already have the PDB sequence data available
        at this point, and it makes the next step quicker.

    Args:
        df (DataFrame): A pre-filtered DataFrame from pdb_chain_uniprot.tsv.
        ss_dis (dictionary): A dictionary extracted from ss_dis.txt.
        ss_dis has the following form:
            ss_dis[pdb_A] = {
                'sequence': '',
                'secstr': '',
                'disorder': ''
            }
    Returns:
        A filtered DataFrame with an added column.

    """
    log_pdb = getLogger('pdb_app_logger')
    log_root = getLogger('root')
    df['PDB_SEQ'] = ''
    progress = ProgressBar(
        len(df.index),
        start_msg="Removing rows for pdb_chains not in ss_dis.",
        end_msg="Done removing rows for pdb_chains not in ss_dis.."
    )
    log_root.info("Adding PDB_SEQ can take quite a while.")
    for i, row in df.iterrows():
        try:
            id_chain = ''.join([
                row.PDB,
                '_',
                row.CHAIN
            ])
        except TypeError as append_err:
            log_root.warning(
                "Error appending row. Error was:\n"
                "\t{}\n"
                "\trow.PDB was: [{}] {}\n"
                "\trow.CHAIN was: [{}]{}".format(
                    append_err.args,
                    type(row.PDB),
                    row.PDB,
                    type(row.CHAIN),
                    row.CHAIN
                )
            )
        if id_chain in ss_dis.keys():
            peptide = ss_dis[id_chain]['sequence'][row.RES_BEG-1:row.RES_END]
            df.set_value(i, 'PDB_SEQ', peptide)
        else:
            try:
                df.drop(i, inplace=True)
            except MemoryError as mem_err:
                log_pdb.error(
                    "Memory error while adding PDB peptide "
                    "sequence to DataFrame:\n"
                    "\t{}\n"
                    "\t{}\n"
                    "\t{}\n".format(
                        mem_err.args[0],
                        mem_err.args[1],
                        mem_err.args[2]
                    )
                )
                from struct import calcsize
                int_struct_size = calcsize("P") * 8
                if int_struct_size == 32:
                    log_root.warning(
                        "It appears you're on a 32-bit system and/or "
                        "using a 32-bit version of Python. You may need "
                        "to use a 64-bit version to avoid memory "
                        "errors for these large calculations."
                    )
        progress.inc()
    return df
