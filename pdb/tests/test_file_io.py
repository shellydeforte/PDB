# -*- coding: utf-8 -*-
"""Test lib.file_io."""
from __future__ import (
    absolute_import, division, print_function, unicode_literals)


import os
import shutil
import tempfile
import unittest
from os.path import exists

from pdb.lib.file_io import write_json, read_json


class TestJsonIO(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='pdb-tests_')

        # TODO: See github issue #22 for review of '/r' characters.
        self.ss_dis_dic = {
            '1A04_A': {
                'disorder': 'XXX------------------------------------------------------------------------\r------------------------------------------------------------------XXXXXXX--\r-----------------------------------------------------------------\r',
                'secstr': '     EEEEEE S HHHHHHHHHHHTT TTEEEEEEESSHHHHHHHHHHH  SEEEEETTSTTS HHHHHHHHHH\rS   SEEEEEE    HHHHHHHHHTT SEEEETT  HHHHHHHHHHHHHS     TTTHHHHHHH\r GGGS HHHHHHHHHHHTT  HHHHHHHHT  HHHHHHHHHHHHHHHT  SHHHHHHHHHHHT\r',
                'sequence': 'SNQEPATILLIDDHPMLRTGVKQLISMAPDITVVGEASNGEQGIELAESLDPDLILLDLNMPGMNGLETLDKLRE\rKSLSGRIVVFSVSNHEEDVVTALKRGADGYLLKDMEPEDLLKALHQAAAGEMVLSEALTPVLAASLRANRATTER\rDVNQLTPRERDILKLIAQGLPNKMIARRLDITESTVKVHVKHMLKKMKLKSRVEAAVWVHQERIF\r'},
            '1A4L_D': {
                'disorder': '---------------------------------------------------------------------------\r---------------------------------------------------------------------------\r---------------------------------------------------------------------------\r---------------------------------------------------------------------------\r-------------------------------------------------\r',
                'secstr': '  S  S EEEEEEEGGGS  HHHHHHHHHHHT   S SSHHHHHHHHS SS   HHHHHTTHHHHHHHHTT HHH\rHHHHHHHHHHHHHHTTEEEEEEEE SGGG  SS SS GGG    S  HHHHHHHHHHHHHHHHHHHS EEEEEEE\rEETT GGGHHHHHHHHHHTBTTTEEEEEEES TTSTTGGG HHHHHHHHHHHHTT EEEEEESSSS HHHHHHHH\rHTT  SEEEE GGGGGSHHHHHHHHHTT EEEE HHHHHHTT S TTS  HHHHHHHTT  EEE  B HHHHT\rHHHHHHHHHHSTT  HHHHHHHHHHHHHHSSS HHHHHHHHHHHHHH\r',
                'sequence': 'TPAFNKPKVELHVHLDGAIKPETILYFGKKRGIALPADTVEELRNIIGMDKPLSLPGFLAKFDYYMPVIAGCREA\rIKRIAYEFVEMKAKEGVVYVEVRYSPHLLANSKVDPMPWNQTEGDVTPDDVVDLVNQGLQEGEQAFGIKVRSILC\rCMRHQPSWSLEVLELCKKYNQKTVVAMDLAGDETIEGSSLFPGHVEAYEGAVKNGIHRTVHAGEVGSPEVVREAV\rDILKTERVGHGYHTIEDEALYNRLLKENMHFEVCPWSSYLTGAWDPKTTHAVVRFKNDKANYSLNTDDPLIFKST\rLDTDYQMTKKDMGFTEEEFKRLNINAAKSSFLPEEEKKELLERLYREYQ\r'},
            '173L_A': {
                'disorder': '---------------------------------------------------------------------------\r---------------------------------------------------------------------------\r------------XX\r',
                'secstr': '  HHHHHHHHT  EEEEEE TTS EEEETTEEEESSS HHHHHHHHHHHHTS  SSB  HHHHHHHHHHHHHHHH\rHHHTT TTTHHHHHHS HHHHHHHHHHHHHHHHHHHHT HHHHHHHHTT HHHHHHHHHTSHHHHHSHHHHHHHH\rHHHHH SSGGG\r',
                'sequence': 'MNIFEMLRIDEGLRLEIYKDTEGYYTIGIGHLLTKSPSLNAAKSELDKAIGRNCNGVITKDEAEKLFNQDVDAAV\rRGILRNAKLKPVYDSLDAVRRCALINMVFQMGETGVAGFTNSLEMLQQKRWDEAAVNLAESRWYNQTPNRAERVI\rTTFRTGTWDAYKNL\r'},
            '1A4L_A': {
                'disorder': '---------------------------------------------------------------------------\r---------------------------------------------------------------------------\r---------------------------------------------------------------------------\r---------------------------------------------------------------------------\r-------------------------------------------------\r',
                'secstr': '  S  S EEEEEEEGGGS  HHHHHHHHHHHT   S SSHHHHHHHHS SS   HHHHHTTHHHHHHHHTT HHH\rHHHHHHHHHHHHHTTTEEEEEEEE SGGG  SS SS GGG    S  HHHHHHHHHHHHHHHHHHHT EEEEEEE\rEETTBTTTHHHHHHHHHHTBTTTEEEEEEES TTSTTGGG HHHHHHHHHHHHTT EEEEEESSSS HHHHHHHH\rHTS  SEEEE GGGGGSHHHHHHHHHTT EEEE HHHHHHHSSS TTS  HHHHHHHTT EEEE  B HHHHT\rHHHHHHHHHHSTT  HHHHHHHHHHHHHTSSS HHHHHHHHHHHHHH\r',
                'sequence': 'TPAFNKPKVELHVHLDGAIKPETILYFGKKRGIALPADTVEELRNIIGMDKPLSLPGFLAKFDYYMPVIAGCREA\rIKRIAYEFVEMKAKEGVVYVEVRYSPHLLANSKVDPMPWNQTEGDVTPDDVVDLVNQGLQEGEQAFGIKVRSILC\rCMRHQPSWSLEVLELCKKYNQKTVVAMDLAGDETIEGSSLFPGHVEAYEGAVKNGIHRTVHAGEVGSPEVVREAV\rDILKTERVGHGYHTIEDEALYNRLLKENMHFEVCPWSSYLTGAWDPKTTHAVVRFKNDKANYSLNTDDPLIFKST\rLDTDYQMTKKDMGFTEEEFKRLNINAAKSSFLPEEEKKELLERLYREYQ\r'},
            '1A5J_A': {
                'disorder': '---------------------------------------------------------------------------\r-----------------------------------\r',
                'secstr': '   SS SS   HHHHHHHHHHHHHHTS  HHHHHHHS SS S S HHHHTS     SSSSS  HHHHHHHHTTTT\rTS S HHHHHHHSTT  HHHHHHHHHHTS  TT\r',
                'sequence': 'GIPDLVKGPWTKEEDQKVIELVKKYGTKQWTLIAKHLKGRLGKQCRERWHNHLNPEVKKSSWTEEEDRIIFEAHK\rVLGNRWAEIAKLLPGRTDNAVKNHWNSTIKRKVDT\r'},
            '1A4L_C': {
                'disorder': '---------------------------------------------------------------------------\r---------------------------------------------------------------------------\r---------------------------------------------------------------------------\r---------------------------------------------------------------------------\r-------------------------------------------------\r',
                'secstr': '  S  S EEEEEEEGGGS  HHHHHHHHHHHT   S SSHHHHHHHHS  S   HHHHHTTHHHHHHHHTT HHH\rHHHHHHHHHHHHHHHTEEEEEEEE GGGG SSS SS GGG    S  HHHHHHHHHHHHHHHHHHHT EEEEEEE\rEETTBHHHHHHHHHHHHHTBTTTEEEEEEES TTSTTGGG HHHHHHHHHHHHTT EEEEEESSSS HHHHHHHH\rHTS  SEEEE GGGGGSHHHHHHHHHTT EEEE HHHHHHTTSS TTS  HHHHHHHTT EEEE  B HHHHT\rHHHHHHHHHHSTT  HHHHHHHHHHHHHTSSS HHHHHHHHHHHHHH\r',
                'sequence': 'TPAFNKPKVELHVHLDGAIKPETILYFGKKRGIALPADTVEELRNIIGMDKPLSLPGFLAKFDYYMPVIAGCREA\rIKRIAYEFVEMKAKEGVVYVEVRYSPHLLANSKVDPMPWNQTEGDVTPDDVVDLVNQGLQEGEQAFGIKVRSILC\rCMRHQPSWSLEVLELCKKYNQKTVVAMDLAGDETIEGSSLFPGHVEAYEGAVKNGIHRTVHAGEVGSPEVVREAV\rDILKTERVGHGYHTIEDEALYNRLLKENMHFEVCPWSSYLTGAWDPKTTHAVVRFKNDKANYSLNTDDPLIFKST\rLDTDYQMTKKDMGFTEEEFKRLNINAAKSSFLPEEEKKELLERLYREYQ\r'},
            '1A4L_B': {
                'disorder': '---------------------------------------------------------------------------\r---------------------------------------------------------------------------\r---------------------------------------------------------------------------\r---------------------------------------------------------------------------\r-------------------------------------------------\r',
                'secstr': '  S  S EEEEEEEGGG   HHHHHHHHHHHT   S SSHHHHHHHHS SS   HHHHHHTHHHHHHHHTT HHH\rHHHHHHHHHHHHHHTTEEEEEEEE GGGG  SS SS GGG    S  HHHHHHHHHHHHHHHHHHHS EEEEEEE\rEETT GGGHHHHHHHHHHTBTTTEEEEEEES TTSTTGGG HHHHHHHHHHHHHT EEEEEESSSS HHHHHHHH\rHTS  SEEEE TTGGGSHHHHHHHHHTT EEEE HHHHHHTTSS TTS  HHHHHHHTT EEEE  B HHHHT\rHHHHHHHHHHTT   HHHHHHHHHHHHHTSS  HHHHHHHHHHHHHH\r',
                'sequence': 'TPAFNKPKVELHVHLDGAIKPETILYFGKKRGIALPADTVEELRNIIGMDKPLSLPGFLAKFDYYMPVIAGCREA\rIKRIAYEFVEMKAKEGVVYVEVRYSPHLLANSKVDPMPWNQTEGDVTPDDVVDLVNQGLQEGEQAFGIKVRSILC\rCMRHQPSWSLEVLELCKKYNQKTVVAMDLAGDETIEGSSLFPGHVEAYEGAVKNGIHRTVHAGEVGSPEVVREAV\rDILKTERVGHGYHTIEDEALYNRLLKENMHFEVCPWSSYLTGAWDPKTTHAVVRFKNDKANYSLNTDDPLIFKST\rLDTDYQMTKKDMGFTEEEFKRLNINAAKSSFLPEEEKKELLERLYREYQ\r'},
            '1A6P_B': {
                'disorder': '---------------------------------------------------------------------------\r-------------------\r',
                'secstr': ' EEEEETT  EEE  SS    TTEEEEEEEETTEEEEEEE S EESSTTEEE TTS EEESS  GGG EEEEEEE\rEETTS EEEEEEEEEEEE\r',
                'sequence': 'GTVWGALGHGINLNIPNFQMTDDIDEVRWERGSTLVAEFKRKPFLKSGAFEILANGDLKIKNLTRDDSGTYNVTV\rYSTNGTRILDKALDLRILE\r'},
            '1A6P_A': {
                'disorder': '---------------------------------------------------------------------------\r-------------------\r',
                'secstr': ' EEEEETT  EEE  TT    SSEEEEEEEETTEEEEEEE S EESSTTEEE TTS EEESS  GGG EEEEEEE\rEETTS EEEEEEEEEEEE\r',
                'sequence': 'GTVWGALGHGINLNIPNFQMTDDIDEVRWERGSTLVAEFKRKPFLKSGAFEILANGDLKIKNLTRDDSGTYNVTV\rYSTNGTRILDKALDLRILE\r'},
            '1A2A_C': {
                'disorder': '---------------------------------------------------------------------------\r-----------------------------------------------\r',
                'secstr': ' HHHHHHHHHHHHSS STTTTTSBTTTSSS   SS  SHHHHHHHHHHHHHHH TTS TTT    B  BTTB  B\r S  HHHHHHHHHHHHHHHHHHHHGGG  GGGBT  TTS  S\r',
                'sequence': 'NLLQFNKMIKEETGKNAIPFYAFYGCYCGGGGNGKPKDGTDRCCFVHDCCYGRLVNCNTKSDIYSYSLKEGYITC\rGKGTNCEEQICECDRVAAECFRRNLDTYNNGYMFYRDSKCTETSEEC\r'},
            '1A5H_B': {
                'disorder': '---------------------------------------------------------------------------\r---------------------------------------------------------------------------\r---------------------------------------------------------------------------\r---------------------------\r',
                'secstr': ' BSSEE  GGGSTTEEEEEEE TT   EEEEEEEEEEETTEEEE GGGGTT   GGGEEEEES SBSSS  TT E\rEEEEEEEEE TT  TTT TT  EEEEE  SSS  S   SS    B   TT    TT EEEEEESS SSTT S\rSB EEEEEEE  TTTSSGGGTTT    TTEEEEE    SSS SS  B  TT TT EEEEEETTEEEEEEEEEE S\rSSS TT  EEEEEGGGGHHHHHHH\r',
                'sequence': 'IKGGLFADIASHPWQAAIFAKHRRSPGERFLCGGILISSCWILSAAHCFQERFPPHHLTVILGRTYRVVPGEEEQ\rKFEVEKYIVHKEFDDDTYDNDIALLQLKSDSSRCAQESSVVRTVCLPPADLQLPDWTECELSGYGKHEALSPFYS\rERLKEAHVRLYPSSRCTSQHLLNRTVTDNMLCAGDTRSGGPQANLHDACQGDSGGPLVCLNDGRMTLVGIISWGL\rGCGQKDVPGVYTKVTNYLDWIRDNMRP\r'}
        }

    def test_json_read_write_success(self):
        ss_file_path = os.path.join(self.temp_dir, 'ss_dis.json')
        self.assertFalse(exists(ss_file_path))
        write_json(self.ss_dis_dic, ss_file_path)
        self.assertTrue(exists(ss_file_path))
        result = read_json(ss_file_path)
        self.assertEqual(self.ss_dis_dic, result)
        return None

    def tearDown(self):
        shutil.rmtree(self.temp_dir)


if __name__ == '__main__':
    unittest.main()
