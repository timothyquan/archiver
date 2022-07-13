#!/usr/bin/env python3
import time
__author__ = "Tim Quan"
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Tim Quan"

import pandas as pd
import os
import sys
import shutil
import logging
from logging import handlers
logger = logging.getLogger(__name__)


def list_files(src_path, age_lmt, ignore_list, dst_path='', ):
    filelist = []
    for (path, directory, files) in os.walk(src_path):
        for file in files:

            age_in_days = (
                time.time() - os.stat(os.path.join(path, file)).st_mtime)/86400
            is_ignored = True in [ignore in os.path.join(
                path, file) for ignore in ignore_lst]

            if int(age_in_days) >= int(age_lmt) and not is_ignored:
               filelist.append([path, dst_path, path[len(src_path):], file])

            
    file_df = pd.DataFrame(data = filelist, columns=['source_path', 'destination_path', 'subdir', 'file_name'])
    return file_df


def move_file(row):
    source_file_path = os.path.join(row['source_path'], row['file_name'])
    destination_file_path = os.path.join(str(row['destination_path']) + str(row['subdir']),
                                         row['file_name'])

    logger.info(f'Creating path {destination_file_path}...')
    try:
        os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)
        logger.info('Created sucessfully.')
    except:
        logger.error(
            f'Creation failed: {os.path.dirname(destination_file_path)}.')

    logger.info(f'Moving: {source_file_path} to {destination_file_path}')
    try:
        shutil.move(source_file_path, destination_file_path)
        logger.info(f'Moved completed sucessfully.')

    except:
        logger.error(
            f'Move failed: {source_file_path} to {destination_file_path}')


def remove_empty_dirs(source_path, age_lmt):
    path_list = sorted([path for (path, directory, files)
                        in os.walk(source_path)], key=len, reverse=True)

    for path in path_list:
        is_old = int((time.time() - os.stat(path).st_mtime) /
                     86400) > int(age_lmt)
        # len(os.listdir(path)) returns 0 if the path is empty
        # path != source_path prevents deletion of the source path root
        if len(os.listdir(path)) == 0 and path != source_path and is_old:
            logger.info(f'Removing empty directory: {path}')
            try:
                os.rmdir(path)
                logger.info('Removed directory successfully.')
            except:
                logger.error(f'Removing directory failed: {path}')


def copy_file(row):
    source_file_path = os.path.join(row['source_path'], row['file_name'])
    destination_file_path = os.path.join(str(row['destination_path']) + str(row['subdir']),
                                         row['file_name'])

    logger.info(f'Creating path {destination_file_path}...')
    try:
        os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)
        logger.info('Created sucessfully.')
    except:
        logger.error(
            f'Creation failed: {os.path.dirname(destination_file_path)}.')

    logger.info('Copying: {} to {}'.format(
        source_file_path, destination_file_path))
    try:
        shutil.copy(source_file_path, destination_file_path)
        logger.info('Copy completed sucessfully.')

    except:
        logger.error(
            f'Copy failed: {source_file_path} to {destination_file_path}')


def delete_file(row):
    source_file_path = os.path.join(row['source_path'], row['file_name'])
    destination_file_path = os.path.join(str(row['destination_path']) + str(row['subdir']),
                                         row['file_name'])

    logger.info(f'Deleting: {source_file_path}')
    try:
        os.remove(source_file_path)
        logger.info('Delete completed sucessfully.')

    except:
        logger.error(
            f'Delete failed: {source_file_path}')


def get_logger(logger_name, log_path,  log_level):
    '''Function to configure and return a logger
    Accepts a logger_name, path, and logging level
    ('debug', 'info', 'warn', 'error', 'critical')'''

    log_levels = {'debug': logging.DEBUG,
                  'info': logging.INFO,
                  'warn': logging.WARN,
                  'error': logging.ERROR,
                  'critical': logging.CRITICAL
                  }

    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    log_file_handler = handlers.RotatingFileHandler(
        log_path, maxBytes=1048576, backupCount=5)
    log_file_handler.setFormatter(formatter)
    log_file_handler.setLevel(log_levels[log_level])

    log_console_handler = logging.StreamHandler(sys.stdout)
    log_console_handler.setFormatter(formatter)
    log_console_handler.setLevel(log_levels[log_level])

    logger.addHandler(log_file_handler)
    logger.addHandler(log_console_handler)
    logger.setLevel(log_levels[log_level])

    return logger


if __name__ == "__main__":
    if os.name == 'nt':
        log_path = f"{os.path.dirname(__file__)}\{os.path.basename(__file__)}".replace('.py', '.log')
    else:
        log_path = f"{os.path.dirname(__file__)}/{os.path.basename(__file__)}".replace('.py', '.log')


    action = sys.argv[1]
    age_lmt = sys.argv[2]
    src_path = sys.argv[3]
    dst_path = ''
    if action.lower() == 'delete':
        ignore_lst = [ig_str for ig_str in sys.argv[4:]]
    else:
        dst_path = sys.argv[4]
        ignore_lst = [ig_str for ig_str in sys.argv[5:]]

    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    logger = get_logger('archiver', log_path, 'debug')
    logger.info(
        '###############################################################')
    logger.info('Running archiver')
    logger.info(f'Action: {action}')
    logger.info(f'Age Limit: {age_lmt}')
    logger.info(f'Source Path {src_path}')
    if dst_path != '':
        logger.info(f'Destination Path: {dst_path}')
    logger.info(f'Ignore List: {ignore_lst}')
    logger.info(
        '###############################################################')

    # all files above the specified age in the source directory are accounted for in a dataframe
    # the appropriate function/action is applied against each row in the dataframe
    if action.lower() == 'copy':
        file_df = list_files(src_path, age_lmt, ignore_lst, dst_path=dst_path)
        file_df.apply(copy_file, axis=1)
    elif action.lower() == 'move':
        file_df = list_files(src_path, age_lmt, ignore_lst, dst_path=dst_path)
        file_df.apply(move_file, axis=1)
        remove_empty_dirs(src_path, age_lmt)
    elif action.lower() == 'delete':
        file_df = list_files(src_path, age_lmt, ignore_lst)
        file_df.apply(delete_file, axis=1)
        remove_empty_dirs(src_path, age_lmt)
