__author__ = "Tim Quan"
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Tim Quan"

import pandas as pd
import os, sys
import shutil
import logging
import time


def list_files(source_path, destination_path, age_limit):
    file_df = pd.DataFrame()
    for (path,directory,files) in os.walk(source_path):        
        file_dict = {}
        for file in files:
            #if os.stat(os.path.join(path,file).st_mtime
            age_in_days = (time.time() - os.stat(os.path.join(path,file)).st_mtime)/86400
            if int(age_in_days) > int(age_limit):
                file_dict = {'source_path' : path, 
                    'destination_path' : destination_path,
                    'subdir' : path[len(source_path):],
                    'file_name' : file
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
        logging.error(f'Creation failed: {os.path.dirname(destination_file_path)}.')
    
    logging.info(f'Moving: {source_file_path} to {destination_file_path}')
    try: 
        shutil.move(source_file_path, destination_file_path)
        logging.info(f'Moved completed sucessfully.')

    except:
        logging.error(f'Move failed: {source_file_path} to {destination_file_path}')

def remove_empty_dirs(source_path):
    path_list = sorted([path for (path,directory,files) in os.walk(source_path)],key=len,reverse=True)

    for path in path_list:  
        if len(os.listdir(path) ) == 0 and path != source_path:
            logging.info(f'Removing empty directory: {path}')
            try:
                os.rmdir(path)
                logging.info('Removed directory successfully.')
            except:
                logging.error(f'Removing directory failed: {path}')
    

if __name__ == "__main__":
    #set up logging with console and file output
    src_path = sys.argv[1]
    dst_path = sys.argv[2]
    age_lmt = sys.argv[3]
    logging.basicConfig(level=logging.INFO, 
        format="%(asctime)s [%(levelname)s] %(message)s", 
        filename=os.path.join(dst_path, 'archiver.log'))
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger().addHandler(console)
    
    #files of the specified age are added to a dataframe, and the movefile function is executed against each row.
    file_df = list_files(src_path, dst_path,age_lmt)
    file_df.apply(move_file,axis=1)

    remove_empty_dirs(src_path)


