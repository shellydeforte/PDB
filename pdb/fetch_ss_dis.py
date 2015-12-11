# -*- coding: utf-8 -*-
"""Return dictionary of secondary structure disorder.

Validate ss_dis data files. Download and/or regenerate if necessary.
Then return a dictionary of ss_dis data.

"""
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import filecmp
import os
import re
import requests
import shutil
import stat

from collections import namedtuple
from io import open

from pdb.lib.datetime_info import now_utc
from pdb.lib.file_io import read_json, write_json


__ss_dis_pattern__ = """
    ^          # Anchor to start of line.
    (ss_dis)   # Group 1: Match ss_dis

    \.         # A literal dot.

    (          # Start Group 2.
    \d{8}      # The year as eight digits (YYYYMMDD)
    T          # A literal 'T." (Time)
    \d{6}      # The time as six digits (HHmmss)
    Z          # A literal "Z." (Zulu, for UTC time.)
    )          # End Group 2.

    \.         # A literal dot.

    (          # Start Group 3.
    (?:txt)    # The extension "txt."
    |          # OR
    (?:json)   # The extension "json."
    )          # End Group 3.
    $          # Anchor to end of line.
"""
SS_DIS_PAT = re.compile(__ss_dis_pattern__, re.VERBOSE)

SS_File_Names = namedtuple('ss_dis_files', ['raw', 'json'])


def _find_ss_data(dir_path):
    """Return a list of ss_dis data files.

    Args:
        dir_path (Unicode): The directory path where ss_dis data resides.

    Returns:
        ss_dis_filepaths (list): A list of file paths in
            the directory that match the regex pattern for
            ss_dis filenames.

    """
    found_filepaths = [
        found
        for found in os.listdir(dir_path)
        if os.path.isfile(
            os.path.join(dir_path, found)
        )
        ]

    ss_dis_filepaths = [
        ss_dis_fp
        for ss_dis_fp in found_filepaths
        if SS_DIS_PAT.search(ss_dis_fp)
    ]
    return ss_dis_filepaths


def _make_backup_dir(parent_dir_path):
    """Create a backup folder in the specified directory path.

    Args:
        parent_dir_path (Unicode): The directory path where
            the backup folder will be created.

    Returns:
        None

    Raises:
        RuntimeError: The specified path must not be a file.

    """
    backup_dp = os.path.join(parent_dir_path, 'backup')
    if os.path.isdir(backup_dp):
        print(
            "Found and using backup directory."
        )
    else:
        if os.path.isfile(backup_dp):
            raise RuntimeError(
                "Can not create a backup directory in "
                "specified path because there is a file "
                "named \"backup\" in that directory."
                "Please rename or move the file."
            )
        print("Creating backup directory: \n"
              "\t{}\n".format(backup_dp))
        os.makedirs(backup_dp)
        assert os.path.isdir(backup_dp)
    return None


def _handle_readonly_file(file_path):
    try:
        os.chmod(file_path, stat.S_IWRITE)
        os.remove(file_path)
    except OSError as os_err:
        err_msg = (
            "Unable to delete archive the old ss_dis file."
            "You may wish to manually remove:\n"
            "\t{}\n"
            "The error details are:".format(
                file_path
            )
        )
        for arg in os_err.args:
            err_msg = (
                "{}\n"
                "\t\"{}\"".format(err_msg, arg)
            )
        print(err_msg)
        print("")
    else:
        assert not os.path.isfile(file_path)
    return None


def _archive_ss_data(original_file_path):
    """Move the file at the specified path to a backup directory.

    A backup directory will be created in the dirname() of the
        filepath if it does not already exist.

    Args:
        original_file_path (Unicode): The filepath to be moved.

    Returns:
        None

    """
    root_dp = os.path.dirname(original_file_path)
    backup_dp = os.path.join(root_dp, 'backup')
    if not os.path.isdir(backup_dp):
        _make_backup_dir(root_dp)
    assert os.path.isdir(backup_dp)
    assert os.path.isfile(original_file_path)

    archive_fp = os.path.join(
        backup_dp, os.path.basename(original_file_path)
    )
    shutil.copy(original_file_path, archive_fp)
    assert filecmp.cmp(original_file_path, archive_fp, shallow=0)
    assert os.path.isabs(original_file_path)

    try:
        os.remove(original_file_path)

    except OSError:
        _handle_readonly_file(original_file_path)

    else:
        assert not os.path.isfile(original_file_path)

    finally:
        assert os.path.isfile(archive_fp)

    return None


