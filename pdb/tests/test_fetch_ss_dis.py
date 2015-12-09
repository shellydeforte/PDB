# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import errno
import os
import pdb.fetch_ss_dis as ss
import shutil
import stat
import unittest

from io import open
from tempfile import mkdtemp

from pdb.lib.datetime_info import now_utc


class TestSsDisorderData(unittest.TestCase):
    def setUp(self):
        # Create temp directory and store path.
        self.temp_dir = mkdtemp(prefix='pdb-tests_')
        self.original_working_dir = os.getcwd()
        os.chdir(self.temp_dir)

        # The test data directory should be located in
        # a directory below where this test file is located.
        file_path = os.path.abspath(__file__)
        this_dir = os.path.dirname(file_path)
        self.data_dir = os.path.join(this_dir, 'ss_test_data')

        # Create file for archive/backup test.
        self.archive_test_file = os.path.join(
            self.temp_dir,
            'ss_dis.20150201T020030Z.json'
        )
        open(self.archive_test_file, 'w', encoding='utf-8').close()
        return None

    def test_find_ss_data_pass(self):
        expected = [
            'ss_dis.20121101T020030Z.txt',
            'ss_dis.20131101T020030Z.txt',
            'ss_dis.20151101T020030Z.txt',
            'ss_dis.20151101T020030Z.json'
        ]
        result = ss._find_ss_data(self.data_dir)
        self.assertEqual(set(expected), set(result))
        return None

    def _test_make_backup_dir_pass(self):
        backup_path = os.path.join(self.temp_dir, 'backup')
        assert not os.path.exists(backup_path)
        ss._make_backup_dir(self.temp_dir)
        self.assertTrue(os.path.isdir(backup_path))
        return None

    def test_archive_ss_data_pass(self):
        ss._archive_ss_data(
            self.archive_test_file
        )

        # Assert that the original file was removed.
        self.assertFalse(os.path.isfile(self.archive_test_file))

        # Assert that the new archive file exists.
        base_name = os.path.basename(self.archive_test_file)
        expected = os.path.join(self.temp_dir, 'backup', base_name)
        self.assertTrue(os.path.isfile(expected))
        return None

    def test_archive_read_only_file_pass(self):
        this_dir_path = os.path.dirname(self.archive_test_file)
        backup_dir_path = os.path.join(this_dir_path, 'backup')
        archive_file_name = os.path.basename(self.archive_test_file)
        archive_file_path = os.path.join(backup_dir_path, archive_file_name)

        os.chmod(self.archive_test_file, stat.S_IREAD)
        ss._archive_ss_data(
            self.archive_test_file
        )

        self.assertTrue(os.path.isfile(archive_file_path))
        self.assertFalse(os.path.isfile(self.archive_test_file))
        return None

    def test_find_matching_datetimes_pass(self):
        filenames = [
            'ss_dis.20151101T020030Z.txt',
            'ss_dis.20141103T020030Z.json',
            'ss_dis.20120203T020030Z.txt',
            'ss_dis.20120203T020030Z.json',
            'ss_dis.20110203T020030Z.txt',
            'ss_dis.20110203T020030Z.json'
        ]
        filenames.sort(reverse=True)
        result = ss._find_matching_datetime_pairs(filenames)
        expected = {
            'files_to_archive': [
                'ss_dis.20151101T020030Z.txt',
                'ss_dis.20141103T020030Z.json',
                'ss_dis.20110203T020030Z.json',
                'ss_dis.20110203T020030Z.txt'],
            'valid_raw_file': 'ss_dis.20120203T020030Z.txt',
            'valid_json_file': 'ss_dis.20120203T020030Z.json'
        }
        self.assertEqual(set(expected), set(result))
        return None

    def test_no_matching_datetimess_raw_exists_pass(self):
        """_find_matching_datetime_pairs()

        Test no matching pairs. The most recent text file (raw
        data) should be returned.

        """
        filenames = [
            'ss_dis.20151101T020030Z.txt',
            'ss_dis.20141103T020030Z.json',
            'ss_dis.20120203T020030Z.json',
            'ss_dis.20110203T020030Z.txt',
            'ss_dis.20110203T020030Z.txt'
        ]
        filenames.sort(reverse=True)

        result = ss._find_matching_datetime_pairs(filenames)
        expected = {
            'files_to_archive': [
                'ss_dis.20141103T020030Z.json',
                'ss_dis.20120203T020030Z.json',
                'ss_dis.20110203T020030Z.txt',
                'ss_dis.20110203T020030Z.txt'],
            'valid_raw_file': 'ss_dis.20151101T020030Z.txt',
            'valid_json_file': None
        }
        self.assertEqual(expected, result)
        return None

    def test_no_matching_datetimes_or_raw_pass(self):
        """_find_matching_datetime_pairs()

        Test no matching pairs and no text files (raw
        data).

        """
        filenames = [
            'ss_dis.20151101T020030Z.json',
            'ss_dis.20141103T020030Z.json',
            'ss_dis.20120203T020030Z.json',
            'ss_dis.20110203T020030Z.json',
            'ss_dis.20110203T020030Z.json'
        ]
        filenames.sort(reverse=True)

        result = ss._find_matching_datetime_pairs(filenames)
        expected = {
            'files_to_archive': [
                'ss_dis.20151101T020030Z.json',
                'ss_dis.20141103T020030Z.json',
                'ss_dis.20120203T020030Z.json',
                'ss_dis.20110203T020030Z.json',
                'ss_dis.20110203T020030Z.json'],
            'valid_raw_file': None,
            'valid_json_file': None
        }
        self.assertEqual(expected, result)
        return None

    def test_single_datetimes_txt_pass(self):
        """find_matching_datetimes()"""
        filenames = [
            'ss_dis.20151101T020030Z.txt'
        ]
        expected = {
            'files_to_archive': [],
            'valid_raw_file': 'ss_dis.20151101T020030Z.txt',
            'valid_json_file': None
        }
        result = ss._find_matching_datetime_pairs(filenames)
        self.assertEqual(expected, result)
        return None

    def test_single_datetimes_json_pass(self):
        """find_matching_datetimes()"""
        filenames = [
            'ss_dis.20151101T020030Z.json'
        ]
        expected = {
            'files_to_archive': ['ss_dis.20151101T020030Z.json'],
            'valid_raw_file': None,
            'valid_json_file': None
        }
        result = ss._find_matching_datetime_pairs(filenames)
        self.assertEqual(expected, result)
        return None

    def test_new_filenames_pass(self):
        estimated_time = now_utc()
        result_names = ss._new_filenames()
        json_base, json_time, json_ext = result_names.json.split('.')
        raw_base, raw_time, raw_ext = result_names.raw.split('.')

        self.assertEqual(json_time, raw_time)
        self.assertAlmostEquals(json_time, estimated_time)
        self.assertEqual({json_base, raw_base, 'ss_dis'}, {'ss_dis'})
        self.assertEqual(json_ext, 'json')
        self.assertEqual(raw_ext, 'txt')
        return None

    def _handle_remove_readonly(self, func, path, except_info):
        error_no = except_info[1]
        try:
            func in (os.rmdir, os.remove) and error_no.errno == errno.EACCES
        except:
            raise
        else:
            os.chmod(path, stat.S_IWRITE)
            func(path)
        return None

    def tearDown(self):
        os.chdir(self.original_working_dir)
        try:
            shutil.rmtree(
                self.temp_dir,
                ignore_errors=False,
                onerror=self._handle_remove_readonly)
        except OSError as os_err:
            msg = (
                "\nrmtree failed with an OSError "
                "while removing folder:\n"
                "\t\"{}\"\n"
                "Manually remove the path if necessary.\n"
                "The error details are:".format(
                    self.temp_dir
                )
            )
            for arg in os_err.args:
                msg = (
                    "{}\n"
                    "\t\"{}\"".format(msg, arg)
                )
            print(msg)
        else:
            self.assertFalse(os.path.isdir(self.temp_dir))
        return None


