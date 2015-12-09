# -*- coding: utf-8 -*-
"""Integration tests."""
from __future__ import (
    absolute_import, division, print_function, unicode_literals)


import os
import shutil
import stat
import unittest
from filecmp import cmp
from io import open
from os.path import exists
from tempfile import mkdtemp

from pdb.lib.data_paths import ProjectFolders
from pdb.filtering_step_one import initial_filtering

try:
    from StringIO import StringIO  # Python 2
except ImportError:
    from io import StringIO        # Python 3


class TestInitialFilteringDataExists(unittest.TestCase):
    """Test when initial data already exists."""
    def setUp(self):
        self.temp_dir = mkdtemp(prefix='pdb-tests_')

        working_dp = os.path.join(self.temp_dir, 'working')
        self.dirs = ProjectFolders(
            user_home=None,
            project_home=self.temp_dir,
            uni_data=None,
            tsv_data=None,
            working=working_dp
        )
        os.mkdir(working_dp)
        return None

    def test_pdb_seq_tsv_exists_pass(self):
        pdb_seq_fp = os.path.join(self.dirs.working, 'pdb_seq.tsv')
        with open(pdb_seq_fp, mode='w', encoding='utf-8') as pdb_fh:
            pdb_fh.writelines('\n')
        self.assertTrue(exists(pdb_seq_fp))

        initial_filtering(self.dirs)
        self.assertTrue(initial_filtering(self.dirs))
        return None

    def tearDown(self):
        shutil.rmtree(self.temp_dir)


class TestGenerateInitialFilteringData(unittest.TestCase):
    """Test the generation of initial filtering data."""
    def setUp(self):
        self.temp_dir = mkdtemp(prefix='pdb-tests_')

        this_file_path = os.path.abspath(__file__)
        this_dir_path = os.path.dirname(this_file_path)
        source_path = os.path.join(
            this_dir_path, 'data', 'initial_filtering_data'
        )
        dst_path = os.path.join(self.temp_dir, 'initial_filtering_data')
        shutil.copytree(source_path, dst_path)

        project_dp = os.path.join(
            self.temp_dir, 'initial_filtering_data'
        )
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

    def test_generate_pdb_seq_tsv_pass(self):
        expected_pdb_seq_fp = os.path.join(
            self.dirs.working,
            'pdb_seq.tsv.expected'
        )
        result_pdb_seq_fp = os.path.join(
            self.dirs.working,
            'pdb_seq.tsv'
        )
        initial_filtering(self.dirs)
        set_write_permissions(self.temp_dir)
        self.assertTrue(exists(result_pdb_seq_fp))
        self.assertTrue(
            cmp(expected_pdb_seq_fp, result_pdb_seq_fp, shallow=0)
        )
        return None

    def tearDown(self):
        print(os.getcwd())
        shutil.rmtree(self.temp_dir)
        return None


def set_write_permissions(this_dir_path):
    """Individually set each file and directory to write.

    os.chmod doesn't work well with Windows, therefore
    recursively set stat.S_IWRITE on each directory object.

    Args:
        this_dir_path (Unicode): The full directory path on which to set
            write permissions.

    Returns:
        None

    """
    os.chmod(this_dir_path, stat.S_IWRITE)
    for path, subdirs, files_list in os.walk(this_dir_path):
        for file_name in files_list:
            os.chmod(
                os.path.join(path, file_name),
                stat.S_IWRITE
            )
        for dir_name in subdirs:
            os.chmod(
                os.path.join(path, dir_name),
                stat.S_IWRITE
            )
    return None


if __name__ == '__main__':
    unittest.main()