def _find_matching_datetime_pairs(sorted_dis_names):
    """Find a ss_dst json and text file with the same timestamp.

    The ss_dis.txt file from the PDB database isn't used directly; it
    is read, processed, and then turned into a dictionary.
    That dictionary, with modified data, is stored as a json file
    for future use.

    The ss_dis text file is kept to enable regeneration of the json
    file without downloading the data again. (This is also helpful
    for unit testing so that servers aren't overloaded.)

    To ensure consistency, the dictionary of modified ss_dis is never
    returned directly (which it could be after writing the json
    for the first time. Instead, the data is always read from the
    json file.

    Both the json and text file are written with a timestamp to
    assert that files belong to the same set of data.

    Args:
        sorted_dis_names (list): A list of ss_dis filenames (not path
            names) that have been found in the data directory.

    Returns:
        match_results (dict): A dictionary of file names with the
            following keys:

            valid_raw_file (Unicode):
                A ss_dis text file with a matching json file.
            valid_json_file (Unicode):
                A ss_dis json file with a matching txt (raw data) file.
            files_to_archive (list):
                A list of files names with no matching paris, or that
                are older than the valid_raw_file/valid_json_file,
                that should be moved to the backup directory.

    """
    sorted_dis_names = list(sorted_dis_names)
    match_results = {
        'valid_raw_file': None,
        'valid_json_file': None,
        'files_to_archive': []
    }
    while len(sorted_dis_names) >= 2:
        # For a ss_dis file, group 1 matches "ss_dis",
        #  group 2 matches the timestamp, and group 3 matches
        #  the file extension.
        first_date = SS_DIS_PAT.search(sorted_dis_names[0]).group(2)
        second_date = SS_DIS_PAT.search(sorted_dis_names[1]).group(2)

        first_extension = SS_DIS_PAT.search(sorted_dis_names[0]).group(3)
        second_extension = SS_DIS_PAT.search(sorted_dis_names[1]).group(3)
        extensions = (first_extension, second_extension)

        if not first_date == second_date:
            match_results['files_to_archive'].append(sorted_dis_names[0])
            sorted_dis_names.pop(0)
            continue

        if 'json' not in extensions or 'txt' not in extensions:
            match_results['files_to_archive'].append(sorted_dis_names[0])
            sorted_dis_names.pop(0)
            continue

        assert first_date == second_date
        assert first_extension != second_extension

        if first_extension == 'txt':
            match_results['valid_raw_file'] = sorted_dis_names.pop(0)
            # Reference the next file directly because we used pop().
            assert SS_DIS_PAT.search(sorted_dis_names[0]).group(3) == 'json'
            match_results['valid_json_file'] = sorted_dis_names.pop(0)
        elif first_extension == 'json':
            match_results['valid_json_file'] = sorted_dis_names.pop(0)
            # Reference the next file directly because we used pop().
            assert SS_DIS_PAT.search(sorted_dis_names[0]).group(3) == 'txt'
            match_results['valid_raw_file'] = sorted_dis_names.pop(0)
        else:
            raise RuntimeError("Unhandled case.")
        # Return only the most recent files as valid.
        break

    # Add any remaining (older) files to the list for archiving.
    if sorted_dis_names:
        match_results['files_to_archive'].extend(sorted_dis_names)

    # If two matching files haven't been found, return the most
    # recent raw txt file, if one exists.
    if not match_results['valid_raw_file']:
        assert not match_results['valid_json_file']
        match_results['files_to_archive'].sort(reverse=True)
        for archive_file in match_results['files_to_archive']:
            if SS_DIS_PAT.search(sorted_dis_names[0]).group(3) == 'txt':
                match_results['valid_raw_file'] = archive_file
                # Remove this file from the archive list
                # because it will now be used.
                match_results['files_to_archive'].remove(archive_file)
                break

    return match_results


