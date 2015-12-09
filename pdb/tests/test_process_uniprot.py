# -*- coding: utf-8 -*-
"""Fetching and Parsing"""
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import os
import unittest
from io import open
from tempfile import mkdtemp

from pdb.fetch_uniprot import UniProtFetcher
from pdb.lib.create_folders import create_folders
from pdb.lib.data_paths import ProjectFolders
from pdb.tests.test_data import TsvData, UniData


class TestUniProtProcessing(unittest.TestCase):
    """Temporary tests prior to refactoring."""
    def _create_dirs(self, project_name='pdb'):
        project_dp = os.path.join(self.temp_dir, project_name)
        uni_dp = os.path.join(project_dp, 'uni_data')
        tsv_dp = os.path.join(project_dp, 'tsv_data')
        working_dp = os.path.join(project_dp, 'working')
        self.dirs = ProjectFolders(
            user_home=None,
            project_home=project_dp,
            uni_data=uni_dp,
            tsv_data=tsv_dp,
            working=working_dp
        )
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
        self._create_dirs()
        self.tsv_test_fp = os.path.join(
            self.dirs.working,
            'pdb_seq.tsv'
        )
        create_folders(self.dirs)
        return None

    def test_download_uniprot_with_obsolete_pass(self):
        self._write_initial_tsv()
        self._write_initial_uni()

        fetcher = UniProtFetcher(self.dirs)
        fetcher.fetch_fasta_files()

        with open(self.tsv_test_fp, 'r', encoding='utf-8') as result_fh:
            result = result_fh.read()
        self.assertEqual(result, TsvData.pdb_seq_tsv_valid)
        return None


if __name__ == '__main__':
    unittest.main()
