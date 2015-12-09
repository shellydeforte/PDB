# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import os
import unittest

import pandas as pd
from pandas.util.testing import assert_frame_equal

import pdb.filtering_step_one
import pdb.filtering_step_two
import pdb.lib.create_pdb_intervals
import pdb.lib.pdb_tools
import pdb.lib.uni_tools
import pdb.pdb_composite
import pdb.tests.test_data as test_data


class TestFiltering(unittest.TestCase):
    def setUp(self):
        file_path = os.path.abspath(__file__)
        this_dir = os.path.dirname(file_path)
        self.uniprot_folder = os.path.join(this_dir, 'uniprot')

    def test_filter_pdb_chain_uniprot(self):
        """
        10GS, 109M deleted because obsolete
        108M, 109L deleted because not in x-ray
        106M deleted because interval too short
        105M deleted because -1
        104M deleted because intervals don't match
        10GS C deleted because only one chain for that UniProt
        """
        expected = pd.DataFrame(
            test_data.PDBParseData.filter_pdb_chain_uniprot_expected)
        obs = ['10GS', '109M']
        xray = ['102L', '103L', '11BG', '104L', '104M', '105M',
                '106M', '10GS', '109M', '3V47', '3V44']
        df = pd.DataFrame(test_data.PDBParseData.filter_pdb_chain_uniprot_input)
        result = pdb.filtering_step_one.filter_pdb_chain_uniprot(df, obs, xray)
        assert_frame_equal(expected, result)

    def test_add_pdbseq_to_df(self):
        """Remove 103L, 3V44, 3V47.

        Remove 103L, 3V44, 3V47 because they are absent from test_ss_dis.
        Checked the peptide sequence by hand.
        """
        expected = pd.DataFrame(
            test_data.PDBParseData.add_pdbseq_to_df_expected)
        expected.reset_index(inplace=True)
        del expected['index']
        expected.sort_index(axis=1, inplace=True)

        df = pd.DataFrame(test_data.PDBParseData.add_pdbseq_to_df_input)

        result = pdb.filtering_step_one.add_pdbseq_to_df(
            df,
            test_data.PDBParseData.ss_dis)
        result.reset_index(inplace=True)
        del result['index']
        result.sort_index(axis=1, inplace=True)
        assert_frame_equal(result, expected)

    def test_filter_single_pdb_chain_sep(self):
        expected = pd.DataFrame(
            test_data.PDBParseData.filter_single_pdb_chain_sep_expected
        )
        df = pd.DataFrame(
            test_data.PDBParseData.filter_single_pdb_chain_sep_input)
        result = pdb.lib.pdb_tools.filter_single(df)
        assert_frame_equal(expected, result)

    def test_filter_single_pdb_chain(self):
        expected = pd.DataFrame(
            test_data.PDBParseData.filter_single_pdb_chain_expected)
        expected.reset_index(inplace=True)
        del expected['index']
        df = pd.DataFrame(test_data.PDBParseData.filter_single_pdb_chain_input)
        result = pdb.lib.pdb_tools.filter_single(df)
        result.reset_index(inplace=True)
        del result['index']
        assert_frame_equal(expected, result)

    def test_compare_to_uni(self):
        """
        Remove all entries related to P00720,
        keep entries related to P00669.
        """
        expected = pd.DataFrame(test_data.PDBParseData.compare_to_uni_expected)
        expected.reset_index(inplace=True)
        del expected['index']
        expected.sort_index(axis=1, inplace=True)
        df = pd.DataFrame(test_data.PDBParseData.compare_to_uni_input)
        result = pdb.filtering_step_two.compare_to_uni(df, self.uniprot_folder)
        result.reset_index(inplace=True)
        del result['index']
        result.sort_index(axis=1, inplace=True)
        assert_frame_equal(expected, result)

    def test_read_pdb_chain_uniprot_uniIDs(self):
        expected = ['P00718', 'P00720', 'P00669', 'Q4G1L2', 'B3DIN1']
        df = pd.DataFrame(
            test_data.PDBParseData.read_pdb_chain_uniprot_uniIDs_input)
        result = pdb.lib.pdb_tools.read_pdb_chain_uniprot_uniIDs(df)
        self.assertEqual(expected.sort(), result.sort())


