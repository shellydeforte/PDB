# -*- coding: utf-8 -*-
"""Test lib.file_io."""
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import os
import re
import unittest
from shutil import rmtree
from tempfile import mkdtemp

from pdb.lib.data_paths import ProjectFolders
from pdb.uni_composite import (
    _create_composite_file_names, _create_composite_file_paths,
    _compile_uni_composite_regex, _get_local_file_names,
    _uni_composite_file_exists)


class TestJsonIO(unittest.TestCase):
    def _create_project_folders(self):
        project_dp = os.path.join(self.temp_dir, 'pdb')
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

    def _create_test_files(self):
        self.test_files = {
            'uni_composite.20151202T062045Z.tsv',
            'uni_composite.20151202T062047Z.tsv',
            'uni_composite.20151202T062050Z.tsv',
            'uni_composite.20151202T062052Z.tsv',
            'uni_composite.20151202T062054Z.tsv'
        }
        for test_fn in self.test_files:
            open(
                os.path.join(
                    self.temp_dir,
                    test_fn), 'w'
            ).close()
        return None

    def _create_valid_composite_regex(self):
        valid_composite_pat = """
                                   # Group 1
            (uni_composite)        # Base name
            \.                     # Literal period.

            (                      # Group 2
            \d{8,}                 # Date
            T                      # "T" (indicate time)
            \d{6,}                 # Time
            Z                      # "Z" (indicate GMT)
            )

            \.                     # Literal period.

                                   # Group 3
            (                      # Valid file extentions.
            (?:json)|(?:yaml)|(?:tsv)
            )
        """
        self.valid_composite_fn = re.compile(valid_composite_pat, re.VERBOSE)
        return None

    def setUp(self):
        self.temp_dir = mkdtemp(prefix='pdb-tests_')
        self._create_project_folders()
        self._create_test_files()
        self._create_valid_composite_regex()
        return None

    def test_create_composite_file_names_pass(self):
        result = _create_composite_file_names()
        for name in result:
            this_name = result[name]
            self.assertTrue(
                self.valid_composite_fn.search(this_name)
            )
        return None

    def test_create_composite_file_paths_pass(self):
        names = _create_composite_file_names()
        result = _create_composite_file_paths(self.temp_dir, names)
        for name in result:
            this_path = result[name]
            dir_name = os.path.dirname(this_path)
            self.assertTrue(os.path.isdir(dir_name))
            file_name = os.path.basename(this_path)
            self.assertTrue(self.valid_composite_fn.search(file_name))
        return None

    def test_match_time_stamped_composite_fn_pass(self):
        uniprot_composite_pat = _compile_uni_composite_regex()
        time_stamped_name = 'uni_composite.20151202T051543Z.tsv'
        self.assertTrue(uniprot_composite_pat.search(time_stamped_name))
        return None

    def test_match_composite_fn_pass(self):
        uniprot_composite_pat = _compile_uni_composite_regex()
        composite_name = 'uni_composite.tsv'
        self.assertTrue(uniprot_composite_pat.search(composite_name))
        return None

    def test_get_local_file_names(self):
        local_files = set(_get_local_file_names(self.temp_dir))
        self.assertEqual(local_files, self.test_files)
        return None

    def test_find_valid_file_pass(self):
        self.assertTrue(_uni_composite_file_exists(self.temp_dir))
        return None

    def tearDown(self):
        rmtree(self.temp_dir)
        return None


if __name__ == '__main__':
    unittest.main()
