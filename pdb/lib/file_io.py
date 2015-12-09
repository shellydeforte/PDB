# -*- coding: utf-8 -*-
"""Read and write data files."""
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import json
import os
import yaml

from filecmp import cmp
from logging import getLogger
from os.path import isfile
from shutil import copy2
from sys import version_info

from pdb.lib.datetime_info import now_utc

PYTHON2 = version_info[0] == 2
PYTHON3 = version_info[0] == 3

if PYTHON2:
    from codecs import open
else:
    from io import open


def write_json(data, dst_path):
    """Write object as JSON to the destination path."""
    msg = getLogger('root')
    msg.info("START: Writing json file: {}".format(dst_path))
    with open(dst_path, 'w', encoding='utf-8') as json_fh:
        json.dump(data, json_fh, ensure_ascii=False, indent=4, sort_keys=True)
    assert isfile(dst_path)
    msg.info("COMPLETE: Finished witting json file: {}".format(dst_path))
    return None


def read_json(src_path):
    """Deserialize JSON from the specified to file path and return object."""
    msg = getLogger('root')
    msg.info("START: Reading json file: t{}".format(src_path))
    with open(src_path, 'r', encoding='utf-8') as read_json_fh:
        json_result = json.load(
            read_json_fh,
            encoding='utf-8'
        )
    msg.info("COMPLETE: Finished reading json file: {}".format(src_path))
    return json_result


def read_yaml(yaml_file):
    """Return data from a YAML file.

    Args:
        yaml_file (Unicode): The path to a YAML file.

    """
    with open(yaml_file, 'r', encoding='utf-8') as yaml_fh:
        ss_dict = yaml.load(yaml_fh)
    return ss_dict


def write_yaml(data, yaml_path, **yaml_params):
    """Write data to a yaml file.

    Serialize a python object into a YAML stream, using custom
    parameters if specified, and write the steam to the
    specified file path.

    Args:
        data (obj): The data to be written to a YAML file.
        yaml_path (Unicode): The path of the yaml file to be written.
        **yaml_params (dict):
            width (int): Line width.
            indent (int): Line indentation.
            canonical (bool):  YAML supports the need for scalar
                equality by requiring that every scalar tag
                must specify a mechanism for producing the
                canonical form of any formatted content.
            default_flow_style (bool): Use False to always serialize
                collections in the block style.

    Returns:
        None

    """
    default_params = {
        'width': 500,
        'indent': 4,
        'canonical': True,
        'default_flow_style': None
    }

    if yaml_params and PYTHON2:
        for k, v in yaml_params.viewitems():
            if k in default_params:
                default_params[k] = v
    elif yaml_params and PYTHON3:
        for k, v in yaml_params.items():
            if k in default_params:
                default_params[k] = v

    print(
        "Writing YAML file:\n"
        "\t{}".format(yaml_path)
    )
    with open(yaml_path, 'w', encoding='utf-8') as fh:
        yaml.dump(
            data,
            fh,
            **default_params
        )
    assert os.path.isfile(yaml_path)
    print("Finished writing YAML file:\n"
          "\t{}".format(yaml_path))
    return None


def backup_file(original_file_path):
    log_pdb = getLogger('pdb_app_logger')

    if not os.path.abspath(original_file_path):
        raise RuntimeError("Please pass an absolute file path.")

    name_segments = original_file_path.split('.')
    if len(name_segments) > 2:
        original_fn = ''.join(name_segments[:-1])
        extension = ''.join(
            ['.', name_segments[-1]]
        )
    elif len(name_segments) == 2:
        original_fn = name_segments[0]
        extension = ''.join(
            ['.', name_segments[1]]
        )
    else:
        assert len(name_segments) == 1
        original_fn = name_segments[0]
        extension = ''

    timestamp = now_utc()
    new_fn = ''.join([
        original_fn,
        '.',
        timestamp,
        extension

    ])
    new_fp = os.path.join(
        os.path.basename(original_file_path),
        new_fn
    )
    copy2(original_file_path, new_fp)
    assert isfile(new_fp)
    assert cmp(original_file_path, new_fp, shallow=False)
    log_pdb.info(
        "Created a backup of \'{}\' at the following location:\n"
        "\t{}".format(original_file_path, new_fp)
    )

    return None
