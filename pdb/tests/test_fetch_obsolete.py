# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import os
import re
from shutil import rmtree
import sys
import unittest

from contextlib import contextmanager
from io import open
from tempfile import mkdtemp

from pdb.fetch_obsolete import fetch_obsolete
from pdb.lib.file_io import read_yaml

try:
    from StringIO import StringIO  # Python 2
except ImportError:
    from io import StringIO        # Python 3


class TestFetchObsolete(unittest.TestCase):
    def setUp(self):
        self.success_msg = re.compile(
            r'^Found local copy of.*',
            re.IGNORECASE
        )
        self.temp_dir = mkdtemp(prefix='pdb-tests_')
        return None

    def test_fetch_obsolete_existing_file_pass(self):
        """Test fetch_obsolete() when file exists."""
        obs_fp = os.path.join(self.temp_dir, 'obs.yaml')

        with open(obs_fp, 'w', encoding='utf-8') as obs_fh:
            obs_fh.writelines("\n")

        with captured_stdout() as stdout:
            fetch_obsolete(obs_fp)
        result = stdout.getvalue().strip()
        self.assertTrue(self.success_msg.search(result))
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
    def test_fetch_obsolete_from_servers(self):
        expected = {
            "2TNA", "2TNC", "2UCE", "2UV9", "2UVA", "2UVB", "2UVC",
            "2UWG", "2UWY", "2UWZ", "2V0Q", "2V2Y", "2V44", "2V46"
        }
        obs_fp = os.path.join(self.temp_dir, 'obs.yaml')
        fetch_obsolete(obs_fp)
        self.assertTrue(expected < set(read_yaml(obs_fp)))
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
