# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import os
import shutil
import tempfile
import unittest
from os.path import isdir

from pdb.lib.create_folders import create_folders
from pdb.lib.data_paths import ProjectFolders


class CreateFoldersTest(unittest.TestCase):

    def setUp(self):
        project_dp = tempfile.mkdtemp(prefix='pdb-tests_')
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

    def test_project_folder_success(self):
        """create_folders()"""
        expected_path = self.dirs.project_home
        self.assertTrue(os.path.exists(expected_path))

    def test_working_folder_success(self):
        """create_folders()"""
        create_folders(self.dirs)
        expected_path = self.dirs.working
        self.assertTrue(isdir(expected_path))

    def test_uni_folder_success(self):
        """create_folders()"""
        create_folders(self.dirs)
        expected_path = self.dirs.uni_data
        self.assertTrue(isdir(expected_path))

    def test_tsv_folder_success(self):
        """create_folders()"""
        create_folders(self.dirs)
        expected_path = self.dirs.tsv_data
        self.assertTrue(isdir(expected_path))

    def tearDown(self):
        shutil.rmtree(self.dirs.project_home)


if __name__ == '__main__':
    unittest.main()
