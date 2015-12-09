# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import re

from pdb.lib.progress_bar import ProgressBar


def create_intervals(pdb_df, uni_df):
    """Add a column to uni_df with the missing interval regions.

    Missing interval regions are of the following form:
        [
            ['conserved', (0, 10)],
            ['conflict', (34, 45)]
        ]

    Args:
        pdb_df (DataFrame): DataFrame with PDB_chains and composite structure.
        uni_df (DataFrame): DataFrame with UniProt IDs and
            composite UniProt structure.

    Returns:
        uni_df (DataFrame): A DataFrame which includes a column for
            the missing interval regions.

    """
    uni_df['MISSING'] = ''
    progress = ProgressBar(
        len(uni_df.index),
        approx_percentage=1,
        start_msg="Adding a column to uni_df with missing interval regions.",
        end_msg="Done adding columns."
    )
    for i, row in uni_df.iterrows():
        struct_indexes = []
        uni_id = row.SP_PRIMARY
        uni_struct = row.STRUCT
        pdbs = pdb_df[pdb_df.SP_PRIMARY == uni_id]
        indexes = _find_indexes(uni_struct)
        for ind in indexes:
            struct_intervals = []
            for j, line in pdbs.iterrows():
                assert len(line.SEC_STRUCT) == len(uni_struct)
                struct_intervals.append(line.SEC_STRUCT[ind[0]:ind[1]])
            for struct in struct_intervals:
                assert len(struct) == len(struct_intervals[0])
            assert len(struct_intervals) == len(pdbs.index)
            dis_type = determine_dis_type(struct_intervals)
            struct_indexes.append([dis_type, ind])
        assert len(indexes) == len(struct_indexes)
        uni_df.set_value(i, 'MISSING', struct_indexes)
        progress.inc()
    return uni_df


def _find_indexes(uni_struct):
    """ Returns the index positions of the missing regions.

    Given a string of characters, returns a list of indexes that provide
    the coordinates for contiguous stretches of 'X'. It will provide
    the initial index (starting from 0), and the last index +1, so
    these can be used to directly  call the missing region.

    Args:
    uni_struct (string): of the form '---OOOXXX--O'

    Returns:
        A list of indexes.. For example: [(0,10), (50,73),...]

    """
    return (
        [
            pos.span()
            for pos in re.finditer(r'(x+)', uni_struct, re.IGNORECASE)
        ]
    )


def determine_dis_type(struct_intervals):
    """Determine disorder type.

    struct_intervals are the section of structure for one
    interval. For example:
        ['XXP', 'XXP', 'XPP', 'XPP', 'XPP', 'XXX', '-XP', '-PP', 'XPP',
        'XXP', 'XXP', 'XPP']

    """
    if _is_conflict(struct_intervals):
        return 'conflict'
    elif not _qualifies(struct_intervals):
        return 'discarded'
    elif _is_conserved(struct_intervals):
        return 'conserved'
    elif _is_contained(struct_intervals):
        return 'contained'
    else:
        return 'overlap'


def _qualifies(struct_intervals, num=2):
    # At least num entries with X.
    count = 0
    for si in struct_intervals:
        if 'X' in si:
            count += 1
    if count >= num:
        return True
    else:
        return False


def _is_conflict(struct_intervals):
    # Contains any combination of: P, E, G, T, S, H, B, I.
    # Does not contain 'X' or '-'.
    # Only needs one interval to have structure.
    for si in struct_intervals:
        if 'X' not in si and '-' not in si:
            return True
    return False


def _is_conserved(struct_intervals):
    for si in struct_intervals:
        if set(si) != {'X'}:
            return False
    return True


def _is_contained(struct_intervals):
    # At least one is set(si) == set(['X']) and at least one other has at
    #  least one X. This tests only for the presence of
    #  one full length disordered interval.
    for si in struct_intervals:
        if set(si) == {'X'}:
            return True
    return False
