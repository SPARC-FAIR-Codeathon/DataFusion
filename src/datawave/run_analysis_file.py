# wrapper_script.py
import os
import shutil
import subprocess
import sys


def install_packages(requirements_file):
    try:
        print("Installing packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while installing packages: {e}")
        return False
    return True


def run_target_script(script_path, df_file):
    try:
        result = subprocess.run(['python', script_path, df_file], capture_output=True, text=True)
        print("Output:")
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"An error occurred while running the target script: {e}")
        return False


def copy_files(source_folder):
    files = ['requirements.txt', 'target_script.py']
    for file_name in files:
        src = os.path.join(source_folder, file_name)
        dst = os.path.join(os.getcwd(), file_name)
        if os.path.isfile(src):
            print(f"Copying {file_name} from {source_folder} to {os.getcwd()}")
            shutil.copy(src, dst)
        else:
            print(f"{file_name} not found in {source_folder}")


def run(source_folder, df):

    # Check if the source folder exists
    if not os.path.isdir(source_folder):
        print("Source folder not found.")
        return None

    # Copy files from the source folder to the current working directory
    copy_files(source_folder)

    requirements_file = 'requirements_analysis.txt'
    target_script_path = 'analysis.py'

    if os.path.isfile(requirements_file):
        # Install required packages
        if not install_packages(requirements_file):
            sys.exit(1)


    # Run the target script
    if not run_target_script(target_script_path, df):
        print("Failed to run the target script.")
        sys.exit(1)