class TestPDBSeq(unittest.TestCase):
    def setUp(self):
        file_path = os.path.abspath(__file__)
        this_dir = os.path.dirname(file_path)
        self.uniprot_folder = os.path.join(this_dir, 'uniprot')

    def test_create_pdb_composite(self):
        expected = pd.DataFrame(
            test_data.PDBParseData.create_pdb_composite_expected)

        ss_dis = test_data.PDBParseData.ss_dis
        df = pd.DataFrame(test_data.PDBParseData.create_pdb_composite_input)
        result = pdb.pdb_composite.create_pdb_composite(
            df,
            ss_dis,
            self.uniprot_folder)

        expected_sort = expected.sort_values(
            by=['PDB_CHAIN', 'SEC_STRUCT', 'SP_PRIMARY']
        )
        expected_sort.reset_index(drop=True, inplace=True)
        result_sort = result.sort_values(
            by=['PDB_CHAIN', 'SEC_STRUCT', 'SP_PRIMARY']
        )
        result_sort.reset_index(drop=True, inplace=True)
        assert_frame_equal(expected_sort, result_sort)
        return None

    def test_create_pdb_struct(self):
        expected = '---------------------XXXXTTPPE----SSPHHHHHHHH---------------'
        ss = '     TT  EE   SS HHHHHHHHHHHT  TEEEEEEEE  SGGG    '
        disorder = 'XXXXX-------------------------------------------------------'
        intervals = [[[2, 10], [22, 30]], [[15, 25], [35, 45]]]
        uni_seq_len = 60
        result = pdb.pdb_composite._create_pdb_struct(
            intervals,
            disorder,
            ss,
            uni_seq_len
        )
        self.assertEqual(expected, result)

    def test_create_structure1(self):
        disorder = ("XX-------------------------------------------------------"
                    "---------------------------------------------------------"
                    "---------XXXXX-------------------------------------------"
                    "-------------------XXXXXXXXXXXXXXXXXXX-------------------"
                    "---------------------------------------------------------"
                    "---------------------------------------------------------"
                    "-----------------------XX")
        ss = ("     TT  EE   SS HHHHHHHHHHHT HHHHHHHHTT"
              "TTGGG  SS TTS TTHHHHHHHHHHHHHTSSS SEE  H"
              "HHHHHHHHH GGGGSSS   HHHHHHHHHHHHHHHT S S"
              "S          SS HHHHHHHHHHHHHTT  SHHHHHH E"
              "EEEEEEE TTT  EEEEEEEESSEEEE             "
              "          EEHHHHHHHHHS EE  TT  EEETTTTEE"
              "E  EEEEEEEE  SEEEEEEE EEE SS EEE    EE  "
              "SS EE GGGB  TTS   EEEEEEEEEEE TTSS EEEEE"
              "EE TTT  EEEEETTEEEE  GGGTSSTTEEEEEEEE  S"
              "GGG    ")
        correct_return = ("------------------------------"
                          "------------------------------"
                          "------------------------------"
                          "------------------------------"
                          "------------------------------"
                          "------------------------------"
                          "------------------------------"
                          "------------------------------"
                          "------------------------------"
                          "-------------------------PPPTT"
                          "PPEEPPPSSPHHHHHHHHHHHTPHHHHHHH"
                          "HTTTTGGGPPSSPTTSPTTHHHHHHHHHHH"
                          "HHTSSSPSEEPPHHHHHHHHHHPGGGGSSS"
                          "PPPHHHHHHHHHHHHHHHTPSPSSPPXXXX"
                          "XPPPSSPHHHHHHHHHHHHHTTPPSHHHHH"
                          "HPEEEEEEEEPTTTPPEEEEEEEESSEEEE"
                          "PPPXXXXXXX--------------------"
                          "------------------------------"
                          "------------------------------"
                          "------------------------------"
                          "------------------------------"
                          "------------------------------"
                          "------------------------------"
                          "------------------------------"
                          "------------------------------"
                          "--------------XXXXXXXXXXPEEHHH"
                          "HHHHHHSPEEPPTTPPEEETTTTEEEPPEE"
                          "EEEEEEPPSEEEEEEEPEEEPSSPEEEPPP"
                          "PEEPPSSPEEPGGGBPPTTSPPPEEEEEEE"
                          "EEEEPTTSSPEEEEEEEPTTTPPEEEEETT"
                          "EEEEPPGGGTSSTTEEEEEEEEPPSGGGPP"
                          "XX----------------------------"
                          "---")
        intervals = [((3, 197), (296, 490)), ((200, 367), (765, 932))]
        uni_seq_len = 963
        fun_return = pdb.pdb_composite._create_pdb_struct(
            intervals,
            disorder,
            ss,
            uni_seq_len
        )
        self.assertEqual(uni_seq_len, len(fun_return))
        self.assertEqual(correct_return, fun_return)

    def test_create_structure2(self):
        # 3GIY_A
        disorder = ("XXX--------------------------------------------"
                    "-----------------------------------------------"
                    "-----------------------------------------------"
                    "-----------------------------------------------"
                    "-----------------------------------------------"
                    "-----------------------------------------------"
                    "-----------------------------------------------"
                    "---------------------------XXXXXXXXXXXXXXXXXXXX"
                    "XXXX")
        ss = (
            '      SHHHHHHHHHHHS HHHHHHHH  STT HHHHHHHHGGGGEEE    S   SS B  EEETTEEESSSEEE   S GGGTSTTHHHHHHHHHHHHT  EEE TT '
            'SS HHHHHHH  S EEEEE  SSHHHHHHHHHHHHHTT  EEEEE S SS    HHHHHHT    TT   GGGTT   S  SSTTTHHHHHHT S   TT  HH'
            'HHHHHHHH  SEEEEEEE SHHHHHHHHHTT SEEEE  GGGTS TT   GGGTHHHHHHHH S EEE SS  SHHHHHHHHHTT S EEESHHHHHHHHHHHH'
            'HHHHHHHHHHHHHHHHHHHHHT  BGGG  GGGEEE                         '
        )
        correct_return = (
            '---------------------------------------------------------------------------------------------'
            '---------------------------------------------------------------------------------------------'
            '-----------------------------THHHHHHTPSPPPTTPPHHHHHHHHHHPPSEEEEEEEPSHHHHHHHHHTTPSEEEEPPGGGTSP'
            'TTPPPGGGTHHHHHHHHPSPEEEPSSPPSHHHHHHHHHTTPSPEEESHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHTPPBGGGPPGGGE'
            'EEPXXXXXXXXXXXXXXXXXX'
        )
        intervals = [((197, 374), (216, 393))]
        uni_seq_len = 393
        fun_return = pdb.pdb_composite._create_pdb_struct(
            intervals,
            disorder,
            ss,
            uni_seq_len)
        self.assertEqual(uni_seq_len, len(fun_return))
        self.assertEqual(correct_return, fun_return)


