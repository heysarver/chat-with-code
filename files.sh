#!/bin/bash

# Get the folder path from command line argument
folder_path=$1

# Get the comma separated list of file extensions from command line argument
file_extensions=$2

# Get the list of directory names to exclude from command line argument
exclude_directories=$3

# Loop through each file in the folder recursively
find "$folder_path" -type f | while read -r file; do
    # Get the file extension of the current file
    file_extension="${file##*.}"

    # Check if the file extension is in the comma separated list of file extensions
    if [[ ",$file_extensions," == *",$file_extension,"* ]]; then
        # Check if the file is not in any of the excluded directories
        if ! [[ "$file" == *"$exclude_directories"* ]]; then
            # Print the file path
            echo "$file:"
            echo ""
            # Print the content of the file
            cat "$file"
            
            # Print a separator
            echo "--------"
            echo ""
            echo ""
        fi
    fi
done
