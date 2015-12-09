# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals)


import unittest
import os

from io import open
from tempfile import mkdtemp

from pdb.fetch_uniprot import UniProtFetcher
from pdb.lib.data_paths import ProjectFolders, find_home_dir
from pdb.tests.test_data import TsvData


class TestLoadUniProt(unittest.TestCase):
    def _write_mock_tsv(self):
        tsv_fp = os.path.join(self.dirs.working, 'pdb_seq.tsv')
        with open(tsv_fp, 'w', encoding='utf-8') as tsv_fh:
            tsv_fh.writelines(TsvData.pdb_seq_tsv_valid)
            pass
        return None

    def _generate_dir_names(self):
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

    def setUp(self):
        self.temp_dir = mkdtemp(prefix='pdb-tests_')
        self._generate_dir_names()
        self._write_mock_tsv()

        return None

    def test_404_assigned_as_obsolete(self):
        """HTTP 404 errors should be assigned as obsolete, not missing."""
        uni_id = 'P123451'
        fetcher = UniProtFetcher(self.dirs)
        fetcher._download_uniprot(uni_id)
        self.assertTrue(uni_id in fetcher.obs)
        return None

    def test_known_obsolete_pass(self):
        """Test zero length HTTP 200 UniProt download."""
        uni_id = 'Q8NI70'
        fetcher = UniProtFetcher(self.dirs)
        fetcher._download_uniprot(uni_id)
        self.assertTrue(uni_id in fetcher.obs)
        return None

if __name__ == '__main__':
    unittest.main()
