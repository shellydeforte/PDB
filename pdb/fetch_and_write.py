# -*- coding: utf-8 -*-
"""Download data files if they don't exist and write to project folder."""
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import os
from pdb.fetch_obsolete import fetch_obsolete
from pdb.fetch_xray import fetch_xray
from pdb.lib.data_paths import ProjectFolders
from pdb.fetch_pdb_chain_uni import fetch_pdb_chain_uniprot


def fetch_and_write_files(dirs):
    """Fetch initial data files.

    Fetch data from remote servers and write to files if local files
    do not already exist. Fetches pdb_chain_uniprot.tsv, obsolete PDB
    files, and X-ray PDB files.

    Args:
        dirs (ProjectFolders): A named tuple of directory paths.

    Returns:
        None

    """
    assert isinstance(dirs, ProjectFolders)
    assert os.path.isdir(dirs.project_home)
    assert dirs.uni_data
    assert dirs.tsv_data
    assert dirs.working

    # Run unit test for this manually to not overload servers.
    obs_fp = os.path.join(dirs.working, 'obs.yaml')
    if not os.path.exists(obs_fp):
        fetch_obsolete(obs_fp)

    # Run unit test for this manually to not overload servers.
    xray_fp = os.path.join(dirs.working, 'xray.yaml')
    if not os.path.exists(xray_fp):
        fetch_xray(xray_fp)

    # Run unit test for this manually to not overload servers.
    chain_fp = os.path.join(dirs.tsv_data, 'pdb_chain_uniprot.tsv')
    if not os.path.exists(chain_fp):
        fetch_pdb_chain_uniprot(chain_fp)

    return None
