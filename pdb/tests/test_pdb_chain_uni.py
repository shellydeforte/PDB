# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import os
import re
import sys
import unittest
from contextlib import contextmanager
from io import open
from shutil import rmtree
from tempfile import mkdtemp

from pdb.lib.data_paths import ProjectFolders, find_home_dir
from pdb.fetch_pdb_chain_uni import fetch_pdb_chain_uniprot

try:
    from StringIO import StringIO  # Python 2
except ImportError:
    from io import StringIO        # Python 3


class TesPDBChain(unittest.TestCase):
    """ """
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

    def setUp(self):
        self.temp_dir = mkdtemp(prefix='pdb-tests_')
        self. _get_test_data_dir()
        self._generate_dir_names()
        self.tsv_test_fp = os.path.join(
            self.dirs.working,
            'pdb_seq.tsv'
        )
        # create_folders(self.dirs)
        return None

    def test_fetch_pdb_chain_existing_file_pass(self):
        """fetch_pdb_chain_uniprot with existing file"""
        success_msg = re.compile(
            r'^Found local copy of.*',
            re.IGNORECASE
        )

        chain_fp = os.path.join(
            self.test_data_dp,
            'data',
            'initial_filtering_data',
            'tsv_data',
            'pdb_chain_uniprot.tsv')
        with captured_stdout() as stdout:
            fetch_pdb_chain_uniprot(chain_fp)
        result = stdout.getvalue().strip()
        print(result)
        self.assertTrue(success_msg.search(result))
        return None


class ManualTests(unittest.TestCase):
    """Tests that should be run manually and only occasionally
    to prevent needless load on servers."""
    def _get_test_data_dir(self):
        file_path = os.path.abspath(__file__)
        self.test_data_dp = os.path.dirname(file_path)
        return None

    def setUp(self):
        self. _get_test_data_dir()
        self.temp_dir = mkdtemp(prefix='pdb-tests_')
        self.working_dp = os.path.join(
            self.test_data_dp,
            'data',
            'initial_filtering_data',
            'working'
        )
        return None

    @unittest.skip("Run download tests manually when needed.")
    def test_fetch_pdb_chain_from_server_pass(self):
        expected = re.compile(r'(\w+\t\w{1,2}\t\w+\t(\d+[\t\n]){6,})')

        chain_fp = os.path.join(
            self.temp_dir,
            'pdb_chain_uniprot.tsv')
        fetch_pdb_chain_uniprot(chain_fp)
        with open(chain_fp, 'r', encoding='utf-8') as chain_fh:
            for line in chain_fh.readlines()[3:10]:
                self.assertTrue(expected.search(line))
        return None

    def tearDown(self):
        rmtree(self.temp_dir)


@contextmanager
def captured_stdout():
    """Capture standard output to for tests where
    functions aren't returning or writing data."""
    original_stdout = sys.stdout
    new_stdout = StringIO()
    try:
        sys.stdout = new_stdout
        yield sys.stdout
    finally:
        sys.stdout = original_stdout


if __name__ == '__main__':
    unittest.main()