class TestGetSsDisDictionary(unittest.TestCase):
    def setUp(self):
        # Create temp directory and store path.
        self.temp_dir = mkdtemp(prefix='pdb-tests_')
        self.original_working_dir = os.getcwd()
        os.chdir(self.temp_dir)

        # The test data directory should be located in
        # a directory below where this test file is located.
        file_path = os.path.abspath(__file__)
        this_dir = os.path.dirname(file_path)
        self.data_dir = os.path.join(this_dir, 'ss_test_data')
        return None

    def write_fasta(self, time_stamp):
        fasta = """>1DBO:A:sequence
MKMLNKLAGYLLPIMVLLNVAPCLGQVVASNETLYQVVKEVKPGGLVQIADGTYKDVQLIVSNSGKSGLPITIKA
LNPGKVFFTGDAKVELRGEHLILEGIWFKDGNRAIQAWKSHGPGLVAIYGSYNRITACVFDCFDEANSAYITTSL
TEDGKVPQHCRIDHCSFTDKITFDQVINLNNTARAIKDGSVGGPGMYHRVDHCFFSNPQKPGNAGGGIRIGYYRN
DIGRCLVDSNLFMRQDSEAEIITSKSQENVYYGNTYLNCQGTMNFRHGDHQVAINNFYIGNDQRFGYGGMFVWGS
RHVIACNYFELSETIKSRGNAALYLNPGAMASEHALAFDMLIANNAFINVNGYAIHFNPLDERRKEYCAANRLKF
ETPHQLMLKGNLFFKDKPYVYPFFKDDYFIAGKNSWTGNVALGVEKGIPVNISANRSAYKPVKIKDIQPIEGIAL
DLNALISKGITGKPLSWDEVRPYWLKEMPGTYALTARLSADRAAKFKAVIKRNKEH
>5C1Z:B:sequence
MIVFVRFNSSHGFPVEVDSDTSIFQLKEVVAKRQGVPADQLRVIFAGKELRNDWTVQNCDLDQQSIVHIVQRPWR
KGQEMNATNSFYVYCKGPCQRVQPGKLRVQCSTCRQATLTLTQGPSCWDDVLIPNRMSGECQSPHCPGTSAEFFF
KCGAHPTSDKETSVALHLIATNSRNITCITCTDVRSPVLVFQCNSRHVICLDCFHLYCVTRLNDRQFVHDPQLGY
SLPCVAGCPNSLIKELHHFRILGEEQYNRYQQYGAEECVLQMGGVLCPRPGCGAGLLPEPDQRKVTCEGGNGLGC
GFAFCRECKEAYHEGECSAVFEASGTTTQAYRVDERAAEQARWEAASKETIKKTTKPCPRCHVPVEKNGGCMHMK
CPQPQCRLEWCWNCGCEWNRVCMGDHWFDV
>5C1Z:B:secstr
 EEEEESSSSS EEEE  TT BHHHHHHHHHHHHTS GGGEEEEETTEEE TT BHHHHT  TT EEEEEE
    TT     EEEETTTT EEEEEEEEEEETTT SS EEESS   SHHHHHSTT SBEEE STT    BEEEEE
EESSS   TT   EE TTEE  TT  B TTT  B SSEEE  STT BEEEHHHHHHHHHHHHHTT  EEETTTEE
E   TT  TT   S GGGGGG
"""
        txt_file_name = (
            "{}.{}.{}".format(
                'ss_dis',
                time_stamp,
                'txt'
            )
        )

        txt_file_path = os.path.join(self.temp_dir, txt_file_name)
        with open(
                txt_file_path,
                mode='w',
                encoding='utf-8') as raw:
            for line in fasta:
                raw.writelines(line)
        assert os.path.isfile(txt_file_path)
        return None

    def test_generate_json(self):
        time_stamp = now_utc()
        json_file_name = (
            "{}.{}.{}".format(
                'ss_dis',
                time_stamp,
                'json'
            )
        )
        json_file_path = os.path.join(self.temp_dir, json_file_name)

        self.write_fasta(time_stamp)
        self.assertFalse(os.path.isfile(json_file_path))
        ss.fetch_ss_dis(self.temp_dir)
        self.assertTrue(os.path.isfile(json_file_path))
        return None

    def test_generate_json_and_return_dic(self):
        # TODO: Value of expected updated to include '\r' after from __future__ import unicode_literals and from io import os. Validate this data.
        expected = {
            u'1DBO_A': {
                u'disorder': u'',
                u'secstr': u'',
                u'sequence': u'MKMLNKLAGYLLPIMVLLNVAPCLGQVVASNETLYQVVKEVKPGGLVQIADGTYKDVQLIVSNSGKSGLPITIKALNPGKVFFTGDAKVELRGEHLILEGIWFKDGNRAIQAWKSHGPGLVAIYGSYNRITACVFDCFDEANSAYITTSLTEDGKVPQHCRIDHCSFTDKITFDQVINLNNTARAIKDGSVGGPGMYHRVDHCFFSNPQKPGNAGGGIRIGYYRNDIGRCLVDSNLFMRQDSEAEIITSKSQENVYYGNTYLNCQGTMNFRHGDHQVAINNFYIGNDQRFGYGGMFVWGSRHVIACNYFELSETIKSRGNAALYLNPGAMASEHALAFDMLIANNAFINVNGYAIHFNPLDERRKEYCAANRLKFETPHQLMLKGNLFFKDKPYVYPFFKDDYFIAGKNSWTGNVALGVEKGIPVNISANRSAYKPVKIKDIQPIEGIALDLNALISKGITGKPLSWDEVRPYWLKEMPGTYALTARLSADRAAKFKAVIKRNKEH'
            },
            u'5C1Z_B': {
                u'disorder': u'',
                u'secstr': u' EEEEESSSSS EEEE  TT BHHHHHHHHHHHHTS GGGEEEEETTEEE TT BHHHHT  TT EEEEEE    TT     EEEETTTT EEEEEEEEEEETTT SS EEESS   SHHHHHSTT SBEEE STT    BEEEEEEESSS   TT   EE TTEE  TT  B TTT  B SSEEE  STT BEEEHHHHHHHHHHHHHTT  EEETTTEEE   TT  TT   S GGGGGG',
                u'sequence': u'MIVFVRFNSSHGFPVEVDSDTSIFQLKEVVAKRQGVPADQLRVIFAGKELRNDWTVQNCDLDQQSIVHIVQRPWRKGQEMNATNSFYVYCKGPCQRVQPGKLRVQCSTCRQATLTLTQGPSCWDDVLIPNRMSGECQSPHCPGTSAEFFFKCGAHPTSDKETSVALHLIATNSRNITCITCTDVRSPVLVFQCNSRHVICLDCFHLYCVTRLNDRQFVHDPQLGYSLPCVAGCPNSLIKELHHFRILGEEQYNRYQQYGAEECVLQMGGVLCPRPGCGAGLLPEPDQRKVTCEGGNGLGCGFAFCRECKEAYHEGECSAVFEASGTTTQAYRVDERAAEQARWEAASKETIKKTTKPCPRCHVPVEKNGGCMHMKCPQPQCRLEWCWNCGCEWNRVCMGDHWFDV'
            }
        }
        time_stamp = now_utc()
        self.write_fasta(time_stamp)
        result = ss.fetch_ss_dis(self.temp_dir)
        self.assertEqual(expected, result)
        return None

    def tearDown(self):
        os.chdir(self.original_working_dir)
        try:
            shutil.rmtree(self.temp_dir)
        except OSError as err_args:
            msg = (
                "\nrmtree failed with an OSError "
                "while removing folder:\n"
                "\t\"{}\"\n"
                "Manually remove the path if necessary.\n"
                "The error details are:".format(
                    self.temp_dir
                )
            )
            for arg in err_args:
                msg = (
                    "{}\n"
                    "\t\"{}\"".format(msg, arg)
                )
            print(msg)
        return None


