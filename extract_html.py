#!/usr/bin/env python3
import re
import base64
import argparse
import os
import csv


def extract_base64_html(eml_file):
    """Extracts base64 encoded HTML content from an EML file."""
    try:
        with open(eml_file, 'rb') as f:
            eml_content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {eml_file}")
        return None

    # Pattern to find the base64 encoded HTML
    pattern = re.compile(
        b'''Content-Type: text/html; charset=(?:")?utf-8(?:")?\r\n'''
        b'''(?:Content-Id: .*?\r\n)?'''
        b'''Content-Transfer-Encoding: base64\r\n'''
        b'''\r\n'''
        b'''(.*?)--''',
        re.DOTALL  # DOTALL allows . to match newline characters
    )
    match = pattern.search(eml_content)

    if match:
        # The matched group will contain the base64 content.
        return match.group(1).strip()
    else:
        return None


def replace_in_html(html_content, replacements):
    """Replaces multiple patterns in the HTML content."""
    for pattern, replacement in replacements.items():
        html_content = html_content.replace(pattern, replacement)
    return html_content


def decode_and_save_html(base64_html, html_file, replacements=None):
    """Decodes the base64 HTML content, performs replacements, and saves it to a file."""
    try:
        decoded_html = base64.b64decode(base64_html).decode('utf-8')
    except base64.binascii.Error:
        print("Error: Invalid base64 string.")
        return
    if replacements:
        decoded_html = replace_in_html(decoded_html, replacements)

    try:
        with open(html_file, 'w') as f:
            f.write(decoded_html)
        print(f"HTML content saved to {html_file}")
    except Exception as e:
        print(f"Error writing to file: {e}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Extract HTML content from an EML file.")
    parser.add_argument("-i","--input",  help="The path to the EML file.")
    parser.add_argument("-o", "--output", help="The path to the output HTML file.")
    parser.add_argument("-r", "--replace", nargs=2, action="append", help="A key-value pair to replace (e.g., -r 'find_this' 'replace_with_this'). Can be used multiple times.")
    parser.add_argument("--replacements-file", help="Path to a CSV file with key-value pairs for replacement.")
    args = parser.parse_args()

    if not args.input:
        parser.print_help()
        exit(1)
    eml_file = args.input

    if args.output:
        html_file = args.output
    else:
        html_file = os.path.splitext(args.input)[0] + ".html"

    # The open() function is relative to the CWD by default.
    # We can pass the path directly.
    # Build replacements dictionary
    replacements = {}
    if args.replacements_file:
        try:
            with open(args.replacements_file, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) == 2:
                        replacements[row[0]] = row[1]
        except FileNotFoundError:
            print(f"Error: Replacements file not found: {args.replacements_file}")
    if args.replace:
        for old, new in args.replace:
            replacements[old] = new

    base64_content = extract_base64_html(eml_file)
    if base64_content:
        # Pass the replacements dictionary to the function
        decode_and_save_html(base64_content, html_file, replacements or None)
    else:
        print(f"No HTML content found in {eml_file}.")
