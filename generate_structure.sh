#!/bin/bash

# Function to recursively check folders and subfolders
check_folders() {
    local base_path="$1"
    local indent="$2"
    local skip_folders="$3"

    for item in "$base_path"/*; do
        local name=$(basename "$item")

        # Check if the folder should be skipped
        if [[ " $skip_folders " =~ " $name " ]]; then
            continue
        fi

        if [ -d "$item" ]; then
            echo "${indent}├── $name" >> folder_tree.txt
            check_folders "$item" "$indent│   " "$skip_folders"
        elif [ -f "$item" ]; then
            echo "${indent}├── $name (File)" >> folder_tree.txt
        fi
    done
}

# Get user input for the root folder
read -p "Enter the root folder path: " root_folder

# Check if the root folder exists
if [ ! -d "$root_folder" ]; then
    echo "Error: The specified folder does not exist."
    exit 1
fi

# Get user input for folders to skip
read -p "Enter folders to skip (space-separated): " skip_folders_input

# Convert input to an array
IFS=' ' read -r -a skip_folders_array <<< "$skip_folders_input"

# Initialize folder tree structure
echo "Folder Tree for: $root_folder" > folder_tree.txt
check_folders "$root_folder" "" "${skip_folders_array[@]}"

echo "Folder tree has been generated and saved to folder_tree.txt"

