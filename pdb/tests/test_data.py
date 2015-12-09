# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

class PDBParseData:
    ss_dis = {
        '104L_B': {
            'disorder': '--------------------------------------------------------------------------------------------------------------------------------------------------------------------XX',
            'secstr': '  HHHHHHHHH   SB EE TTS EE TTT      SS  HHHHHHHHHHHS S  TTB  HHHHHHHHHHHHHHHHHHHHT TTHHHHHHHS SSHHHHHHHHHHHH HHHHHH HHHHHHHHTT TTHHHHHHTSSHHHHHS HHHHHHHHHHHS SGGGG   ',
            'sequence': 'MNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLNAAKSAAELDKAIGRNTNGVITKDEAEKLFNQDVDAAVRGILRNAKLKPVYDSLDAVRRAALINMVFQMGETGVAGFTNSLRMLQQKRWDEAAVNLAKSRWYNQTPNRAKRVITTFRTGTWDAYKNL'},
        '104L_A': {
            'disorder': '--------------------------------------------------------------------------------------------------------------------------------------------------------------------XX',
            'secstr': '  HHHHHHHHT   SB EE TTS EEETTTEEEE  TT  HHHHHHHHHHHHTS  TTB  HHHHHHHHHHHHHHHHHHHTT TTTHHHHHHS HHHHHHHHHHHHHHHHHHHHT HHHHHHTTTT HHHHHHHTTSSHHHHHSHHHHHHHHHHHHHSSSGGG   ',
            'sequence': 'MNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLNAAKSAAELDKAIGRNTNGVITKDEAEKLFNQDVDAAVRGILRNAKLKPVYDSLDAVRRAALINMVFQMGETGVAGFTNSLRMLQQKRWDEAAVNLAKSRWYNQTPNRAKRVITTFRTGTWDAYKNL'},
        '11BG_A': {
            'disorder': '----------------------------------------------------------------------------------------------------------------------------',
            'secstr': '   HHHHHHHHHB   SSTT GGGHHHHHHHHTT  SSS  SEEEEE S HHHHHGGGGSEEE  TTS S EEE SS EEEEEEEE TT BTTB  EEEEEEEE EEEEEETTTTEEEEEEEE ',
            'sequence': 'KESAAAKFERQHMDSGNSPSSSSNYCNLMMCCRKMTQGKCKPVNTFVHESLADVKAVCSQKKVTCKNGQTNCYQSKSTMRITDCRETGSSKYPNCAYKTTQVEKHIIVACGGKPSVPVHFDASV'},
        '11BG_B': {
            'disorder': '----------------------------------------------------------------------------------------------------------------------------',
            'secstr': '   HHHHHHHHHB TT  TT GGGHHHHHHHHTT SSSS  SEEEEE S HHHHHGGGGSEEE  SSS S EEE SS EEEEEEEE TT BTTB  EEEEEEEE EEEEEETTTTEEEEEEEE ',
            'sequence': 'KESAAAKFERQHMDSGNSPSSSSNYCNLMMCCRKMTQGKCKPVNTFVHESLADVKAVCSQKKVTCKNGQTNCYQSKSTMRITDCRETGSSKYPNCAYKTTQVEKHIIVACGGKPSVPVHFDASV'},
        '102L_A': {
              'disorder': '-------------------------------------------------------------------------------------------------------------------------------------------------------------------XX',
              'secstr': '  HHHHHHHHH  EEEEEE TTS EEEETTEEEESSS TTTHHHHHHHHHHTS  TTB  HHHHHHHHHHHHHHHHHHHHH TTHHHHHHHS HHHHHHHHHHHHHHHHHHHHT HHHHHHHHTT HHHHHHHHHSSHHHHHSHHHHHHHHHHHHHSSSGGG   ',
              'sequence': 'MNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLNAAAKSELDKAIGRNTNGVITKDEAEKLFNQDVDAAVRGILRNAKLKPVYDSLDAVRRAALINMVFQMGETGVAGFTNSLRMLQQKRWDEAAVNLAKSRWYNQTPNRAKRVITTFRTGTWDAYKNL'}}
    filter_pdb_chain_uniprot_input = {
        'CHAIN': {
            0: 'A', 1: 'A', 2: 'A', 3: 'A', 4: 'A', 5: 'B', 6: 'A',
            7: 'A', 8: 'B', 9: 'B', 10: 'A', 11: 'A',
            12: 'A', 13: 'A', 14: 'A', 15: 'A', 16: 'A', 17: 'B', 18: 'C',
            19: 'A', 20: 'A', 21: 'A', 22: 'A'},
        'PDB_BEG': {
            0: 1, 1: 41, 2: 1, 3: 41, 4: 1, 5: 1, 6: 1, 7: 45, 8: 1,
            9: 45, 10: 1, 11: 1, 12: 0, 13: 0, 14: 1,
            15: 0, 16: 1, 17: 1, 18: 1, 19: 22, 20: 343, 21: 22,
            22: 391},
        'SP_BEG': {
            0: 1, 1: 41, 2: 1, 3: 41, 4: 27, 5: 27, 6: 1, 7: 45, 8: 1,
            9: 45, 10: 2, 11: 2, 12: 1, 13: 1, 14: 1,
            15: 1, 16: 2, 17: 2, 18: 2, 19: 22, 20: 126, 21: 22,
            22: 126},
        'SP_END': {
            0: 40, 1: 164, 2: 40, 3: 164, 4: 150, 5: 150, 6: 44, 7: 164,
            8: 44, 9: 164, 10: 155, 11: 154, 12: 3,
            13: 154, 14: 164, 15: 154, 16: 210, 17: 210, 18: 210,
            19: 342, 20: 200, 21: 390, 22: 200},
        'RES_BEG': {
            0: 1, 1: 42, 2: 1, 3: 44, 4: 1, 5: 1, 6: 1, 7: 47, 8: 1,
            9: 47, 10: 1, 11: -1, 12: 1, 13: 1, 14: 1,
            15: 1, 16: 1, 17: 1, 18: 1, 19: 5, 20: 326, 21: 5, 22: 374},
        'PDB_END': {
            0: 40, 1: 164, 2: 40, 3: 164, 4: 124, 5: 124, 6: 44, 7: 164,
            8: 44, 9: 164, 10: 153, 11: 153,
            12: 153, 13: 153, 14: 164, 15: 153, 16: 209, 17: 209,
            18: 209, 19: 342, 20: 417, 21: 390, 22: 465},
        'SP_PRIMARY': {
            0: 'P00720', 1: 'P00720', 2: 'P00720', 3: 'P00720',
            4: 'P00669', 5: 'P00669', 6: 'P00720',
            7: 'P00720', 8: 'P00720', 9: 'P00720', 10: 'P02185',
            11: 'P02185', 12: 'P02185', 13: 'P02185',
            14: 'P00720', 15: 'P02185', 16: 'P09211', 17: 'P09211',
            18: 'P09212', 19: 'B3DIN1', 20: 'Q4G1L2',
            21: 'B3DIN1', 22: 'Q4G1L2'},
        'RES_END': {
            0: 40, 1: 165, 2: 40, 3: 167, 4: 124, 5: 124, 6: 44, 7: 166,
            8: 44, 9: 166, 10: 153, 11: 153, 12: 3,
            13: 154, 14: 164, 15: 154, 16: 209, 17: 209, 18: 209,
            19: 325, 20: 400, 21: 373, 22: 448},
        'PDB': {
            0: '102l', 1: '102l', 2: '103l', 3: '103l', 4: '11bg',
            5: '11bg', 6: '104l', 7: '104l', 8: '104l',
            9: '104l', 10: '104m', 11: '105m', 12: '106m', 13: '108m',
            14: '109l', 15: '109m', 16: '10gs',
            17: '10gs', 18: '10gs', 19: '3v44', 20: '3v44', 21: '3v47',
            22: '3v47'}
    }

    filter_pdb_chain_uniprot_expected = {
        'CHAIN': {
            0: 'A', 1: 'A', 2: 'A', 3: 'A', 4: 'A', 5: 'B', 6: 'A',
            7: 'A', 8: 'B', 9: 'B', 19: 'A', 20: 'A', 21: 'A', 22: 'A'},
        'SP_BEG': {
            0: 1, 1: 41, 2: 1, 3: 41, 4: 27, 5: 27, 6: 1, 7: 45, 8: 1,
            9: 45, 19: 22, 20: 126, 21: 22, 22: 126},
        'PDB': {
            0: '102L', 1: '102L', 2: '103L', 3: '103L', 4: '11BG',
            5: '11BG', 6: '104L', 7: '104L', 8: '104L', 9: '104L',
            19: '3V44', 20: '3V44', 21: '3V47', 22: '3V47'},
        'RES_BEG': {
            0: 1, 1: 42, 2: 1, 3: 44, 4: 1, 5: 1, 6: 1, 7: 47, 8: 1,
            9: 47, 19: 5, 20: 326, 21: 5, 22: 374},
        'SP_PRIMARY': {
            0: 'P00720', 1: 'P00720', 2: 'P00720', 3: 'P00720',
            4: 'P00669', 5: 'P00669', 6: 'P00720', 7: 'P00720',
            8: 'P00720', 9: 'P00720', 19: 'B3DIN1', 20: 'Q4G1L2',
            21: 'B3DIN1', 22: 'Q4G1L2'},
        'RES_END': {
            0: 40, 1: 165, 2: 40, 3: 167, 4: 124, 5: 124, 6: 44, 7: 166,
            8: 44, 9: 166, 19: 325, 20: 400, 21: 373, 22: 448},
        'SP_END': {
            0: 40, 1: 164, 2: 40, 3: 164, 4: 150, 5: 150, 6: 44, 7: 164,
            8: 44, 9: 164, 19: 342, 20: 200, 21: 390, 22: 200}
    }

    add_pdbseq_to_df_input = {
        'CHAIN': {
            0: 'A', 1: 'A', 2: 'A', 3: 'A', 4: 'A', 5: 'B', 6: 'A',
            7: 'A', 8: 'B', 9: 'B', 19: 'A', 20: 'A', 21: 'A', 22: 'A'},
        'SP_BEG': {
            0: 1, 1: 41, 2: 1, 3: 41, 4: 27, 5: 27, 6: 1, 7: 45, 8: 1,
            9: 45, 19: 22, 20: 126, 21: 22, 22: 126},
        'PDB': {
            0: '102L', 1: '102L', 2: '103L', 3: '103L', 4: '11BG',
            5: '11BG', 6: '104L', 7: '104L', 8: '104L', 9: '104L',
            19: '3V44', 20: '3V44', 21: '3V47', 22: '3V47'},
        'RES_BEG': {
            0: 1, 1: 42, 2: 1, 3: 44, 4: 1, 5: 1, 6: 1, 7: 47, 8: 1,
            9: 47, 19: 5, 20: 326, 21: 5, 22: 374},
        'SP_PRIMARY': {
            0: 'P00720', 1: 'P00720', 2: 'P00720', 3: 'P00720',
            4: 'P00669', 5: 'P00669', 6: 'P00720', 7: 'P00720',
            8: 'P00720', 9: 'P00720', 19: 'B3DIN1', 20: 'Q4G1L2',
            21: 'B3DIN1', 22: 'Q4G1L2'},
        'RES_END': {
            0: 40, 1: 165, 2: 40, 3: 167, 4: 124, 5: 124, 6: 44, 7: 166,
            8: 44, 9: 166, 19: 325, 20: 400, 21: 373, 22: 448},
        'SP_END': {
            0: 40, 1: 164, 2: 40, 3: 164, 4: 150, 5: 150, 6: 44, 7: 164,
            8: 44, 9: 164, 19: 342, 20: 200, 21: 390, 22: 200}
    }

    add_pdbseq_to_df_expected = {
        'PDB_SEQ': {
            0: 'MNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLN',
            1: 'AAKSELDKAIGRNTNGVITKDEAEKLFNQDVDAAVRGILRNAKLKPVYDSLDAVRRAALINMVFQMGETGVAGFTNSLRMLQQKRWDEAAVNLAKSRWYNQTPNRAKRVITTFRTGTWDAYKNL',
            2: 'KESAAAKFERQHMDSGNSPSSSSNYCNLMMCCRKMTQGKCKPVNTFVHESLADVKAVCSQKKVTCKNGQTNCYQSKSTMRITDCRETGSSKYPNCAYKTTQVEKHIIVACGGKPSVPVHFDASV',
            3: 'KESAAAKFERQHMDSGNSPSSSSNYCNLMMCCRKMTQGKCKPVNTFVHESLADVKAVCSQKKVTCKNGQTNCYQSKSTMRITDCRETGSSKYPNCAYKTTQVEKHIIVACGGKPSVPVHFDASV',
            4: 'MNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLNAAKS',
            5: 'ELDKAIGRNTNGVITKDEAEKLFNQDVDAAVRGILRNAKLKPVYDSLDAVRRAALINMVFQMGETGVAGFTNSLRMLQQKRWDEAAVNLAKSRWYNQTPNRAKRVITTFRTGTWDAYKNL',
            6: 'MNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLNAAKS',
            7: 'ELDKAIGRNTNGVITKDEAEKLFNQDVDAAVRGILRNAKLKPVYDSLDAVRRAALINMVFQMGETGVAGFTNSLRMLQQKRWDEAAVNLAKSRWYNQTPNRAKRVITTFRTGTWDAYKNL'},
        'CHAIN': {
            0: 'A', 1: 'A', 2: 'A', 3: 'B', 4: 'A', 5: 'A', 6: 'B',
            7: 'B'},
        'SP_BEG': {0: 1, 1: 41, 2: 27, 3: 27, 4: 1, 5: 45, 6: 1, 7: 45},
        'SP_END': {0: 40, 1: 164, 2: 150, 3: 150, 4: 44, 5: 164, 6: 44, 7: 164},
        'RES_BEG': {0: 1, 1: 42, 2: 1, 3: 1, 4: 1, 5: 47, 6: 1, 7: 47},
        'SP_PRIMARY': {
            0: 'P00720', 1: 'P00720', 2: 'P00669', 3: 'P00669',
            4: 'P00720', 5: 'P00720', 6: 'P00720', 7: 'P00720'},
        'RES_END': {
            0: 40, 1: 165, 2: 124, 3: 124, 4: 44, 5: 166, 6: 44,
            7: 166},
        'PDB': {
            0: '102L', 1: '102L', 2: '11BG', 3: '11BG', 4: '104L',
            5: '104L', 6: '104L', 7: '104L'}
    }

    filter_single_pdb_chain_sep_input = {
        'CHAIN': {
            0: 'A', 1: 'A', 2: 'A', 3: 'A', 4: 'A', 5: 'B', 6: 'A',
            7: 'A', 8: 'B', 9: 'B', 10: 'A', 11: 'A', 12: 'A', 13: 'A',
            14: 'A'},
        'SP_BEG': {
            0: 1, 1: 41, 2: 1, 3: 41, 4: 27, 5: 27, 6: 1, 7: 45, 8: 1,
            9: 45, 10: 22, 11: 126, 12: 22, 13: 126, 14: 1},
        'SP_END': {
            0: 40, 1: 164, 2: 40, 3: 164, 4: 150, 5: 150, 6: 44, 7: 164,
            8: 44, 9: 164, 10: 342, 11: 200, 12: 390, 13: 200, 14: 185},
        'RES_BEG': {
            0: 1, 1: 42, 2: 1, 3: 44, 4: 1, 5: 1, 6: 1, 7: 47, 8: 1,
            9: 47, 10: 5, 11: 326, 12: 5, 13: 374, 14: 1},
        'SP_PRIMARY': {
            0: 'P00720', 1: 'P00720', 2: 'P00720', 3: 'P00720',
            4: 'P00669', 5: 'P00669', 6: 'P00720', 7: 'P00720',
            8: 'P00720', 9: 'P00720', 10: 'B3DIN1', 11: 'Q4G1L2',
            12: 'B3DIN1', 13: 'Q4G1L2', 14: 'P00718'},
        'RES_END': {
            0: 40, 1: 165, 2: 40, 3: 167, 4: 124, 5: 124, 6: 44, 7: 166,
            8: 44, 9: 166, 10: 325, 11: 400, 12: 373, 13: 448, 14: 185},
        'PDB': {
            0: '102L', 1: '102L', 2: '103L', 3: '103L', 4: '11BG',
            5: '11BG', 6: '104L', 7: '104L', 8: '104L', 9: '104L',
            10: '3V44', 11: '3V44', 12: '3V47', 13: '3V47', 14: '154L'}
    }

    filter_single_pdb_chain_sep_expected = {
        'CHAIN': {
            0: 'A', 1: 'A', 2: 'A', 3: 'A', 4: 'A', 5: 'B', 6: 'A',
            7: 'A', 8: 'B', 9: 'B', 10: 'A', 11: 'A', 12: 'A', 13: 'A'},
        'SP_BEG': {
            0: 1, 1: 41, 2: 1, 3: 41, 4: 27, 5: 27, 6: 1, 7: 45, 8: 1,
            9: 45, 10: 22, 11: 126, 12: 22, 13: 126},
        'SP_END': {
            0: 40, 1: 164, 2: 40, 3: 164, 4: 150, 5: 150, 6: 44, 7: 164,
            8: 44, 9: 164, 10: 342, 11: 200, 12: 390, 13: 200},
        'RES_BEG': {
            0: 1, 1: 42, 2: 1, 3: 44, 4: 1, 5: 1, 6: 1, 7: 47, 8: 1,
            9: 47, 10: 5, 11: 326, 12: 5, 13: 374},
        'SP_PRIMARY': {
            0: 'P00720', 1: 'P00720', 2: 'P00720', 3: 'P00720',
            4: 'P00669', 5: 'P00669', 6: 'P00720', 7: 'P00720',
            8: 'P00720', 9: 'P00720', 10: 'B3DIN1', 11: 'Q4G1L2',
            12: 'B3DIN1', 13: 'Q4G1L2'},
        'RES_END': {
            0: 40, 1: 165, 2: 40, 3: 167, 4: 124, 5: 124, 6: 44, 7: 166,
            8: 44, 9: 166, 10: 325, 11: 400, 12: 373, 13: 448},
        'PDB': {
            0: '102L', 1: '102L', 2: '103L', 3: '103L', 4: '11BG',
            5: '11BG', 6: '104L', 7: '104L', 8: '104L', 9: '104L',
            10: '3V44', 11: '3V44', 12: '3V47', 13: '3V47'}
    }

    filter_single_pdb_chain_input = {
        'SP_PRIMARY': {0: 'P00720', 1: 'P00720', 2: 'P00669', 3: 'P00720'},
        'SEC_STRUCT': {
            0: 'PPHHHHHHHHTPPPSBPEEPTTSPEEETTTEEEEPPTTPPHHHHHHHHHHTSPPTTBPPHHHHHHHHHHHHHHHHHHHTTPTTTHHHHHHSPHHHHHHHHHHHHHHHHHHHHTPHHHHHHTTTTPHHHHHHHTTSSHHHHHSHHHHHHHHHHHHHSSSGGGPXX',
            1: 'PPHHHHHHHHHPPPSBPEEPTTSPEEPTTTPPPPPPSSPPHHHHHHHHHSPSPPTTBPPHHHHHHHHHHHHHHHHHHHHTPTTHHHHHHHSPSSHHHHHHHHHHHHPHHHHHHPHHHHHHHHTTPTTHHHHHHTSSHHHHHSPHHHHHHHHHHHSPSGGGGPXX',
            2: '-XXXPPPHHHHHHHHHBPPPSSTTPGGGHHHHHHHHTTPPSSSPPSEEEEEPSPHHHHHGGGGSEEEPPTTSPSPEEEPSSPEEEEEEEEPTTPBTTBPPEEEEEEEEPEEEEEETTTTXXXXXXXXP',
            3: 'PPHHHHHHHHHPPEEEEEEPTTSPEEEETTEEEESSSPTTHHHHHHHHHHTSPPTTBPPHHHHHHHHHHHHHHHHHHHHHPTTHHHHHHHSPHHHHHHHHHHHHHHHHHHHHTPHHHHHHHHTTPHHHHHHHHHSSHHHHHSHHHHHHHHHHHHHSSSGGGPXX'},
        'PDB_CHAIN': {0: '104L_A', 1: '104L_B', 2: '11BG_A', 3: '102L_A'}
    }

    filter_single_pdb_chain_expected = {
        'SP_PRIMARY': {0: 'P00720', 1: 'P00720', 2: 'P00720'}, 'SEC_STRUCT': {
            0: 'PPHHHHHHHHTPPPSBPEEPTTSPEEETTTEEEEPPTTPPHHHHHHHHHHTSPPTTBPPHHHHHHHHHHHHHHHHHHHTTPTTTHHHHHHSPHHHHHHHHHHHHHHHHHHHHTPHHHHHHTTTTPHHHHHHHTTSSHHHHHSHHHHHHHHHHHHHSSSGGGPXX',
            1: 'PPHHHHHHHHHPPPSBPEEPTTSPEEPTTTPPPPPPSSPPHHHHHHHHHSPSPPTTBPPHHHHHHHHHHHHHHHHHHHHTPTTHHHHHHHSPSSHHHHHHHHHHHHPHHHHHHPHHHHHHHHTTPTTHHHHHHTSSHHHHHSPHHHHHHHHHHHSPSGGGGPXX',
            2: 'PPHHHHHHHHHPPEEEEEEPTTSPEEEETTEEEESSSPTTHHHHHHHHHHTSPPTTBPPHHHHHHHHHHHHHHHHHHHHHPTTHHHHHHHSPHHHHHHHHHHHHHHHHHHHHTPHHHHHHHHTTPHHHHHHHHHSSHHHHHSHHHHHHHHHHHHHSSSGGGPXX'},
        'PDB_CHAIN': {0: '104L_A', 1: '104L_B', 2: '102L_A'}
    }

    compare_to_uni_input = {
        'PDB_SEQ': {0: 'MNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLN',
                    1: 'AAKSELDKAIGRNTNGVITKDEAEKLFNQDVDAAVRGILRNAKLKPVYDSLDAVRRAALINMVFQMGETGVAGFTNSLRMLQQKRWDEAAVNLAKSRWYNQTPNRAKRVITTFRTGTWDAYKNL',
                    2: 'KESAAAKFERQHMDSGNSPSSSSNYCNLMMCCRKMTQGKCKPVNTFVHESLADVKAVCSQKKVTCKNGQTNCYQSKSTMRITDCRETGSSKYPNCAYKTTQVEKHIIVACGGKPSVPVHFDASV',
                    3: 'KESAAAKFERQHMDSGNSPSSSSNYCNLMMCCRKMTQGKCKPVNTFVHESLADVKAVCSQKKVTCKNGQTNCYQSKSTMRITDCRETGSSKYPNCAYKTTQVEKHIIVACGGKPSVPVHFDASV',
                    4: 'MNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLNAAKS',
                    5: 'ELDKAIGRNTNGVITKDEAEKLFNQDVDAAVRGILRNAKLKPVYDSLDAVRRAALINMVFQMGETGVAGFTNSLRMLQQKRWDEAAVNLAKSRWYNQTPNRAKRVITTFRTGTWDAYKNL',
                    6: 'MNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLNAAKS',
                    7: 'ELDKAIGRNTNGVITKDEAEKLFNQDVDAAVRGILRNAKLKPVYDSLDAVRRAALINMVFQMGETGVAGFTNSLRMLQQKRWDEAAVNLAKSRWYNQTPNRAKRVITTFRTGTWDAYKNL'},
        'CHAIN': {
            0: 'A', 1: 'A', 2: 'A', 3: 'B', 4: 'A', 5: 'A', 6: 'B', 7: 'B'},
        'SP_BEG': {0: 1, 1: 41, 2: 27, 3: 27, 4: 1, 5: 45, 6: 1, 7: 45},
        'SP_END': {
            0: 40, 1: 164, 2: 150, 3: 150, 4: 44, 5: 164, 6: 44, 7: 164},
        'RES_BEG': {0: 1, 1: 42, 2: 1, 3: 1, 4: 1, 5: 47, 6: 1, 7: 47},
        'SP_PRIMARY': {
            0: 'P00720', 1: 'P00720', 2: 'P00669', 3: 'P00669',
            4: 'P00720', 5: 'P00720', 6: 'P00720', 7: 'P00720'},
        'RES_END': {
            0: 40, 1: 165, 2: 124, 3: 124, 4: 44, 5: 166, 6: 44,
            7: 166},
        'PDB': {
            0: '102L', 1: '102L', 2: '11BG', 3: '11BG', 4: '104L',
            5: '104L', 6: '104L', 7: '104L'}
    }

    compare_to_uni_expected = {
        'CHAIN': {0: 'A', 1: 'B'},
        'SP_BEG': {0: 27, 1: 27},
        'SP_END': {0: 150, 1: 150},
        'RES_BEG': {0: 1, 1: 1},
        'SP_PRIMARY': {0: 'P00669', 1: 'P00669'},
        'RES_END': {0: 124, 1: 124},
        'PDB': {0: '11BG', 1: '11BG'}
    }

    read_pdb_chain_uniprot_uniIDs_input = {
        'CHAIN': {
            0: 'A', 1: 'A', 2: 'A', 3: 'A', 4: 'A', 5: 'B', 6: 'A',
            7: 'A', 8: 'B', 9: 'B', 10: 'A', 11: 'A', 12: 'A', 13: 'A',
            14: 'A'},
        'SP_BEG': {
            0: 1, 1: 41, 2: 1, 3: 41, 4: 27, 5: 27, 6: 1, 7: 45, 8: 1,
            9: 45, 10: 22, 11: 126, 12: 22, 13: 126, 14: 1},
        'SP_END': {
            0: 40, 1: 164, 2: 40, 3: 164, 4: 150, 5: 150, 6: 44, 7: 164,
            8: 44, 9: 164, 10: 342, 11: 200, 12: 390, 13: 200, 14: 185},
        'RES_BEG': {
            0: 1, 1: 42, 2: 1, 3: 44, 4: 1, 5: 1, 6: 1, 7: 47, 8: 1,
            9: 47, 10: 5, 11: 326, 12: 5, 13: 374, 14: 1},
        'SP_PRIMARY': {
            0: 'P00720', 1: 'P00720', 2: 'P00720', 3: 'P00720',
            4: 'P00669', 5: 'P00669', 6: 'P00720', 7: 'P00720',
            8: 'P00720', 9: 'P00720', 10: 'B3DIN1', 11: 'Q4G1L2',
            12: 'B3DIN1', 13: 'Q4G1L2', 14: 'P00718'},
        'RES_END': {
            0: 40, 1: 165, 2: 40, 3: 167, 4: 124, 5: 124, 6: 44, 7: 166,
            8: 44, 9: 166, 10: 325, 11: 400, 12: 373, 13: 448, 14: 185},
        'PDB': {
            0: '102L', 1: '102L', 2: '103L', 3: '103L', 4: '11BG',
            5: '11BG', 6: '104L', 7: '104L', 8: '104L', 9: '104L',
            10: '3V44', 11: '3V44', 12: '3V47', 13: '3V47', 14: '154L'}
    }

    create_pdb_composite_input = {
        'PDB_SEQ': {
            0: 'MNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLN',
            1: 'AAKSELDKAIGRNTNGVITKDEAEKLFNQDVDAAVRGILRNAKLKPVYDSLDAVRRAALINMVFQMGETGVAGFTNSLRMLQQKRWDEAAVNLAKSRWYNQTPNRAKRVITTFRTGTWDAYKNL',
            2: 'KESAAAKFERQHMDSGNSPSSSSNYCNLMMCCRKMTQGKCKPVNTFVHESLADVKAVCSQKKVTCKNGQTNCYQSKSTMRITDCRETGSSKYPNCAYKTTQVEKHIIVACGGKPSVPVHFDASV',
            3: 'KESAAAKFERQHMDSGNSPSSSSNYCNLMMCCRKMTQGKCKPVNTFVHESLADVKAVCSQKKVTCKNGQTNCYQSKSTMRITDCRETGSSKYPNCAYKTTQVEKHIIVACGGKPSVPVHFDASV',
            4: 'MNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLNAAKS',
            5: 'ELDKAIGRNTNGVITKDEAEKLFNQDVDAAVRGILRNAKLKPVYDSLDAVRRAALINMVFQMGETGVAGFTNSLRMLQQKRWDEAAVNLAKSRWYNQTPNRAKRVITTFRTGTWDAYKNL',
            6: 'MNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLNAAKS',
            7: 'ELDKAIGRNTNGVITKDEAEKLFNQDVDAAVRGILRNAKLKPVYDSLDAVRRAALINMVFQMGETGVAGFTNSLRMLQQKRWDEAAVNLAKSRWYNQTPNRAKRVITTFRTGTWDAYKNL'},
        'CHAIN': {
            0: 'A', 1: 'A', 2: 'A', 3: 'B',
            4: 'A', 5: 'A', 6: 'B', 7: 'B'},
        'SP_BEG': {0: 1, 1: 41, 2: 27, 3: 27, 4: 1, 5: 45, 6: 1, 7: 45},
        'SP_END': {
            0: 40, 1: 164, 2: 150, 3: 150, 4: 44,
            5: 164, 6: 44, 7: 164},
        'RES_BEG': {0: 1, 1: 42, 2: 1, 3: 1, 4: 1, 5: 47, 6: 1, 7: 47},
        'SP_PRIMARY': {
            0: 'P00720', 1: 'P00720', 2: 'P00669', 3: 'P00669',
            4: 'P00720', 5: 'P00720', 6: 'P00720', 7: 'P00720'},
        'RES_END': {
            0: 40, 1: 165, 2: 124, 3: 124, 4: 44, 5: 166,
            6: 44, 7: 166},
        'PDB': {
            0: '102L', 1: '102L', 2: '11BG', 3: '11BG', 4: '104L',
            5: '104L', 6: '104L', 7: '104L'}
    }

    create_pdb_composite_expected = {
        'SP_PRIMARY': {
            0: 'P00720', 1: 'P00669', 2: 'P00720', 3: 'P00720',
            4: 'P00669'},
        'SEC_STRUCT': {
            0: 'PPHHHHHHHHHPPPSBPEEPTTSPEEPTTTPPPPPPSSPPHHHHHHHHHSPSPPTTBPPHHHHHHHHHHHHHHHHHHHHTPTTHHHHHHHSPSSHHHHHHHHHHHHPHHHHHHPHHHHHHHHTTPTTHHHHHHTSSHHHHHSPHHHHHHHHHHHSPSGGGGPXX',
            1: '--------------------------PPPHHHHHHHHHBPTTPPTTPGGGHHHHHHHHTTPSSSSPPSEEEEEPSPHHHHHGGGGSEEEPPSSSPSPEEEPSSPEEEEEEEEPTTPBTTBPPEEEEEEEEPEEEEEETTTTEEEEEEEEP',
            2: 'PPHHHHHHHHHPPEEEEEEPTTSPEEEETTEEEESSSPTTHHHHHHHHHHTSPPTTBPPHHHHHHHHHHHHHHHHHHHHHPTTHHHHHHHSPHHHHHHHHHHHHHHHHHHHHTPHHHHHHHHTTPHHHHHHHHHSSHHHHHSHHHHHHHHHHHHHSSSGGGPXX',
            3: 'PPHHHHHHHHTPPPSBPEEPTTSPEEETTTEEEEPPTTPPHHHHHHHHHHTSPPTTBPPHHHHHHHHHHHHHHHHHHHTTPTTTHHHHHHSPHHHHHHHHHHHHHHHHHHHHTPHHHHHHTTTTPHHHHHHHTTSSHHHHHSHHHHHHHHHHHHHSSSGGGPXX',
            4: '--------------------------PPPHHHHHHHHHBPPPSSTTPGGGHHHHHHHHTTPPSSSPPSEEEEEPSPHHHHHGGGGSEEEPPTTSPSPEEEPSSPEEEEEEEEPTTPBTTBPPEEEEEEEEPEEEEEETTTTEEEEEEEEP'},
        'PDB_CHAIN': {
            0: '104L_B', 1: '11BG_B', 2: '102L_A', 3: '104L_A',
            4: '11BG_A'}
    }

    create_uni_struct_input = {
        'SP_PRIMARY': {
            0: 'P00720', 1: 'P00669', 2: 'P00720',
            3: 'P00720', 4: 'P00669'},
        'SEC_STRUCT': {
            0: 'PPHHHHHHHHHPPPSBPEEPTTSPEEPTTTPPPPPPSSPPHHHHHHHHHSPSPPTTBPPHHHHHHHHHHHHHHHHHHHHTPTTHHHHHHHSPSSHHHHHHHHHHHHPHHHHHHPHHHHHHHHTTPTTHHHHHHTSSHHHHHSPHHHHHHHHHHHSPSGGGGPXX',
            1: '--------------------------PPPHHHHHHHHHBPTTPPTTPGGGHHHHHHHHTTPSSSSPPSEEEEEPSPHHHHHGGGGSEEEPPSSSPSPEEEPSSPEEEEEEEEPTTPBTTBPPEEEEEEEEPEEEEEETTTTEEEEEEEEP',
            2: 'PPHHHHHHHHHPPEEEEEEPTTSPEEEETTEEEESSSPTTHHHHHHHHHHTSPPTTBPPHHHHHHHHHHHHHHHHHHHHHPTTHHHHHHHSPHHHHHHHHHHHHHHHHHHHHTPHHHHHHHHTTPHHHHHHHHHSSHHHHHSHHHHHHHHHHHHHSSSGGGPXX',
            3: 'PPHHHHHHHHTPPPSBPEEPTTSPEEETTTEEEEPPTTPPHHHHHHHHHHTSPPTTBPPHHHHHHHHHHHHHHHHHHHTTPTTTHHHHHHSPHHHHHHHHHHHHHHHHHHHHTPHHHHHHTTTTPHHHHHHHTTSSHHHHHSHHHHHHHHHHHHHSSSGGGPXX',
            4: '--------------------------PPPHHHHHHHHHBPPPSSTTPGGGHHHHHHHHTTPPSSSPPSEEEEEPSPHHHHHGGGGSEEEPPTTSPSPEEEPSSPEEEEEEEEPTTPBTTBPPEEEEEEEEPEEEEEETTTTEEEEEEEEP'},
        'Unnamed: 0': {0: 0, 1: 1, 2: 2, 3: 3, 4: 4},
        'PDB_CHAIN': {
            0: '104L_B', 1: '11BG_B', 2: '102L_A',
            3: '104L_A', 4: '11BG_A'}
    }

    create_uni_struct_expected = {
        'SP_PRIMARY': {0: 'P00720', 1: 'P00669'},
        'STRUCT': {
            0: 'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOXX',
            1: '--------------------------OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO'}
    }

    create_intervals_pdb_df = {
        'SP_PRIMARY': {
            0: 'Q5SLQ0', 1: 'Q5SLQ0', 2: 'Q805F6', 3: 'Q5SLQ0',
            4: 'Q5SLQ0', 5: 'Q5SLQ0', 6: 'Q5SLQ0', 7: 'Q5SLQ0',
            8: 'Q5SLQ0', 9: 'Q5SLQ0', 10: 'Q5SLQ0', 11: 'Q5SLQ0',
            12: 'Q5SLQ0', 13: 'Q5SLQ0', 14: 'Q805F6', 15: 'Q5SLQ0',
            16: 'Q5SLQ0', 17: 'Q5SLQ0', 18: 'Q5SLQ0', 19: 'Q5SLQ0',
            20: 'Q5SLQ0', 21: 'Q5SLQ0', 22: 'Q5SLQ0', 23: 'Q5SLQ0',
            24: 'Q5SLQ0', 25: 'Q5SLQ0', 26: 'Q5SLQ0', 27: 'Q5SLQ0',
            28: 'Q5SLQ0', 29: 'Q5SLQ0', 30: 'Q5SLQ0', 31: 'Q5SLQ0',
            32: 'Q5SLQ0', 33: 'Q5SLQ0', 34: 'Q5SLQ0', 35: 'Q5SLQ0',
            36: 'Q5SLQ0', 37: 'Q5SLQ0', 38: 'Q5SLQ0', 39: 'Q5SLQ0',
            40: 'Q5SLQ0', 41: 'Q5SLQ0', 42: 'Q5SLQ0', 43: 'Q5SLQ0',
            44: 'Q5SLQ0', 45: 'Q5SLQ0', 46: 'Q5SLQ0', 47: 'Q5SLQ0',
            48: 'Q5SLQ0', 49: 'Q5SLQ0'},
        'SEC_STRUCT': {
            0: 'XXXXXXXXXXXXXXXXXXPPPTTTSSPSPPTTPTTPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHHTSSPSPPPEEPP',
            1: 'XXXXXXXXXXXXXXXPPPSPPHHHHSPSEETTPTTPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHHTSSPSPPPBPPP',
            2: '----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------XXXPPTTEETTTTEEPTTPSPSSSTTEETTEEPPTTPEEEPPSSSSPPEEPPSSPSSPPPPPXX-',
            3: '-XXXXXXXXXXXXXXPPPSPPTTTSSPSPPTTPTTPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHHTSSPSPPPEEPP',
            4: '------------------PPPSTTTSPSPPSSPTTPHHHHHHTBPTTPPBPPHHHHPPPHHHHHHHHHHHHHHHHTTSSPSPPPEEPP',
            5: 'XXXXXXXXXXXXXXXXXPPPPTTTTPPSEETTPSSPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHTTSSPSPPPEEPP',
            6: 'XXXXXXXXXXXXXXXXXXPPPGGGSPPSEESSPTTPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHTTSSPSPPPEEPP',
            7: 'XXXXXXXXXXXXXXXXXXPPPTTTSPPPEETTPSSPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHTTSSPSPPPEEPP',
            8: 'XXXXXXXXXXXXXXXPPPSPPTTTSSPPEETTPTTPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHTTSSPSPPPEEPP',
            9: '-XXXXXXXXXXXXXXPPPSPPTTTSSPSPPTTPTTPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHTTSSPSPPPEEPP',
            10: 'XXXXXXXXXXXXXXXPPPSPPTTTSSPSEESSPSSPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHTTSSPSPPPEEPP',
            11: 'XXXXXXXXXXXXXXXXXXPPPTTTSPPSEESSPSSPPTTTGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHTTSSPSPPPEEPP',
            12: 'XXXXXXXXXXXXXXXPPPSPPHHHHSPSPPTTPTTPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHTTSSPSPPPBPPP',
            13: 'XXXXXXXXXXXXXXXXXXPPPSTTSSPPEESSPSSPHHHHTTSSPSSSPPPPHHHHPPPHHHHHHHHHHHHHHHHHTSSPSPPPEEPP',
            14: '----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------XXXPPTTEETTTTEEPTTPSPSSSTTEETTEEPPTTPEEEPPPTTPPPEEPPSSPSSPPXXXXX-',
            15: 'XXXXXXXXXXXXXXXXXXPPPTTTSSPSPBSSPTTPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHTTSSPSPPPEEPP',
            16: 'XXXXXXXXXXXXXXXPPPSPPHHHHSSSEESSPSSPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHHTSSPSPPPEEPP',
            17: 'XXXXXXXXXXXXXXXPPPSPPTTTTSPSEESSPSSPHHHHHTTBPSSSPBPPHHHHTPPHHHHHHHHHHHHHHHHTTSSPSPPPBPPP',
            18: 'XXXXXXXXXXXXXXXXXXPPPTTSSSPSEESSPTTPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHTTSSPSPPPEEPP',
            19: 'XXXXXXXXXXXXXXXPPPSSPGGGGPPSPPTTPSSPHHHHHTTBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHTTSSPSPPPEEPP',
            20: '------------------PPPTTTTPSSEETTPTTPHHHHGGGBPTTPPBPPHHHHPPPHHHHHHHHHHHHHHHHTTSSPSPPPEEPP',
            21: 'XXXXXXXXXXXXXXXXXXPPPSTTSSPPEESSPSSPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHTTSSPSPPPBPPP',
            22: 'XXXXXXXXXXXXXXXPPPSPPTTTSSPPEETTPTTPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHTTSSPSPPPEEPP',
            23: '-XXXXXXXXXXXXXXPPPSPPTTTSSPPEETTPTTPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHHTSSPSPPPEEPP',
            24: '-XXXXXXXXXXXXXXPPPSPPTTTSSPPPPTTPTTPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHHTSSPSPPPEEPP',
            25: '------------------PPPHHHHPPPEETTPSSPHHHHGGGBPTTPPBPPHHHHPPPHHHHHHHHHHHHHHHHHTSSPSPPPPBPP',
            26: 'XXXXXXXXXXXXXXXXXXPPPSGGGPPSEESSPTTPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHTTSSPSPPPEEPP',
            27: 'XXXXXXXXXXXXXXXXXXPPPTTTSPPSPPSSPTTPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHTTSSPSPPPEEPP',
            28: 'XXXXXXXXXXXXXXXPPPSPPHHHHSPSEETTPTTPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHHTSSPSPPPEEPP',
            29: '-XXXXXXXXXXXXXXPPPSPPTTTSSPPEETTPTTPHHHHHTTBPSSSPBPPHHHHPPPTTHHHHHHHHHHHHHHTTSSPSPPPEEPP',
            30: 'XXXXXXXXXXXXXXXXXXPPPSTTSPPSPPSSPTTPHHHHHTTBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHTTSSPSPPPEEPP',
            31: 'XXXXXXXXXXXXXXXXXXPPPTTTSPPSEETTPTTPHHHHGGGBPSSSPBPPHHHHTPPHHHHHHHHHHHHHHHHTTSSPSPPPEEPP',
            32: 'XXXXXXXXXXXXXXXXXXPPPTTTSPPSPPSSPTTPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHTTSSPSPPPEEPP',
            33: 'XXXXXXXXXXXXXXXXXXPPPTTTSSPSEESSPSSPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHTTSSPSPPPEEPP',
            34: 'XXXXXXXXXXXXXXXXXXPPPTTTSPPSPPTTPTTPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHTTSSPSPPPBPPP',
            35: 'XXXXXXXXXXXXXXXPPPSPPTTTSSPPEETTPSSPPTTGGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHHTSSPSPPPEEPP',
            36: '------------------PPPTTTTPPPEETTPSSPHHHHGGGBPTTSPBPPHHHHPPPHHHHHHHHHHHHHHHHHTSSPSPPPEEPP',
            37: 'XXXXXXXXXXXXXXXXXXPPPSTTSPPSPPSSPSSPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHTTSSPSPPPEEPP',
            38: 'XXXXXXXXXXXXXXXPPPSPPTTTSSPSPBTTPSSPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHHTSSPSPPPEEPP',
            39: '-XXXXXXXXXXXXXXPPPSPPTTTSSPSEETTPTTPHHHHGGGBPSSSSBPPHHHHPPPTTHHHHHHHHHHHHHHHTSSPSPPPBPPP',
            40: 'XXXXXXXXXXXXXXXXXXPPPTTTSSPPPBTTPTTPHHHHGGGSPSSSPPPPTTTSPPPHHHHHHHHHHHHHHHHHTSSPSPPPEEPP',
            41: 'XXXXXXXXXXXXXXXPPPSPPTTTSSPPEETTPTTPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHTTSSPSPPPEEPP',
            42: 'XXXXXXXXXXXXXXXPPPSPPHHHHPPSEETTPTTPHHHHHTTBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHHTSSPSPPPEEPP',
            43: 'XXXXXXXXXXXXXXXXXXPPPTTTSPPSEESSPTTPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHTTSSPSPPPBPPP',
            44: 'XXXXXXXXXXXXXXXXXXPPPTTTTSPPPBTTPTTPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHHTSSPSPPPBPPP',
            45: 'XXXXXXXXXXXXXXXXXXPPPGGGSPPSPPSSPSSPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHTTSSPSPPPEEPP',
            46: 'XXXXXXXXXXXXXXXXXXPPPTTTSPPSEESSPTTPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHTTSSPSPPPBPPP',
            47: 'XXXXXXXXXXXXXXXPPPSSPHHHHSPSPPSSPSSPHHHHHTTBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHTTSSPSPPPBPPP',
            48: 'XXXXXXXXXXXXXXXXXXPPPTTTSPPSEETTPSSPHHHHGGGBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHTTSSPSPPPEEPP',
            49: 'XXXXXXXXXXXXXXXXXPPPPHHHHPPSEETTPSSPPHHHHTTBPSSSPBPPHHHHPPPHHHHHHHHHHHHHHHHTTSSPSPPPEEPP'},
        'PDB_CHAIN': {
            0: '4DV6_R', 1: '4LFB_R', 2: '3C05_B', 3: '2UU9_R',
            4: '4K0K_R', 5: '4DR6_R', 6: '4DR3_R', 7: '4NXM_R',
            8: '4LF7_R', 9: '2UUB_R', 10: '4LF5_R', 11: '4JI4_R',
            12: '4LF9_R', 13: '4JI8_R', 14: '3C05_D', 15: '4JI3_R',
            16: '4DR4_R', 17: '4LFC_R', 18: '4JI6_R', 19: '4JI1_R',
            20: '4JYA_R', 21: '4DV1_R', 22: '4OX9_R', 23: '2UUA_R',
            24: '2UUC_R', 25: '4JV5_R', 26: '4JI2_R', 27: '4DV4_R',
            28: '4DR5_R', 29: '2UXB_R', 30: '4DUZ_R', 31: '4DUY_R',
            32: '4DV7_R', 33: '4DV5_R', 34: '4DV3_R', 35: '4LF6_R',
            36: '4KHP_R', 37: '4DV0_R', 38: '4LF4_R', 39: '2UXD_R',
            40: '4JI5_R', 41: '4LF8_R', 42: '4DR2_R', 43: '4DV2_R',
            44: '4JI7_R', 45: '4DR1_R', 46: '4JI0_R', 47: '4LFA_R',
            48: '4NXN_R', 49: '4DR7_R'}
    }

    create_intervals_uni_df = {
        'SP_PRIMARY': {0: 'Q5SLQ0', 1: 'Q805F6'},
        'STRUCT': {
            0: 'XXXXXXXXXXXXXXXXXXOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO',
            1: '----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------XXXOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOXXXXX-'}
    }

    create_intervals_expected = {
        'SP_PRIMARY': {15401: 'Q805F6', 10068: 'Q5SLQ0'},
        'STRUCT': {
            15401: '----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------XXXOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOXXXXX-',
            10068: 'XXXXXXXXXXXXXXXXXXOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO'},
        'MISSING': {
            15401: [['conserved', (418, 421)], ['contained', (477, 482)]],
            10068: [['contained', (0, 18)]]}
    }


