from PIL import Image
import os
import pathlib
import sys

directories = []
is_running = True
key = os.curdir

# Change the condition to your use-case of target directories,
# In this case, this is targeting folders with '_' prefix.
def initialize_target_directories(path:str):
    current_directory = pathlib.Path(path).absolute()
    for dir in os.listdir(current_directory):
        if dir.startswith('_') and os.path.isdir(dir):
            directories.append(dir)

def iterate_directory_files(path:str):
    current_directory = pathlib.Path(os.curdir).absolute()
    target_directory = pathlib.Path(path).absolute()
    joined_path = pathlib.Path.joinpath(current_directory, target_directory)

    index = 0
    iterable_items = os.listdir(joined_path)
    while index < len(iterable_items):
        current_file = pathlib.Path.joinpath(joined_path, iterable_items[index]).absolute()
        # Folder name for the optimized images,
        # reusing the _FOLDER_Name and returning folder_name. 
        folder_name = path[1:len(path)].lower()
        folder_absolute_path = pathlib.Path.joinpath(joined_path, folder_name).absolute()

        if not folder_absolute_path.exists():
            os.mkdir(folder_absolute_path)

        # Save file as new file in result folder in the current directory.
        if current_file.is_file():
            image = Image.open(current_file)
            splitted_file_info = iterable_items[index].split('.')
            file_name = splitted_file_info[0]
            file_extension = splitted_file_info[1]
            save_file_path = pathlib.Path.joinpath(joined_path, f'{folder_name}/{file_name}_{index}.{file_extension}').absolute()
            # print(save_file_path)
            image.save(save_file_path, optimize=True, quality=10)
        index += 1
        
        

if __name__ == '__main__':
    initialize_target_directories(os.curdir)

    for target_directory in directories:
        print(target_directory)
        iterate_directory_files(target_directory)
        
        ### CHECKING.
        # while is_running:
            # key = input('')
            # formatted_key = f'_{key.upper()}'

            # if key == 'x':
            #     print('Exiting loop')
            #     is_running = False
            # elif directories.__contains__(formatted_key):
            #     iterate_directory_files(formatted_key)