def _new_filenames():
    """Create text and json filenames with matching timestamps.

    Returns:
        new_filenames (SS_Names): A named 2-tuple where raw is the
            filename of the new text file and json is the name
            of the matching (datetime) json file.

    """
    timestamp = now_utc()
    rfn = "{}.{}.{}".format(
        'ss_dis',
        timestamp,
        'txt'
    )
    yfn = "{}.{}.{}".format(
        'ss_dis',
        timestamp,
        'json'
    )
    new_filenames = SS_File_Names(raw=rfn, json=yfn)
    return new_filenames


def _download_ss_data(
        raw_file_path,
        url='http://www.rcsb.org/pdb/files/ss_dis.txt'):
    """Download ss_dis from the PDB servers.

    Args:
        raw_file_path (Unicode): The timestamped path name to for the data
            to be downloaded.

    Kwargs:
        url (Unicode): The current URL for ss_dis on the PDB servers.

    """
    ss_request = requests.get(url, stream=True)
    with open(raw_file_path, 'w', encoding='utf-8') as raw_fh:
        for chunk in ss_request.iter_content(
                chunk_size=None,
                decode_unicode=True):
            if chunk:  # Filter keep-alive chunks.
                raw_fh.write(chunk)
    ss_request.close()
    return None


def _generate_ss_dict(ss_raw_data_filepath):
    """Read ss_raw_data_filepath.txt into a dictionary and return.

    Process a ss_dis text file and return the modified
    data as a dictionary.

    Args:
        ss_raw_data_filepath (Unicode): The file path of the ss_dis file.

    Returns:
        pdb_dict (dict): A PDB dictionary in the following form:

            pdb_dict[pdb_chain] = {
                'sequence': '',
                'secstr': '',
                'disorder': ''
            }

    """
    pdb_dict = {}
    with open(ss_raw_data_filepath, 'r', encoding='utf-8') as raw_fh:
        ss_data = raw_fh.readlines()
        for line in ss_data:
            if line[0] == '>':
                header_info = line.split(':')
                pdb = header_info[0][1:].upper()
                chain = header_info[1]
                outer_key = ''.join([
                    pdb,
                    '_',
                    chain
                ])
                pdb_dict[outer_key] = {
                    'sequence': '',
                    'secstr': '',
                    'disorder': ''}
        # iterate through a second time and fill in
        seqstr = ''
        header_info = ss_data[0].split(':')
        pdb = header_info[0][1:].upper()
        chain = header_info[1]
        ltype = header_info[2].rstrip()
        len_ss_dis = len(ss_data)

        for i in range(1, len_ss_dis):
            line = ss_data[i]
            if line[0] == '>':
                outer_key = ''.join([
                    pdb.upper(),
                    '_',
                    chain
                ])
                pdb_dict[outer_key][ltype] = seqstr
                header_info = line.split(':')
                pdb = header_info[0][1:].upper()
                chain = header_info[1]
                ltype = header_info[2].rstrip()
                seqstr = ''
            else:
                seqstr += line.rstrip('\n')
            if i == len_ss_dis - 1:
                outer_key = ''.join([
                    pdb,
                    '_',
                    chain
                ])
                pdb_dict[outer_key][ltype] = seqstr

    return pdb_dict


