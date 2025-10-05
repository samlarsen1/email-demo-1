#!/bin/bash

# This script finds all .eml files under the 'examples' directory
# and runs the extract_html.py script on them, applying replacements.

# Define the directory to search for EML files
SEARCH_DIR="examples"
REPLACEMENTS_FILE="replacements.csv"

# Check if the replacements file exists
if [ ! -f "$REPLACEMENTS_FILE" ]; then
    echo "Error: Replacements file not found at '$REPLACEMENTS_FILE'"
    exit 1
fi

# Find all .eml files and loop through them
find "$SEARCH_DIR" -type f -name "*.eml" | while read -r eml_file; do
  # Create the output filename by replacing .eml with .html
  output_file="${eml_file%.eml}.html"

  echo "Processing '$eml_file' -> '$output_file'"

  # Run the Python script with the specified replacements
  python3 extract_html.py \
    -i "$eml_file" \
    -o "$output_file" \
    --replacements-file "$REPLACEMENTS_FILE"
done

echo "All EML files processed."
