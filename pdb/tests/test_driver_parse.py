# -*- coding: utf-8 -*-
"""Fetching and Parsing"""
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import os
import unittest
from io import open
from tempfile import mkdtemp

from pdb.lib.create_folders import create_folders
from pdb.lib.data_paths import find_home_dir, ProjectFolders
from pdb.tests.test_data import TsvData, UniData


class TestUniProtProcessing(unittest.TestCase):
    def _generate_dir_names(self, project_name='pdb'):
        user_home = find_home_dir()
        project_dp = os.path.join(user_home, 'pdb')
        uni_dp = os.path.join(project_dp, 'uni_data')
        tsv_dp = os.path.join(project_dp, 'tsv_data')
        working_dp = os.path.join(project_dp, 'working')
        self.dirs = ProjectFolders(
            user_home=user_home,
            project_home=project_dp,
            uni_data=uni_dp,
            tsv_data=tsv_dp,
            working=working_dp
        )
        return None

    def _get_test_data_dir(self):
        file_path = os.path.abspath(__file__)
        self.test_data_dp = os.path.dirname(file_path)
        return None

    def _write_initial_tsv(self):
        print(self.tsv_test_fp)
        with open(self.tsv_test_fp, 'w', encoding='utf-8') as tsv_fh:
            tsv_fh.write(TsvData.pdb_seq_tsv_valid)
        return None

    def _write_initial_uni(self):
        for uni_name in ['P00720', 'P02185']:
            uni_path = os.path.join(
                self.dirs.uni_data,
                uni_name + '.fasta'
            )
            with open(uni_path, 'w', encoding='utf-8') as uni_fh:
                uni_fh.write(getattr(UniData, uni_name))
        return None

    def setUp(self):
        self.temp_dir = mkdtemp(prefix='pdb-tests_')
        self. _get_test_data_dir()
        self._generate_dir_names()
        self.tsv_test_fp = os.path.join(
            self.dirs.working,
            'pdb_seq.tsv'
        )
        create_folders(self.dirs)
        return None


if __name__ == '__main__':
    unittest.main()