class TestUniStruct(unittest.TestCase):
    def setUp(self):
        self.uniprot_folder = 'uniprot/'
        self.testing_folder = '../test_data/parsing/'

    def test_eval_one_pos_struct(self):
        expected = 'X'
        one_pos_struct = ['X', 'X', 'P', '-']
        result = pdb.lib.uni_tools._eval_one_pos_struct(one_pos_struct)
        self.assertEqual(expected, result)
        expected = 'O'
        one_pos_struct = ['-', '-', 'P', '-']
        result = pdb.lib.uni_tools._eval_one_pos_struct(one_pos_struct)
        self.assertEqual(expected, result)
        expected = '-'
        one_pos_struct = ['-', '-', '-', '-', '-']
        result = pdb.lib.uni_tools._eval_one_pos_struct(one_pos_struct)
        self.assertEqual(expected, result)

    def test_uni_struct(self):
        expected = 'XXO-O'
        struct_list = [['X', 'P', 'H', '-', '-'], ['-', 'X', 'P', '-', 'H']]
        result = pdb.lib.uni_tools._uni_struct(struct_list)
        self.assertEqual(expected, result)

    def test_create_uni_struct(self):
        expected = pd.DataFrame(
            test_data.PDBParseData.create_uni_struct_expected)

        df = pd.DataFrame(test_data.PDBParseData.create_uni_struct_input)
        result = pdb.lib.uni_tools.create_uni_struct(df)

        expected_sort = expected.sort_values(
            by=['SP_PRIMARY', 'STRUCT']
        )
        expected_sort.reset_index(drop=True, inplace=True)
        result_sort = result.sort_values(
            by=['SP_PRIMARY', 'STRUCT']
        )
        result_sort.reset_index(drop=True, inplace=True)
        assert_frame_equal(expected_sort, result_sort)
        return None


