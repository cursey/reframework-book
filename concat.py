import os
import glob

def concatenate_md_files(root_dir, output_file):
    all_md_content = ""

    # Walking through the root directory and all its subdirectories
    for folder_name, subfolders, filenames in os.walk(root_dir):
        for filename in glob.glob(os.path.join(folder_name, '*.md')):
            with open(filename, 'r', encoding='utf-8') as file:
                all_md_content += file.read() + "\n\n"  # Adding a newline between files

    # Writing the concatenated content to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(all_md_content)

# Usage
root_directory = 'src'  # Replace with the path to your directory
output_file = 'amalgamated_file.md'  # Name of the output file
concatenate_md_files(root_directory, output_file)