def _find_existing_files(ss_dir_path):
    """Find any and all ss_dis file in the specified path.

    Both the json and text file are written with a timestamp to
    assert that files belong to the same set of data. Find the
    most current matching json/txt pair.

    Args:
        ss_dir_path (Unicode): The directory path where ss_dis
            data resides.

    Returns:
        validation_results (dict): A dictionary of file paths
            with the following keys:

                valid_raw_file (Unicode): Path to the
                    validated ss_dis.txt file.
                valid_json_file (Unicode): Path to the
                    validated ss_dis.json file.
                files_to_archive (list): A list of files
                    paths to be moved to the backup directory.

    """
    validation_results = {
        'valid_raw_file': None,
        'valid_json_file': None,
        'files_to_archive': []
    }
    dis_file_paths = _find_ss_data(ss_dir_path)

    if not dis_file_paths:
        pass

    # Use an existing raw data file, but archive if it's a json file.
    elif len(dis_file_paths) == 1:
        this_file = dis_file_paths[0]
        this_extension = SS_DIS_PAT.search(this_file).group(3)
        if this_extension == 'txt':
            validation_results['valid_raw_file'] = this_file
        else:
            assert this_extension == 'json'
            validation_results['files_to_archive'].append(this_file)

    # Find the most recent matching (raw/json) pair and archive the rest.
    elif len(dis_file_paths) > 1:
        assert len(dis_file_paths) > 1
        dis_file_names = [
            os.path.basename(dis_file_path)
            for dis_file_path in dis_file_paths
            ]
        dis_file_names.sort(reverse=True)
        found = _find_matching_datetime_pairs(dis_file_names)

        # Add values from the dictionary by key name, instead of copying
        # the dictionary, to allow for possible future changes.
        if found['files_to_archive']:
            validation_results['files_to_archive'] = found['files_to_archive']
        if found['valid_raw_file']:
            validation_results['valid_raw_file'] = found['valid_raw_file']
        if found['valid_json_file']:
            validation_results['valid_json_file'] = found['valid_json_file']
    else:
        raise SyntaxError("Unhandled case.")

    return validation_results


def fetch_ss_dis(dir_path):
    """Return a processed dictionary for ss_dis data.

    Args:
        dir_path (Unicode): The dir path where ss_dis files are located.

    Returns:
        ss_dis_data (dict): A dictionary of processed ss_dis data.

    """
    working_path = os.path.abspath(dir_path)
    ss_dis_files = _find_existing_files(working_path)

    if ss_dis_files['files_to_archive']:
        for name_to_archive in ss_dis_files['files_to_archive']:
            path_to_archive = os.path.join(working_path, name_to_archive)
            _archive_ss_data(
                path_to_archive
            )

    if ss_dis_files['valid_raw_file']:
        valid_raw_fp = os.path.join(
            working_path, ss_dis_files['valid_raw_file']
        )
    else:
        valid_raw_fp = None

    if ss_dis_files['valid_json_file']:
        valid_json_fp = os.path.join(
            working_path, ss_dis_files['valid_json_file']
        )
    else:
        valid_json_fp = None

        # If we a valid pair exists, use the json to return a dictionary.
    if valid_raw_fp and valid_json_fp:
        assert os.path.isfile(valid_raw_fp)
        assert os.path.isfile(valid_json_fp)
        current_json_path = valid_json_fp

    # Generate a companion json file if a single raw file is found.
    elif valid_raw_fp:
        valid_raw_fn = os.path.basename(valid_raw_fp)
        assert not valid_json_fp
        this_timestamp = SS_DIS_PAT.search(valid_raw_fn).group(2)
        companion_json = "{}.{}.{}".format(
            'ss_dis',
            this_timestamp,
            'json'
        )
        companion_json_path = os.path.join(working_path, companion_json)
        ss_dict = _generate_ss_dict(valid_raw_fp)
        write_json(ss_dict, companion_json_path)
        current_json_path = companion_json_path

    # Download new data and generate json file.
    elif not (valid_raw_fp or valid_json_fp):
        new_names = _new_filenames()
        new_raw_path = os.path.join(working_path, new_names.raw)
        new_json_path = os.path.join(working_path, new_names.json)

        _download_ss_data(new_raw_path)
        ss_dict = _generate_ss_dict(new_raw_path)
        write_json(ss_dict, new_json_path)
        current_json_path = new_json_path

    elif valid_raw_fp and not valid_json_fp:
        raise RuntimeError("Should not have a JSON file without a TXT file.")

    else:
        raise RuntimeError("Unhandled case.")

    # Always return the ss_dis dictionary by reading the json
    # file to ensure consistency of future runs.
    ss_dis_data = read_json(current_json_path)

    return ss_dis_data
