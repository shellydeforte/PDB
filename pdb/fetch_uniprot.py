# -*- coding: utf-8 -*-
"""Download FASTA files for a list UniProt IDs."""
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import os

import pandas as pd
import requests
import time

from logging import getLogger
from io import open


from pdb.lib.create_delimiter import create_delimiter
from pdb.lib.data_paths import ProjectFolders
from pdb.lib.pdb_tools import read_pdb_chain_uniprot_uniIDs
from pdb.lib.progress_bar import ProgressBar


class UniProtFetcher(object):
    def __init__(self, dirs):
        assert isinstance(dirs, ProjectFolders)
        self.dirs = dirs

        self.missing = []
        self.obs = []
        self.pdb_seq_fp = None
        self.uni_list = None
        self.df = None
        self.uni_log = None
        self.session = None

        self._initialize()

    def _initialize(self):
        self.pdb_seq_fp = os.path.join(self.dirs.working, 'pdb_seq.tsv')
        self._initialize_logs()
        self._initial_dataframe()
        self._initialize_uniprot_list()
        self._initialize_http_session()
        return None

    def _initialize_uniprot_list(self):
        self.uni_list = read_pdb_chain_uniprot_uniIDs(self.df)
        return None

    def _initial_dataframe(self):
        self.df = pd.read_csv(
            self.pdb_seq_fp,
            sep='\t',
            index_col=0,
            keep_default_na=False,
            na_values=['NULL', 'N/A'])
        return None

    def _initialize_logs(self):
        self.uni_log = getLogger('uni_error_logger')
        return None

    def _initialize_http_session(self):
        self.session = requests.Session()
        self.session.mount(
            "http://",
            requests.adapters.HTTPAdapter(max_retries=3)
        )
        self.session.mount(
            "https://",
            requests.adapters.HTTPAdapter(max_retries=3)
        )
        return None

    def fetch_fasta_files(self):
        self._create_progress_bar()

        for uni_id in self.uni_list:
            fasta = None
            fasta_fn = ''.join([uni_id, '.fasta'])
            fasta_fp = os.path.join(self.dirs.uni_data, fasta_fn)

            if os.path.exists(fasta_fp):
                self._check_if_obsolete(fasta_fp, uni_id)
            else:
                fasta = self._download_uniprot(uni_id)
                time.sleep(.4)

            if fasta:
                self._write_fasta(fasta, fasta_fp)

            self.progress.inc()

        self._process_missing_and_obsolete()
        self._write_new_dataframe()

        return None

    def _create_progress_bar(self):
        uni_start_msg = (
            "Downloading FASTA files. This may take a while. "
            "There are {0} UniProt IDs.".format(len(self.uni_list)))
        self.progress = ProgressBar(
            len(self.uni_list),
            start_msg=uni_start_msg,
            end_msg="FASTA download complete.",
            approx_percentage=1
        )
        return None

    def _check_if_obsolete(self, fasta_fp, uni_id):
        with open(fasta_fp, 'r', encoding='utf-8') as existing_fh:
            if len(existing_fh.read()) == 0:
                self.obs.append(uni_id)
        return None

    def _download_uniprot(self, uni_id):
        """Download a FASTA file from UniProt

        Args:
            uni_id (Unicode): A single UniProt ID.

        Returns:
            result (dict): A dictionary with keys to indicate if a sequence
                was returned, if the UniProt ID is obsolete, or
                an error was encountered with the download as the
                data is missing.

        Raises:
            HTTPError: There is no file
            URLError: The server is down. An obsolete entry will not throw an
                error, but when the file is read, it will
                return an empty string.

        """
        response = None
        result = None
        uni_url = ("http://www.uniprot.org/uniprot/{}.fasta".format(uni_id))
        try:
            response = self.session.get(
                url=uni_url,
                timeout=5
            )

        except requests.exceptions.ConnectTimeout:
            self.missing.append(uni_id)
            self.uni_log.critical(
                "[Missing] Timed out while trying to connect to the server. "
                "Could not download fasta file. "
                "{} added to list of missing IDs.".format(uni_id)
            )

        except requests.exceptions.ConnectionError:
            self.missing.append(uni_id)
            self.uni_log.critical(
                "[Missing] Connection error attempting to "
                "download fasta file. (DNS failure, refused "
                "connection, etc.) "
                "{} added to list of missing IDs.".format(uni_id)
            )

        except requests.exceptions.HTTPError:
            self.missing.append(uni_id)
            self.uni_log.error(
                "[Missing] Received an invalid HTTP response. "
                "{} added to list of missing IDs.".format(uni_id)
            )

        except requests.exceptions.TooManyRedirects:
            self.missing.append(uni_id)
            self.uni_log.warning(
                "Redirect history was: {}".format(response.history)
            )
            self.uni_log.warning(
                "[Missing] Too many redirects while trying "
                "to download fasta file. "
                "{} added to list of missing IDs.".format(uni_id)
            )

        except requests.exceptions.ReadTimeout:
            self.missing.append(uni_id)
            self.uni_log.warning(
                "[Missing] Request timed out waiting for the server "
                "while trying to download fasta file. "
                "{} added to list of missing IDs.".format(uni_id)
            )

        else:
            if response.status_code == 200 and len(response.text) > 0:
                result = response.text
            elif response.status_code == 200 and len(response.text) == 0:
                self.obs.append(uni_id)
                self.uni_log.error(
                    "[Obsolete] Zero-length record and HTTP 200 OK. "
                    "{} added to list of obsolete IDs.".format(uni_id)
                )
            elif response.status_code == 404:
                self.obs.append(uni_id)
                self.uni_log.error(
                    "[Obsolete] Server returned HTTP 404 Not Found. "
                    "{} added to list of obsolete IDs.".format(uni_id)
                )
        return result

    @staticmethod
    def _write_fasta(response, fasta_fp):
        if response:
            with open(fasta_fp, 'w', encoding='utf-8') as new_fh:
                new_fh.write(response)
        return None

    def _process_missing_and_obsolete(self):
        if self.missing:
            self._log_missing()
            self._remove_missing()

        if self.obs:
            self._remove_obsolete()
        return None

    def _log_missing(self):
        log_missing = getLogger('missing_uni_logger')
        log_missing.error(
            'There are missing FASTA files for '
            'the following UniProt IDs. '
            'See pdb.log for more details.')
        for miss in self.missing:
            log_missing.error(miss)
        return None

    def _remove_obsolete(self):
        if self.obs:
            print(
                "Removing {0} obsolete entries "
                "from the DataFrame...".format(len(self.obs))
            )
            # TODO: Don't modify DataFrame in place.
            self.df = self.df[-self.df.SP_PRIMARY.isin(self.obs)]
        return None

    def _remove_missing(self):
        if self.obs:
            print(
                "Removing {0} missing entries "
                "from the DataFrame...".format(len(self.obs))
            )
            # TODO: Don't modify DataFrame in place.
            self.df = self.df[-self.df.SP_PRIMARY.isin(self.missing)]
        return None

    def _write_new_dataframe(self):
        delimiter = create_delimiter('\t')
        self.df.to_csv(self.pdb_seq_fp, sep=delimiter, encoding='utf-8')
        return None
