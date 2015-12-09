# -*- coding: utf-8 -*-
"""Initialize logging for the application."""
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import logging
import logging.config
import os

from pdb.lib.file_io import read_yaml
from pdb.lib.data_paths import find_home_dir


def _build_config_path(config_filename):
    """Return a path for the config that resides in this same directory."""
    file_path = os.path.abspath(__file__)
    this_dir = os.path.dirname(file_path)
    if not os.path.isabs(config_filename):
        parent_pre = os.path.join(this_dir, os.pardir)
        parent_fp = os.path.normpath(parent_pre)
        config_fp = os.path.join(parent_fp, config_filename)
    else:
        config_fp = config_filename
    if not os.path.exists(config_fp):
        raise IOError("Log configuration file does not exist.")
    return config_fp


def _create_logfile_path(log_file_name):
    """Create a path name for a log handler in user home."""
    home_dp = find_home_dir()
    log_path = os.path.join(home_dp, log_file_name)
    return log_path


def create_logger(config_file='logging_config.yaml'):
    """Setup logging configuration.

    Examples:
        write_log = logging.getLogger('pdb_app_logger')
        write_log.warning('A warning message in the application log.')

        msg = logging.getLogger('pdb_console_handler_logger')
        msg.info("Writing an information msg to the screen.")

        uni_log = logging.getLogger('uni_error_logger')
        uni_log.error("A UniProt download failed.")

        general_log = logging.getLogger('root')
        general_log.debug("Writing a message to the app log and the screen.")

    Args:
        config_file (Unicode): The logging configuration file.

    Returns:
        None

    """
    config_fp = _build_config_path(config_file)
    config = read_yaml(config_fp)
    handler_names = ['pdb_app_handler', 'uni_err_handler']
    for handler in handler_names:
        handler_log_name = config['handlers'][handler]['filename']
        handler_log_path = _create_logfile_path(handler_log_name)
        config['handlers'][handler]['filename'] = handler_log_path
    logging.config.dictConfig(config)
    return None