class TestSsFileValidator(unittest.TestCase):
    def setUp(self):
        # Create temp directory and store path.
        self.temp_dir = mkdtemp(prefix='pdb-tests_')
        self.original_working_dir = os.getcwd()
        os.chdir(self.temp_dir)

        # The test data directory should be located in
        # a directory below where this test file is located.
        file_path = os.path.abspath(__file__)
        this_dir = os.path.dirname(file_path)
        self.data_dir = os.path.join(this_dir, 'ss_test_data')
        return None

    def test_no_ss_files_pass(self):
        expected = {
            'files_to_archive': [],
            'valid_raw_file': None,
            'valid_json_file': None
        }
        result = ss._find_existing_files(self.temp_dir)
        self.assertEqual(expected, result)
        return None

    def test_single_json_file_pass(self):
        expected = {
            'files_to_archive': ['ss_dis.20150101T000000Z.json'],
            'valid_raw_file': None,
            'valid_json_file': None
        }
        open("ss_dis.20150101T000000Z.json", 'w', encoding='utf-8').close()
        result = ss._find_existing_files(self.temp_dir)
        self.assertEqual(expected, result)
        return None

    def test_multiple_with_valid_pair_pass(self):
        ss_files = [
            'ss_dis.20121101T020030Z.txt',
            'ss_dis.20131101T020030Z.txt',
            'ss_dis.20151101T020030Z.txt',
            'ss_dis.20151101T020030Z.json'
        ]
        for name in ss_files:
            ss_path = os.path.join(
                self.temp_dir,
                name
            )
            open(ss_path, 'w', encoding='utf-8').close()

        expected = {
            'files_to_archive': [
                'ss_dis.20131101T020030Z.txt',
                'ss_dis.20121101T020030Z.txt'],
            'valid_raw_file': 'ss_dis.20151101T020030Z.txt',
            'valid_json_file': 'ss_dis.20151101T020030Z.json'
        }
        result = ss._find_existing_files(self.temp_dir)
        self.assertEqual(expected, result)
        return None

    def test_multiple_with_single_txt_pass(self):
        ss_files = [
            'ss_dis.20131101T020030Z.txt',
            'ss_dis.20101101T020030Z.txt',
            'ss_dis.20141101T020030Z.json',
            'ss_dis.20151101T020030Z.json'
        ]
        for name in ss_files:
            ss_path = os.path.join(
                self.temp_dir,
                name
            )
            open(ss_path, 'w', encoding='utf-8').close()

        expected = {
            'files_to_archive': [
                'ss_dis.20141101T020030Z.json',
                'ss_dis.20131101T020030Z.txt',
                'ss_dis.20101101T020030Z.txt'],
            'valid_raw_file': 'ss_dis.20151101T020030Z.json',
            'valid_json_file': None
        }
        result = ss._find_existing_files(self.temp_dir)
        self.assertEqual(expected, result)
        return None

    def test_multiple_with_no_txt_pass(self):
        ss_files = [
            'ss_dis.20131101T020030Z.json',
            'ss_dis.20101101T020030Z.json',
            'ss_dis.20141101T020030Z.json',
            'ss_dis.20151101T020030Z.json'
        ]
        for name in ss_files:
            ss_path = os.path.join(
                self.temp_dir,
                name
            )
            open(ss_path, 'w', encoding='utf-8').close()

        expected = {
            'files_to_archive': [
                'ss_dis.20151101T020030Z.json',
                'ss_dis.20141101T020030Z.json',
                'ss_dis.20131101T020030Z.json',
                'ss_dis.20101101T020030Z.json'],
            'valid_raw_file': None,
            'valid_json_file': None
        }
        result = ss._find_existing_files(self.temp_dir)
        self.assertEqual(expected, result)
        return None

    def tearDown(self):
        os.chdir(self.original_working_dir)
        try:
            shutil.rmtree(self.temp_dir)
        except OSError as err_args:
            msg = (
                "\nrmtree failed with an OSError "
                "while removing folder:\n"
                "\t\"{}\"\n"
                "Manually remove the path if necessary.\n"
                "The error details are:".format(
                    self.temp_dir
                )
            )
            for arg in err_args:
                msg = (
                    "{}\n"
                    "\t\"{}\"".format(msg, arg)
                )
            print(msg)
        return None


class TestJson(unittest.TestCase):
    def setUp(self):
        # Create temp directory and store path.
        self.temp_dir = mkdtemp(prefix='pdb-tests_')
        self.original_working_dir = os.getcwd()
        os.chdir(self.temp_dir)

        # The test data directory should be located in
        # a directory below where this test file is located.
        file_path = os.path.abspath(__file__)
        this_dir = os.path.dirname(file_path)
        self.data_dir = os.path.join(this_dir, 'ss_test_data')

        return None

# TODO: Where are the json tests?

    def tearDown(self):
        os.chdir(self.original_working_dir)
        try:
            shutil.rmtree(self.temp_dir)
        except OSError as err_args:
            msg = (
                "\nrmtree failed with an OSError "
                "while removing folder:\n"
                "\t\"{}\"\n"
                "Manually remove the path if necessary.\n"
                "The error details are:".format(
                    self.temp_dir
                )
            )
            for arg in err_args:
                msg = (
                    "{}\n"
                    "\t\"{}\"".format(msg, arg)
                )
            print(msg)
        return None


if __name__ == '__main__':
    unittest.main()
