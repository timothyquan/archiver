__author__ = "Tim Quan"
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Tim Quan"

import pandas as pd
import os
import sys
import shutil
import logging
import time


def list_files(src_path, age_lmt, ignore_list,dst_path='', ):
    file_df = pd.DataFrame()
    for (path, directory, files) in os.walk(src_path):
        file_dict = {}
        for file in files:
            age_in_days = (
                time.time() - os.stat(os.path.join(path, file)).st_mtime)/86400
            is_ignored = True in [ignore in os.path.join(
                path, file) for ignore in ignore_lst]
            if int(age_in_days) >= int(age_lmt) and not is_ignored:
                file_dict = {'source_path': path,
                             'destination_path': dst_path,
                             'subdir': path[len(src_path):],
                             'file_name': file
                             }
            if file_dict.__len__() != 0:
                file_df = file_df.append(file_dict, ignore_index=True)
    return file_df


def move_file(row):
    source_file_path = os.path.join(row['source_path'], row['file_name'])
    destination_file_path = os.path.join(str(row['destination_path']) + str(row['subdir']),
                                         row['file_name'])
    logging.info(f'Creating path {destination_file_path}...')
    try:
        os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)
        logging.info(f'Created sucessfully.')
    except:
        logging.error(
            f'Creation failed: {os.path.dirname(destination_file_path)}.')

    logging.info(f'Moving: {source_file_path} to {destination_file_path}')
    try:
        shutil.move(source_file_path, destination_file_path)
        logging.info(f'Moved completed sucessfully.')

    except:
        logging.error(
            f'Move failed: {source_file_path} to {destination_file_path}')


def remove_empty_dirs(source_path, age_lmt):
    path_list = sorted([path for (path, directory, files)
                        in os.walk(source_path)], key=len, reverse=True)
    for path in path_list:
        is_old = int((time.time() - os.stat(path).st_mtime) /
                     86400) > int(age_lmt)
        if len(os.listdir(path)) == 0 and path != source_path and is_old:
            logging.info(f'Removing empty directory: {path}')
            try:
                os.rmdir(path)
                logging.info('Removed directory successfully.')
            except:
                logging.error(f'Removing directory failed: {path}')


def copy_file(row):
    source_file_path = os.path.join(row['source_path'], row['file_name'])
    destination_file_path = os.path.join(str(row['destination_path']) + str(row['subdir']),
                                         row['file_name'])
    logging.info(f'Creating path {destination_file_path}...')
    try:
        os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)
        logging.info(f'Created sucessfully.')
    except:
        logging.error(
            f'Creation failed: {os.path.dirname(destination_file_path)}.')
    logging.info(f'Copying: {source_file_path} to {destination_file_path}')
    try:
        shutil.copy(source_file_path, destination_file_path)
        logging.info(f'Copy completed sucessfully.')

    except:
        logging.error(
            f'Copy failed: {source_file_path} to {destination_file_path}')

def delete_file(row):
    source_file_path = os.path.join(row['source_path'], row['file_name'])
    destination_file_path = os.path.join(str(row['destination_path']) + str(row['subdir']),
                                         row['file_name'])
    logging.info(f'Deleting: {source_file_path}')
    try:
        os.remove(source_file_path)
        logging.info('Delete completed sucessfully.')

    except:
        logging.error(
            f'Delete failed: {source_file_path}')


if __name__ == "__main__":
    action = sys.argv[1]
    age_lmt = sys.argv[2]    
    src_path = sys.argv[3]
    
    # set up logging with console and file output
    if action.lower() == 'delete':
        ignore_lst = [ig_str for ig_str in sys.argv[4:]]
        logpath = os.path.join(src_path, 'archiver.log')
    else:
        dst_path = sys.argv[4]
        ignore_lst = [ig_str for ig_str in sys.argv[5:]]
        logpath = os.path.join(dst_path, 'archiver.log')

    os.makedirs(os.path.dirname(logpath), exist_ok=True)

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(message)s",
                        filename=logpath)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger().addHandler(console)


    #all files above the specified age in the source directory are accounted for in a dataframe
    #the appropriate function/action is applied against each row in the dataframe
    if action.lower() == 'copy':
        file_df = list_files(src_path, age_lmt, ignore_lst, dst_path=dst_path)
        file_df.apply(copy_file, axis=1)
    elif action.lower() == 'move':
        file_df = list_files(src_path, age_lmt, ignore_lst,dst_path=dst_path)
        file_df.apply(move_file, axis=1)
        remove_empty_dirs(src_path, age_lmt)
    elif action.lower() == 'delete': 
        file_df = list_files(src_path, age_lmt, ignore_lst)
        file_df.apply(delete_file, axis=1)
        remove_empty_dirs(src_path, age_lmt)

