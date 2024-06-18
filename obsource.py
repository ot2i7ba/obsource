# Copyright (c) 2023 ot2i7ba
# https://github.com/ot2i7ba/
# This code is licensed under the MIT License (see LICENSE for details).

"""
Obsource - Sourcecode Security through obscurity v0.1

This is a Python script designed to obscure or deobscure Python source code files. 
It utilizes a simple byte-shifting algorithm based on a user-provided seed value for the transformation process. 

The script supports two primary operations:
1. Obscure: Alters each byte of the source code by adding the seed value, rendering the code unreadable and non-executable. 
   This mode is intended to hide the code's content from immediate understanding.
2. Deobscure: Reverses the obscuring process by subtracting the seed value from each byte of the obscured code. 
   It requires the same seed used during the obscuring process to correctly restore the original code.

The script can be operated either through command-line arguments or interactive prompts, providing flexibility in usage. 
It includes basic functionalities like input validation, error handling, and logging, enhancing its reliability and user-friendliness.

Note: This script employs 'Security through Obscurity', which should not be considered a robust security measure. 
It's primarily meant for hiding code from plain sight rather than providing any strong encryption or protection.

usage: obsource.py [-h] [{o,d}] [file] [seed]

positional arguments:
  {o,d}       Mode: "o" for obscure, "d" for deobscure
  file        Python file to be processed
  seed        Four-digit initial code (Seed)

optional arguments:
  -h, --help  show this help message and exit
"""

import os
import logging
import hashlib
import time
import argparse
import sys

# Clear screen function
def clear_screen():
    if os.name == 'nt':  # for Windows
        os.system('cls')
    else:  # for macOS and Linux
        os.system('clear')

# Logging configuration
logging.basicConfig(filename='obscurce.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_md5(file_path):
    """Calculates the MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def obscure_code(code, seed):
    """Obscures the code based on a seed. Uses byte shifting."""
    try:
        bytes_code = code.encode('utf-8')
        return bytes((byte + seed) % 256 for byte in bytes_code)
    except Exception as e:
        logging.error(f"Error obscuring code: {e}")
        raise

def deobscure_code(code, seed):
    """Deobscures the code based on a seed. Uses byte shifting."""
    try:
        return bytes((byte - seed) % 256 for byte in code).decode('utf-8')
    except Exception as e:
        logging.error(f"Error deobscuring code: {e}")
        raise

def validate_file_path(file_path):
    """Checks if the given file path is valid."""
    if not os.path.isfile(file_path):
        logging.error(f"File {file_path} does not exist.")
        return False
    return True

def updated_process_file(file_path, seed, mode):
    """Processes the file for obscuring or deobscuring and considers relative paths."""
    start_time = time.time()  # Start timing

    try:
        if not os.path.dirname(file_path):
            file_path = os.path.join(os.getcwd(), file_path)

        if not validate_file_path(file_path):
            print(f"Error: File {file_path} does not exist.")
            return

        md5_original = calculate_md5(file_path)
        logging.info(f"MD5 of original file ({file_path}): {md5_original}")

        with open(file_path, 'rb' if mode == 'd' else 'r') as file:
            content = file.read()

        base_filename = os.path.splitext(file_path)[0]
        if mode == 'o':
            new_content = obscure_code(content, seed)
            new_file_path = f"{base_filename}_obscure.py"
        else:
            new_content = deobscure_code(content, seed)
            new_file_path = f"{base_filename}_deobscure.py"

        if os.path.exists(new_file_path):
            overwrite = input(f"File {new_file_path} already exists. Overwrite? (y/n): ").lower()
            if overwrite != 'y':
                print("Operation cancelled.")
                return

        with open(new_file_path, 'wb' if mode == 'o' else 'w') as file:
            file.write(new_content)

        md5_new = calculate_md5(new_file_path)
        logging.info(f"MD5 of new file ({new_file_path}): {md5_new}")

        processing_time = time.time() - start_time  # Calculate processing time
        print(f"File {new_file_path} successfully {'obscured' if mode == 'o' else 'deobscured'} in {processing_time:.2f} seconds.")
        logging.info(f"File {new_file_path} successfully {'obscured' if mode == 'o' else 'deobscured'} in {processing_time:.2f} seconds.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        logging.error(f"An unexpected error occurred: {e}")

def parse_arguments():
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(description='Obscure or deobscure Python source code.')
    parser.add_argument('mode', nargs='?', choices=['o', 'd'], help='Mode: "o" for obscure, "d" for deobscure')
    parser.add_argument('file', nargs='?', help='Python file to be processed')
    parser.add_argument('seed', nargs='?', type=int, help='Four-digit initial code (Seed)')
    return parser.parse_args()

def interactive_input():
    """Handles interactive user input."""
    clear_screen()
    print("Obsource - Sourcecode Security through obscurity v0.1")
    print("=======================================================\n")
    
    mode = input("Do you want to obscure (o) or deobscure (d) a source code? Enter 'o' or 'd' (or 'q' to quit): ").lower()
    if mode == 'q':
        sys.exit("Exiting Obscurce.")
    
    file_path = input("Enter the name of the Python file (with .py): ")
    if file_path == 'q':
        sys.exit("Exiting Obscurce.")
    
    seed = input("Enter a four-digit initial code (Seed): ")
    if seed == 'q':
        sys.exit("Exiting Obscurce.")
    
    return mode, file_path, seed

def main():
    args = parse_arguments()

    # Check if the script is run with arguments or needs interactive input
    if args.mode and args.file and args.seed:
        mode = args.mode
        file_path = args.file
        seed = args.seed
    else:
        mode, file_path, seed = interactive_input()

    if not file_path.endswith('.py'):
        print("Invalid file extension. Please specify a Python file (.py).")
        return

    try:
        seed = int(seed)
        if not (1000 <= seed <= 9999):
            raise ValueError
    except ValueError:
        print("Invalid input. The seed must be a four-digit number.")
        return

    updated_process_file(file_path, seed, mode)

if __name__ == "__main__":
    main()
