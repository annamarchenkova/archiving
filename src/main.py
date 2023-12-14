import os
from project_dirs import PROJECT_DIR, OUTPUT_DIR
from utils import (
    process_folder,
    read_config,
)

if __name__ == 'main':
    cnf = read_config(config_dir=PROJECT_DIR, config_name="config.yml")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
  
    process_folder(
        main_dir=cnf['main_dir'], 
        folders=cnf['folders'], 
        secondary_folders = cnf['secondary_folders'],
        subfolder_name=cnf['main_dir_filenames'],
        main_dir_filenames=cnf['main_dir'],
        main_dir_extentions=cnf['main_dir_extentions'],
        secondary_dir=cnf['secondary_dir'], 
        secondary_dir_filenames=cnf['secondary_dir_filenames'], 
        secondary_dir_extentions=cnf['secondary_dir_extentions'], 
        output_folder=cnf['output_folder'],
        main_dir_folder_to_exclude=cnf['main_dir_folder_to_exclude']
        )
  
