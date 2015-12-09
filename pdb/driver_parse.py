# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import os

from pdb.fetch_and_write import fetch_and_write_files
from pdb.fetch_uniprot import UniProtFetcher
from pdb.filtering_step_one import initial_filtering
from pdb.filtering_step_three import final_filtering
from pdb.filtering_step_two import second_filtering
from pdb.lib.create_folders import create_folders
from pdb.lib.data_paths import ProjectFolders, find_home_dir
from pdb.uni_composite import uniprot_composite


def main():
    user_home = find_home_dir()
    project_dp = os.path.join(user_home, 'pdb')
    uni_dp = os.path.join(project_dp, 'uni_data')
    tsv_dp = os.path.join(project_dp, 'tsv_data')
    working_dp = os.path.join(project_dp, 'working')

    dirs = ProjectFolders(
        user_home=user_home,
        project_home=project_dp,
        uni_data=uni_dp,
        tsv_data=tsv_dp,
        working=working_dp
    )
    create_folders(dirs)

    fetch_and_write_files(dirs)
    initial_filtering(dirs)
    fetcher = UniProtFetcher(dirs)
    fetcher.fetch_fasta_files()
    second_filtering(dirs)
    final_filtering(dirs)
    uniprot_composite(dirs)
    print("Processing finished successfully.")
    return None


if __name__ == '__main__':
    main()