class TestMissRegions(unittest.TestCase):

    def setUp(self):
        self.uniprot_folder = 'uniprot/'

    def test_find_indexes(self):
        expected = [(1, 4), (6, 7), (10, 12)]
        uni_struct = '-XXXPHX-HHXX'
        result = pdb.lib.create_pdb_intervals._find_indexes(uni_struct)
        self.assertEqual(expected, result)

    def test_create_intervals(self):
        expected = pd.DataFrame(
            test_data.PDBParseData.create_intervals_expected)
        expected.reset_index(inplace=True)
        del expected['index']
        expected.sort_index(axis=1, inplace=True)
        pdb_df = pd.DataFrame(test_data.PDBParseData.create_intervals_pdb_df)
        uni_df = pd.DataFrame(test_data.PDBParseData.create_intervals_uni_df)
        result = pdb.lib.create_pdb_intervals.create_intervals(pdb_df, uni_df)
        result.reset_index(inplace=True)
        del result['index']
        result.sort_index(axis=1, inplace=True)
        assert_frame_equal(expected, result)

    def test_qualifies(self):
        sis1 = ['XXX', 'XXP', '-XP']
        sis2 = ['XXX', 'XXX', 'XXX']
        sis3 = ['XXX', 'PPP', '-XP']
        sis4 = ['XPX', 'PPP', '-XP']
        sis5 = ['XXX', 'XXX', 'PPP']
        sis6 = ['XXX', 'PPP', '---']
        self.assertTrue(pdb.lib.create_pdb_intervals._qualifies(sis1), 2)
        self.assertTrue(pdb.lib.create_pdb_intervals._qualifies(sis2), 2)
        self.assertTrue(pdb.lib.create_pdb_intervals._qualifies(sis3), 2)
        self.assertTrue(pdb.lib.create_pdb_intervals._qualifies(sis4), 2)
        self.assertTrue(pdb.lib.create_pdb_intervals._qualifies(sis5), 2)
        self.assertFalse(pdb.lib.create_pdb_intervals._qualifies(sis6), 2)

    def test_is_conflict(self):
        sis1 = ['XXX', 'XXP', '-XP']
        sis2 = ['XXX', 'XXX', 'XXX']
        sis3 = ['XXX', 'PPP', '-XP']
        self.assertFalse(pdb.lib.create_pdb_intervals._is_conflict(sis1))
        self.assertFalse(pdb.lib.create_pdb_intervals._is_conflict(sis2))
        self.assertTrue(pdb.lib.create_pdb_intervals._is_conflict(sis3))

    def test_is_conserved(self):
        sis1 = ['XXX', 'XXP', '-XP']
        sis2 = ['XXX', 'XXX', 'XXX']
        sis3 = ['XXX', 'PPP', '-XP']
        sis4 = ['XPX', 'PPP', '-XP']
        self.assertFalse(pdb.lib.create_pdb_intervals._is_conserved(sis1))
        self.assertTrue(pdb.lib.create_pdb_intervals._is_conserved(sis2))
        self.assertFalse(pdb.lib.create_pdb_intervals._is_conserved(sis3))
        self.assertFalse(pdb.lib.create_pdb_intervals._is_conserved(sis4))

    def test_is_contained(self):
        sis1 = ['XXX', 'XXP', '-XP']
        sis2 = ['XXX', 'XXX', 'XXX']
        sis3 = ['XXX', 'PPP', '-XP']
        sis4 = ['XPX', 'PPP', '-XP']
        sis5 = ['XXX', 'XXX', 'PPP']
        sis6 = ['XXX', 'PPP', '---']
        self.assertTrue(pdb.lib.create_pdb_intervals._is_contained(sis1))
        self.assertTrue(pdb.lib.create_pdb_intervals._is_contained(sis2))
        self.assertTrue(pdb.lib.create_pdb_intervals._is_contained(sis3))
        self.assertFalse(pdb.lib.create_pdb_intervals._is_contained(sis4))
        self.assertTrue(pdb.lib.create_pdb_intervals._is_contained(sis5))
        self.assertTrue(pdb.lib.create_pdb_intervals._is_contained(sis6))

    def test_determine_dis_type(self):
        sis1 = ['XXX', 'XXP', '-XP']
        sis2 = ['XXX', 'XXX', 'XXX']
        sis3 = ['XXX', 'PPP', '-XP']
        sis4 = ['XPX', 'PPP', '-XP']
        sis5 = ['XXX', 'XXX', 'PPP']
        sis6 = ['XXX', 'PPP', '---']
        sis7 = ['XX-', 'PPX', '-X-']
        self.assertEqual(pdb.lib.create_pdb_intervals.determine_dis_type(sis1), 'contained')
        self.assertEqual(pdb.lib.create_pdb_intervals.determine_dis_type(sis2), 'conserved')
        self.assertEqual(pdb.lib.create_pdb_intervals.determine_dis_type(sis3), 'conflict')
        self.assertEqual(pdb.lib.create_pdb_intervals.determine_dis_type(sis4), 'conflict')
        self.assertEqual(pdb.lib.create_pdb_intervals.determine_dis_type(sis5), 'conflict')
        self.assertEqual(pdb.lib.create_pdb_intervals.determine_dis_type(sis6), 'conflict')
        self.assertEqual(pdb.lib.create_pdb_intervals.determine_dis_type(sis7), 'overlap')


if __name__ == '__main__':
    unittest.main()
