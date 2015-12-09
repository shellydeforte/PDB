# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

from logging import getLogger

from pdb.lib.progress_bar import ProgressBar


def filter_single(df):
    """Removes UniProt IDs with only one unique PDB chain.

    This filters out any UniProt IDs that do not have > 1 unique PDB chains.
    It will accept a dataframe that has PDB_CHAIN combined or PDB and CHAIN
    separate.

    Note that it is possible to have the same protein multiple times
    on a single chain, and that's why I have chosen to actually iterate
    through and check for unique chains for those tsv files that have the
    PDB and CHAIN separated. Note also that a unique key is created by
    pdb id, chain and uniprot ID.

    Args:
        df: This can accept a DataFrame that has the PDB_CHAIN combined,
        or that has the PDB and CHAIN as separate columns.

    Returns:
        A filtered DataFrame

    """
    log_error = getLogger('pdb_app_logger')
    if 'PDB_CHAIN' in df.columns:
        uni_list = read_pdb_chain_uniprot_uniIDs(df)
        drop_list = []
        progress = ProgressBar(
            len(uni_list),
            start_msg="Removing UniProt IDs with only one unique PDB chain.",
            end_msg="Done removing UniProt IDs."
        )
        for uni in uni_list:
            pdbs = df[df.SP_PRIMARY == uni]
            if len(pdbs.index) < 2:
                drop_list.append(uni)
            progress.inc()
        df = df[-df.SP_PRIMARY.isin(drop_list)]

    else:
        uni_list = read_pdb_chain_uniprot_uniIDs(df)
        drop_list = []
        progress = ProgressBar(
            len(uni_list),
            start_msg="Removing UniProt IDs with only one unique PDB chain.",
            end_msg="Done removing UniProt IDs."
        )
        for uni in uni_list:
            pdbs = df[df.SP_PRIMARY == uni]
            pdb_chains = []
            for i, row in pdbs.iterrows():
                try:
                    new_chain = ''.join([
                        row.PDB,
                        '_',
                        row.CHAIN
                    ])
                except TypeError as append_err:
                    log_error.warning(
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
                else:
                    pdb_chains.append(new_chain)

            if len(set(pdb_chains)) < 2:
                drop_list.append(uni)
            progress.inc()
        df = df[-df.SP_PRIMARY.isin(drop_list)]

    return df


def read_pdb_chain_uniprot_uniIDs(df):
    """Extract UniIDs from a pdb_chain_uniprot.tsv DataFrame."""
    uni_list = df.SP_PRIMARY.tolist()
    return list(set(uni_list))


def uni_pdb_validation(uni_df, pdb_df):
    """Check that UniProt IDs are identical between the two DataFrames.

    Check that the UniIDs are a unique key in uni_df.

    """
    pdb_list = read_pdb_chain_uniprot_uniIDs(pdb_df)
    uni_list = read_pdb_chain_uniprot_uniIDs(uni_df)
    assert len(
        set(pdb_list) ^ set(uni_list)) == 0
    assert len(set(uni_list)) == len(uni_list)
    return None
