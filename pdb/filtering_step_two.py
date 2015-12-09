# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import os
import pandas as pd

from Bio import SeqIO
from io import open
from logging import getLogger

from pdb.lib.create_delimiter import create_delimiter
from pdb.lib.data_paths import ProjectFolders, build_abs_path
from pdb.lib.progress_bar import ProgressBar


def second_filtering(dirs):
    """Compare FASTA with PDB_SEQ and remove rows that aren't matches.

    Open a UniProt fasta file for each line and compare with PDB_SEQ.
    Removes rows if the PDB sequence section is not 100% match with the
    corresponding UniProt section.

    Args:
        dirs (ProjectFolders): A named tuple of directory paths.

    Returns:
        None

    """
    msg = getLogger('root')
    msg.info('START: Second filtering.')
    uni_filtered_name = 'pdb_seq_uni_filtered.tsv'
    uni_filtered_path = os.path.join(
        dirs.working,
        uni_filtered_name
    )
    delimiter = create_delimiter('\t')
    if not os.path.exists(uni_filtered_path):
        pdb_seq_path = os.path.join(dirs.working, 'pdb_seq.tsv')
        df = pd.read_csv(
            pdb_seq_path,
            sep=delimiter,
            index_col=0,
            keep_default_na=False,
            na_values=['NULL', 'N/A'])

        print(
            "Comparing the PDB peptide to the corresponding "
            "section of the UniProt entry. "
            "Starting with {0} rows.".format(len(df.index))
        )
        df = compare_to_uni(df, dirs.uni_data)
        print(
            'Function "compare_to_uni" complete. '
            'There are now {} rows'.format(len(df.index))
        )

        df.to_csv(uni_filtered_path, sep=delimiter, encoding='utf-8')
        print("\npdb_seq_uni_filtered.tsv written")
        print(
            "Wrote {} file; second "
            "filtering complete.".format(uni_filtered_name)
        )
        print('\t"{}"'.format(uni_filtered_path))
    else:
        print(
            "Found {}. Using local file:\n"
            "\t{}".format(
                uni_filtered_name,
                uni_filtered_path
            )
        )
    msg.info('COMPLETE: Second filtering.')
    return None


def compare_to_uni(df, uni_folder):
    """Compare PDB seq to uniprot sequence; remove row if not exact match.

    Opens a UniProt fasta file for each line and compares with PDB_SEQ.

    Removes rows if the PDB sequence section is not 100% match with
    the corresponding UniProt section.

    Notes:
        Do this after UniProt files are downloaded.
        The input DataFrame should at this point only have the rows
        that are in ss_dis and there should be a value under PDB_SEQ.

    Args:
        df (DataFrame): A pre-filtered DataFrame from pdb_chain_uniprot.tsv
        uni_folder (Unicode): A directory path to the folder that has single
        UniProt fasta files.

    Returns:
        A filtered DataFrame with PDB_SEQ removed, a list of UniProt
        files that were missing from the UniProt folder.
    """
    progress = ProgressBar(
        len(df.index),
        start_msg=("Comparing PDB uniprot sequences and "
                   "removing non-matching rows."),
        end_msg="Finished comparing PDB uniprot sequences.",
        approx_percentage=1
    )
    for i, row in df.iterrows():
        uni_id = row.SP_PRIMARY
        uni_fp = build_abs_path(uni_folder, uni_id)

        try:
            uni_seq = (SeqIO.read(open(uni_fp), "fasta")).seq
        except ValueError:
            print(
                "The UniProt folder must have UniProt files for all "
                "lines in the DataFrame. {0} cannot be opened".format(uni_id))
        else:
            uni_peptide = uni_seq[row.SP_BEG-1:row.SP_END]
            if uni_peptide != row.PDB_SEQ:
                df.drop(i, inplace=True)
        progress.inc()

    df.drop('PDB_SEQ', axis=1, inplace=True)
    return df
