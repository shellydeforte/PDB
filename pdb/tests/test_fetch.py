# -*- coding: utf-8 -*-
"""Unitests for fetch functions."""
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import os
import re
import sys
import unittest
from contextlib import contextmanager
from filecmp import cmp
from io import open
from os.path import join
from tempfile import mkdtemp

import pdb.fetch_ss_dis as ss
from pdb.fetch_obsolete import fetch_obsolete
from pdb.fetch_pdb_chain_uni import fetch_pdb_chain_uniprot
from pdb.fetch_uniprot import UniProtFetcher
from pdb.fetch_xray import fetch_xray
from pdb.lib.data_paths import ProjectFolders, find_home_dir
from pdb.lib.file_io import read_yaml

try:
    from StringIO import StringIO  # Python 2
except ImportError:
    from io import StringIO        # Python 3


class TestFetchingAndParsing(unittest.TestCase):
    """Test fetching functions when data already exists.

     Use stdout to test functions that take no action when
     data files already exists.

    """
    def setUp(self):
        self.success_msg = re.compile(
            r'^Found local copy of.*',
            re.IGNORECASE
        )
        self.temp_dir = mkdtemp(prefix='pdb-tests_')
        return None

    def test_fetch_xray_pass(self):
        """Test fetch_xray() when file exists."""
        xray_fp = os.path.join(self.temp_dir, 'xray.part.yaml')

        with open(xray_fp, 'w', encoding='utf-8') as xray_fh:
            xray_fh.writelines("\n")

        with captured_stdout() as stdout:
            fetch_obsolete(xray_fp)
        result = stdout.getvalue().strip()
        self.assertTrue(self.success_msg.search(result))
        return None

    def test_fetch_pdb_chain_pass(self):
        """test fetch_pdb_chain_uniprot() when file exists."""
        chain_fp = os.path.join(self.temp_dir, 'pdb_chain_uniprot.tsv')

        with open(chain_fp, 'w', encoding='utf-8') as chain_fh:
            chain_fh.writelines("\n")

        with captured_stdout() as stdout:
            fetch_obsolete(chain_fp)
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
        self.original_working_dir = os.getcwd()
        os.chdir(self.temp_dir)

        file_path = os.path.abspath(__file__)
        this_dir = os.path.dirname(file_path)
        self.data_dir = os.path.join(this_dir, 'data')
        self.uniprot_folder = os.path.join(this_dir, 'uniprot')
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

    @unittest.skip("Run test_fetch_xray_pass manually.")
    def test_fetch_xray_pass(self):
        """fetch_xray()"""
        xray_fp = os.path.join(self.temp_dir, 'xray.yaml')
        fetch_xray(xray_fp)
        self.assertTrue(os.path.isfile(xray_fp))
        expected = [
            '101M', '102L', '102M', '103L', '103M', '104L', '104M',
            '105M', '106M', '107L', '107M', '108L', '108M',
            '109L', '109M', '10GS', '10MH'
        ]
        result = read_yaml(xray_fp)
        self.assertTrue(set(expected) < set(result))
        return None

    @unittest.skip("Run test_force_fetch_obsolete_pass manually.")
    def test_force_fetch_obsolete_pass(self):
        """fetch_obsolete()"""
        obs_fp = os.path.join(self.temp_dir, 'obs.yaml')
        with open(obs_fp, 'w', encoding='utf-8') as obs_fh:
            obs_fh.write("\n")
        fetch_obsolete(obs_fp, force_download=True)
        expected = {'1E6T', '1E7T', '1E7X'}
        result = read_yaml(obs_fp)
        self.assertLess(expected, set(result))

    @unittest.skip("Run test_fetch_pdb_chain_original_pass manually.")
    def test_fetch_pdb_chain_original_pass(self):
        result_fp = join(
            self.temp_dir,
            'pdb_chain_uniprot.tsv'
        )
        expected_fp = join(
            self.test_data_dp,
            'data',
            'pdb_chain_uniprot.tsv.expected'
        )
        # print(expected_fp)
        fetch_pdb_chain_uniprot(result_fp)
        self.assertTrue(cmp(expected_fp, result_fp, shallow=False))
        return None

    @unittest.skip("Run test_download_and_write_data_pass manually.")
    def test_download_and_write_data_pass(self):
        new = ss._new_filenames()
        expected_fp = os.path.join(
            self.temp_dir,
            new.raw
        )
        ss._download_ss_data(expected_fp)
        self.assertTrue(os.path.isfile(expected_fp))
        return None

    @unittest.skip("Run test_mixed manually.")
    def test_mixed(self):
        result_fp = os.path.join(self.temp_dir, 'P25644.fasta')
        expected_fp = os.path.join(self.uniprot_folder, 'P25644_expected.fasta')

        expected = (['Q8NI70', 'P123451'], [])
        uni_list = ['Q8NI70', 'P123451', 'P25644']
        # TODO: Update unitest; fetch_uniprot replaced by class.
        # result = fetch_uniprot(uni_list, self.temp_dir)
        # self.assertEqual(expected, result)

        self.assertTrue(
            cmp(
                result_fp,
                expected_fp,
                shallow=False
            )
        )
        return None

    @unittest.skip("Run test_mixed manually.")
    def test_download_uniprot_pass(self):
        self._generate_dir_names()
        expected = '>sp|P12345|AATM_RABIT Aspartate aminotransferase, mitochondrial OS=Oryctolagus cuniculus GN=GOT2 PE=1 SV=2\nMALLHSARVLSGVASAFHPGLAAAASARASSWWAHVEMGPPDPILGVTEAYKRDTNSKKM\nNLGVGAYRDDNGKPYVLPSVRKAEAQIAAKGLDKEYLPIGGLAEFCRASAELALGENSEV\nVKSGRFVTVQTISGTGALRIGASFLQRFFKFSRDVFLPKPSWGNHTPIFRDAGMQLQSYR\nYYDPKTCGFDFTGALEDISKIPEQSVLLLHACAHNPTGVDPRPEQWKEIATVVKKRNLFA\nFFDMAYQGFASGDGDKDAWAVRHFIEQGINVCLCQSYAKNMGLYGERVGAFTVICKDADE\nAKRVESQLKILIRPMYSNPPIHGARIASTILTSPDLRKQWLQEVKGMADRIIGMRTQLVS\nNLKKEGSTHSWQHITDQIGMFCFTGLKPEQVERLTKEFSIYMTKDGRISVAGVTSGNVGY\nLAHAIHQVTK\n'
        uni_id = 'P12345'
        fetcher = UniProtFetcher(self.dirs)
        result = fetcher._download_uniprot(uni_id)
        self.assertEqual(expected, result)
        return None


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