class ScoresData:
    uni_df = {
        'SP_PRIMARY': {
            0: 'P30615',
            139: 'P62805',
            102: 'Q8KRK5'
        },

        'STRUCT': {
            0: 'XOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOXXOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO',
            139: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOXXXXXXXXXXX',
            102: '----------XXXXXXXXXOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO'
        },

        'MISSING': {
            0: [
                ['conserved', (0, 1)],
                ['conflict', (95, 97)]
            ],
            139: [
                ['overlap', (0, 28)],
                ['conflict', (92, 103)]
            ],
            102: [
                ['conserved', (10, 19)]
            ]
        }
    }

    create_scores_dict_expected = {
        'iup_short': [
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 1, 1, 1, 1],

        'disordp_rna': [
            0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
            1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 1, 1],

        'esp_xray': [
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0],

        'disordp_dna': [
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

        'dynamine': [
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 1, 1, 1, 1, 1, 1],

        'anchor_def': [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0],

        'disordp_pro': [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        ],

        'morfpred': [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0
        ]
    }

    test_predictions_expected = {
        'anchor_def': {
            '-': 0.0,
            'contained': 0.0,
            'overlap': 0.0,
            'discarded': 0.0,
            'conserved': 0.0,
            'O': 0.0,
            'X': 0.0,
            'conflict': 0.0},

        'disordp_rna': {
            '-': 0.0,
            'contained': 0.0,
            'overlap': 18.0,
            'discarded': 0.0,
            'conserved': 0.0,
            'O': 41.0,
            'X': 20.0,
            'conflict': 2.0},

        'esp_xray': {
            '-': 10.0,
            'contained': 0.0,
            'overlap': 20.0,
            'discarded': 0.0,
            'conserved': 9.0,
            'O': 10.0,
            'X': 29.0,
            'conflict': 0.0},

        'morfpred': {
            '-': 0.0,
            'contained': 0.0,
            'overlap': 3.0,
            'discarded': 0.0,
            'conserved': 0.0,
            'O': 3.0,
            'X': 3.0,
            'conflict': 0.0},

        'iup_short': {
            '-': 10.0,
            'contained': 0.0,
            'overlap': 28.0,
            'discarded': 0.0,
            'conserved': 9.0,
            'O': 6.0,
            'X': 41.0,
            'conflict': 4.0},

        'disordp_dna': {
            '-': 0.0,
            'contained': 0.0,
            'overlap': 27.0,
            'discarded': 0.0,
            'conserved': 1.0,
            'O': 9.0,
            'X': 28.0,
            'conflict': 0.0},

        'total': {
            '-': 10.0,
            'contained': 0.0,
            'overlap': 28.0,
            'discarded': 0.0,
            'conserved': 9.0,
            'O': 106.0,
            'X': 48.0,
            'conflict': 11.0},

        'disordp_pro': {
            '-': 0.0,
            'contained': 0.0,
            'overlap': 0.0,
            'discarded': 0.0,
            'conserved': 0.0,
            'O': 0.0,
            'X': 0.0,
            'conflict': 0.0},

        'dynamine': {
            '-': 10.0,
            'contained': 0.0,
            'overlap': 17.0,
            'discarded': 0.0,
            'conserved': 9.0,
            'O': 9.0,
            'X': 32.0,
            'conflict': 6.0}
    }

    test_fill_data_expected = {
        'esp_xray-iup_short': {
            'conserved': 1.0,
            'contained': 0.0,
            'conflict': 0.63636363636363635,
            'overlap': 0.7142857142857143},

        'dynamine-esp_xray': {
            'conserved': 1.0,
            'contained': 0.0,
            'conflict': 0.45454545454545453,
            'overlap': 0.8928571428571429},

        'iup_short-dynamine': {
            'conserved': 1.0,
            'contained': 0.0,
            'conflict': 0.81818181818181823,
            'overlap': 0.6071428571428571}
    }


class UniData:
    P00720 = """\
>sp|P00720|ENLYS_BPT4 Endolysin OS=Enterobacteria phage T4 GN=E PE=1 SV=2
MNIFEMLRIDERLRLKIYKDTEGYYTIGIGHLLTKSPSLNAAKSELDKAIGRNCNGVITK
DEAEKLFNQDVDAAVRGILRNAKLKPVYDSLDAVRRCALINMVFQMGETGVAGFTNSLRM
LQQKRWDEAAVNLAKSIWYNQTPNRAKRVITTFRTGTWDAYKNL
"""

    P02185 = """\
>sp|P02185|MYG_PHYCD Myoglobin OS=Physeter catodon GN=MB PE=1 SV=2
MVLSEGEWQLVLHVWAKVEADVAGHGQDILIRLFKSHPETLEKFDRFKHLKTEAEMKASE
DLKKHGVTVLTALGAILKKKGHHEAELKPLAQSHATKHKIPIKYLEFISEAIIHVLHSRH
PGDFGADAQGAMNKALELFRKDIAAKYKELGYQG
"""


class TsvData:
    pdb_seq_tsv_valid = """\
\tPDB\tCHAIN\tSP_PRIMARY\tRES_BEG\tRES_END\tSP_BEG\tSP_END\tPDB_SEQ
0\t101M\tA\tP02185\t1\t154\t1\t154\tMVLSEGEWQLVLHVWAKVEADVAGHGQDILIRLFKSHPETLEKFDRVKHLKTEAEMKASEDLKKHGVTVLTALGAILKKKGHHEAELKPLAQSHATKHKIPIKYLEFISEAIIHVLHSRHPGNFGADAQGAMNKALELFRKDIAAKYKELGYQG
1\t102L\tA\tP00720\t1\t40\t1\t40\tMNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLN
2\t102L\tA\tP00720\t42\t165\t41\t164\tAAKSELDKAIGRNTNGVITKDEAEKLFNQDVDAAVRGILRNAKLKPVYDSLDAVRRAALINMVFQMGETGVAGFTNSLRMLQQKRWDEAAVNLAKSRWYNQTPNRAKRVITTFRTGTWDAYKNL
3\t102M\tA\tP02185\t1\t154\t1\t154\tMVLSEGEWQLVLHVWAKVEADVAGHGQDILIRLFKSHPETLEKFDRFKHLKTEAEMKASEDLKKAGVTVLTALGAILKKKGHHEAELKPLAQSHATKHKIPIKYLEFISEAIIHVLHSRHPGNFGADAQGAMNKALELFRKDIAAKYKELGYQG
4\t103L\tA\tP00720\t1\t40\t1\t40\tMNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLN
"""

    # github #25  Need one or two examples of obsolete proteins in pdb_seq.tsv
    # TODO: Replace entries 5 and 6 below with real ones.
    pdb_seq_tsv_with_obs = """\
\tPDB\tCHAIN\tSP_PRIMARY\tRES_BEG\tRES_END\tSP_BEG\tSP_END\tPDB_SEQ
0\t101M\tA\tP02185\t1\t154\t1\t154\tMVLSEGEWQLVLHVWAKVEADVAGHGQDILIRLFKSHPETLEKFDRVKHLKTEAEMKASEDLKKHGVTVLTALGAILKKKGHHEAELKPLAQSHATKHKIPIKYLEFISEAIIHVLHSRHPGNFGADAQGAMNKALELFRKDIAAKYKELGYQG
1\t102L\tA\tP00720\t1\t40\t1\t40\tMNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLN
2\t102L\tA\tP00720\t42\t165\t41\t164\tAAKSELDKAIGRNTNGVITKDEAEKLFNQDVDAAVRGILRNAKLKPVYDSLDAVRRAALINMVFQMGETGVAGFTNSLRMLQQKRWDEAAVNLAKSRWYNQTPNRAKRVITTFRTGTWDAYKNL
3\t102M\tA\tP02185\t1\t154\t1\t154\tMVLSEGEWQLVLHVWAKVEADVAGHGQDILIRLFKSHPETLEKFDRFKHLKTEAEMKASEDLKKAGVTVLTALGAILKKKGHHEAELKPLAQSHATKHKIPIKYLEFISEAIIHVLHSRHPGNFGADAQGAMNKALELFRKDIAAKYKELGYQG
4\t103L\tA\tP00720\t1\t40\t1\t40\tMNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLN
5\t104M\tA\tP45678\t1\t40\t1\t50\tNOTAVALIDPROTEINORSEQUENCE
6\t104L\tA\tP45678\t1\t40\t1\t60\tNOTAVALIDPROTEINORSEQUENCE
"""
