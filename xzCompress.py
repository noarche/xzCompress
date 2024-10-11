import os
import subprocess
import tarfile
from pathlib import Path
from colorama import Fore, Style, init

# Initialize colorama for colorful terminal output
init(autoreset=True)

# Path to xz.exe (default can be overridden here)
XZ_PATH = os.getenv('USERPROFILE') + r'\xz.exe'

def clean_path(user_input):
    """
    Cleans the user input by removing any unwanted quotes.
    """
    return user_input.replace('"', '')

def compress_file(file_path):
    output_path = file_path.with_suffix('.tar.xz')
    print(f"{Fore.GREEN}Compressing file {file_path} to {output_path}")
    
    # First, tar the file
    tar_path = file_path.with_suffix('.tar')
    with tarfile.open(tar_path, "w") as tar:
        tar.add(file_path, arcname=file_path.name)
    
    # Now compress with xz.exe
    subprocess.run([XZ_PATH, tar_path], check=True)
    
    print(f"{Fore.CYAN}Compressed file saved as {output_path}")

    # Wait for user to press enter key to return to main menu
    input(f"{Fore.YELLOW}Press enter key to return to main menu...")

def compress_directory(dir_path, output_dir):
    output_path = Path(output_dir) / (dir_path.name + '.tar.xz')
    print(f"{Fore.GREEN}Compressing directory {dir_path} to {output_path}")
    
    # First, tar the directory
    tar_path = Path(output_dir) / (dir_path.name + '.tar')
    with tarfile.open(tar_path, "w") as tar:
        tar.add(dir_path, arcname=dir_path.name)
    
    # Now compress the tar file with xz.exe
    subprocess.run([XZ_PATH, tar_path], check=True)
    
    print(f"{Fore.CYAN}Compressed directory saved as {output_path}")

    # Wait for user to press any key to return to main menu
    input(f"{Fore.YELLOW}Press any key to return to main menu...")

def decompress_file(file_path):
    print(f"{Fore.GREEN}Decompressing file {file_path}")
    subprocess.run([XZ_PATH, '-d', file_path], check=True)
    
    tar_path = file_path.with_suffix('')  # remove the .xz extension
    print(f"{Fore.GREEN}Extracting tar file {tar_path}")
    
    with tarfile.open(tar_path, "r") as tar:
        tar.extractall(path=tar_path.parent)
    
    # Delete the leftover .tar file
    os.remove(tar_path)
    print(f"{Fore.CYAN}Decompressed and extracted files. {Fore.RED}Deleted {tar_path}")

    # Wait for user to press any key to return to main menu
    input(f"{Fore.YELLOW}Press any key to return to main menu...")

def decompress_directory(file_path):
    decompress_file(file_path)

def get_user_choice():
    print(f"\n{Fore.YELLOW}Choose an operation:")
    print(f"1. Compress a file")
    print(f"2. Compress a directory")
    print(f"3. Decompress a file")
    print(f"4. Decompress a directory")
    print(f"{Fore.RED}Type 'q' or 'quit' to exit.")
    
    choice = input(f"{Fore.BLUE}Enter your choice (default 1): ").strip().lower()
    
    if choice in ['q', 'quit']:
        print(f"{Fore.MAGENTA}Exiting the script. Goodbye!")
        exit(0)
    
    return choice

def main():
    while True:
        choice = get_user_choice()
        
        if choice == "1":
            file_path_input = input(f"{Fore.BLUE}Enter the file path to compress: ").strip()
            file_path = Path(clean_path(file_path_input))
            compress_file(file_path)
        elif choice == "2":
            dir_path_input = input(f"{Fore.BLUE}Enter the directory path to compress: ").strip()
            dir_path = Path(clean_path(dir_path_input))
            output_dir_input = input(f"{Fore.BLUE}Enter the directory to save compressed file: ").strip()
            output_dir = Path(clean_path(output_dir_input))
            compress_directory(dir_path, output_dir)
        elif choice == "3":
            file_path_input = input(f"{Fore.BLUE}Enter the path of .xz archive to decompress: ").strip()
            file_path = Path(clean_path(file_path_input))
            decompress_file(file_path)
        elif choice == "4":
            dir_path_input = input(f"{Fore.BLUE}Enter the path of .xz archive to decompress: ").strip()
            dir_path = Path(clean_path(dir_path_input))
            decompress_directory(dir_path)
        else:
            print(f"{Fore.RED}Invalid choice! Please enter a number between 1 and 4 or 'q' to quit.")

if __name__ == "__main__":
    main()
