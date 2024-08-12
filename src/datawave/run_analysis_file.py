# wrapper_script.py
import os
import shutil
import subprocess
import sys
import venv

def create_virtualenv(env_name):
    venv.create(env_name, with_pip=True)
    env_path = os.path.join(os.getcwd(), env_name)
    return env_path


def activate_virtualenv(env_path):
    activate_script = os.path.join(env_path, 'bin', 'activate')
    activate_command = f'source {activate_script}'
    return activate_command


def install_packages(requirements_file, env_path):
    activate_command = activate_virtualenv(env_path)
    try:
        print("Installing packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "--quiet" ,"install", "-r", requirements_file])
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while installing packages: {e}")
        return False
    return True


def run_target_script(script_path, df_file):
    import analysis
    try:
        analysis.run_analysis(df_file)
        
    except Exception as e:
        print(f"An error occurred while running the target script: {e}")
        return False


def copy_files(source_folder):
    # files = ['requirements_analysis.txt', 'analysis.py']
    files = os.listdir(source_folder)
    for file_name in files:
        src = os.path.join(source_folder, file_name)
        dst = os.path.join(os.getcwd(), file_name)
        if os.path.isfile(src):
            print(f"Copying {file_name} from {source_folder} to {os.getcwd()}")
            shutil.move(src, dst)
        else:
            print(f"{file_name} not found in {source_folder}")


def run(source_folder, df):

    # Check if the source folder is empty
    if not os.listdir(source_folder):
        print("Source folder is empty.")
        return None

    # Copy files from the source folder to the current working directory
    copy_files(source_folder)

    requirements_file = 'requirements_analysis.txt'
    target_script_path = 'analysis.py'

    env_name = 'ana_venv'
    env_path = create_virtualenv(env_name)

    if os.path.isfile(requirements_file):
        pckg_status = install_packages(requirements_file, env_path)

    # Run the target script
    if os.path.isfile(target_script_path):
        run_target_script(target_script_path, df)

