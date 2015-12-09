# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import os
import pandas as pd

from os.path import basename

from pdb.fetch_ss_dis import fetch_ss_dis
from pdb.lib.create_delimiter import create_delimiter
from pdb.lib.data_paths import ProjectFolders
from pdb.lib.pdb_tools import filter_single
from pdb.pdb_composite import create_pdb_composite


def final_filtering(dirs):
    """Create PDB composite.

    Args:
        dirs (ProjectFolders): A named tuple of directory paths.

    """
    pdb_initial_composite_fp = os.path.join(
        dirs.tsv_data,
        'pdb_initial_composite_df.tsv'
    )

    uni_filtered_path = os.path.join(
        dirs.working,
        'pdb_seq_uni_filtered.tsv'
    )
    if not os.path.exists(pdb_initial_composite_fp):
        df = pd.read_csv(
            uni_filtered_path,
            sep='\t',
            index_col=0,
            keep_default_na=False,
            na_values=['NULL', 'N/A']
        )
        ss_dis = fetch_ss_dis(dirs.working)
        print("Creating PDB composite.")
        df = create_pdb_composite(df, ss_dis, dirs.uni_data)
        print("\nPDB composite finished.")

        print(
            "Removing UniProt entries with < 2 PDB "
            "chains. Starting with {0} rows".format(len(df.index))
        )
        df = filter_single(df)
        print(
            "Entries removed. There are now {0} rows".format(len(df.index))
        )

        print("Writing final PDB chain DataFrame.")
        delimiter = create_delimiter('\t')
        df.to_csv(pdb_initial_composite_fp, sep=delimiter, encoding='utf-8')
        print(
            "Finished writing {}:\n"
            "\t{}\n"
            "This is the final PDB_CHAIN DataFrame.\n"
            "Note that only pdb_chain_uniprot.tsv provides a "
            "unique key".format(
                basename(pdb_initial_composite_fp),
                pdb_initial_composite_fp,
            )
        )
    else:
        print(
            "Found {}. Using local file:\n"
            "\t{}".format(
                basename(pdb_initial_composite_fp),
                pdb_initial_composite_fp
            )
        )
    print("")
    return None
