import os
import shutil
import zipfile


def find_files_by_names_and_extentions(path, name_strs, extentions):
    """
    find_file_by_name
    Args:
        path (str): path
        name_strs (list of str): list of name string to match
        extentions (list of str): list of file extention. 
        name_strs lenght should match extentions lenght.
        If extention of a particular file is irrelevant, 
        provide None as a value for this file.
    """
    out_filepaths = []

    assert len(name_strs) == len(extentions), f"Length of `name_strs`: {len(name_strs)}, and `extentions`: {len(extentions)}; provide same-lenght sequenses."

    for file in os.listdir(path):
        for name, extention in zip(name_strs, extentions):
            if name in file:
                if extention:
                    if file.endswith(extention):
                        out_filepaths.append(os.path.join(path, file))
                else:
                    out_filepaths.append(os.path.join(path, file))

    return  out_filepaths


def add_file_to_zip(zip_file, additional_file, target_subfolder):
    """
    Add a file to a ZIP archive within a specified subfolder.

    Parameters:
    - zip_file (ZipFile): The ZIP file to which the file will be added.
    - additional_file (str): The path to the file to be added.
    - target_subfolder (str): The name of the subfolder within the ZIP file.

    Returns:
    None
    """
    filename = os.path.basename(additional_file)
    target_path = os.path.join(target_subfolder, filename)
    zip_file.write(additional_file, arcname=target_path)


def find_folders(directory, folder_names):
    """
    Find paths of folders or subfolders with specific names in a given directory.

    Args:
        directory (str): Path to the directory to search.
        folder_names (list): List of folder names to search for.

    Returns:
        list: List of paths to the found folders.
    """
    found_folders = []

    for root, dirs, _ in os.walk(directory):
        for folder_name in folder_names:
            if folder_name in dirs:
                found_folder_path = os.path.join(root, folder_name)
                found_folders.append(found_folder_path)

    return found_folders


def process_folder(
        main_dir, 
        folders,
        secondary_folders,
        subfolder_name,
        main_dir_filenames,
        main_dir_extentions,
        secondary_dir, 
        secondary_dir_filenames, 
        secondary_dir_extentions, 
        output_folder,
        main_dir_folder_to_exclude=None,
        ):
    """
    Process folders in the main directory, creating ZIP archives with specified files.

    Parameters:
    - main_dir (str): The main directory containing the folders to process.
    - folders (list): List of folder names to process from the main directory.
    - secondary_folders (list): List of secondary folder names associated with each main folder.
    - subfolder_name (str): The name of the subfolder within each main folder to include in ZIP.
    - main_dir_filenames (list): List of main directory filenames to include in ZIP.
    - main_dir_extentions (list): List of main directory file extensions to include in ZIP.
    - secondary_dir (str): The directory containing additional files associated with each main folder.
    - secondary_dir_filenames (list): List of secondary directory filenames to include in ZIP.
    - secondary_dir_extentions (list): List of secondary directory file extensions to include in ZIP.
    - output_folder (str): The folder where the generated ZIP archives will be saved.
    - main_dir_folder_to_exclude (str, optional): A folder name in the main directory to exclude.

    Returns:
    None
    """
    
    for folder_name, secondary_folder_name in zip(folders, secondary_folders):
        folder_paths = find_folders(main_dir, folder_names=[folder_name])
        if main_dir_folder_to_exclude:
            folder_paths = [i for i in folder_paths if main_dir_folder_to_exclude not in i]
        try:
            folder_path = folder_paths[0]
        except IndexError:
            folder_path = 'None'
        try:
            secondary_folder_path = find_folders(secondary_dir, folder_names=[secondary_folder_name])[0]
        except IndexError:
            secondary_folder_path = 'None'
        

        if os.path.exists(folder_path):
            
            # Find main dir files
            main_files = find_files_by_names_and_extentions(
                path=folder_path, 
                name_strs=main_dir_filenames, 
                extentions=main_dir_extentions,
                )
            
            additional_files = []
            if os.path.exists(secondary_folder_path):
                # Find additional files 
                additional_files = find_files_by_names_and_extentions(
                    path=secondary_folder_path, 
                    name_strs=secondary_dir_filenames, 
                    extentions=secondary_dir_extentions,
                    )
            
            # Create a zip file
            zip_file_path = os.path.join(output_folder, f"{folder_name}.zip")
            with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
                # Add main dir files 
                for main_file in main_files:
                    zip_file.write(main_file, os.path.basename(main_file))
                
                # Add additional files 
                for additional_file in additional_files:
                    zip_file.write(additional_file, os.path.basename(additional_file))

                # Add files from a subfolder
                subfolder_path = os.path.join(folder_path, subfolder_name)
                if os.path.exists(subfolder_path):
                    for root, _, files in os.walk(subfolder_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            add_file_to_zip(zip_file, file_path, subfolder_name)
                else:
                    print(f"Did not find subfolder {subfolder_name} in {folder_path}")

            print(f"Saved {zip_file_path}")
