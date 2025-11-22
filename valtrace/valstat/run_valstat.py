import subprocess,shutil,os
from ..tools.funstat import get_func_trace, ptfunlist

def check_program_installed():
    """
    Check if the necessary programs are installed.
    """
    programs = ['valgrind', 'callgrind_annotate' ]
    for program in programs:
        # Check if the program is available in the system's PATH using shutil.which
        if shutil.which(program) is None:
            print(f"Please install {program} to continue")
            exit(1)

def create_temp_dir(temp_dir):
    """
    Create the temporary directory if it doesn't exist.
    """
    os.makedirs(temp_dir, exist_ok=True)

def clean_log_files(temp_dir):
    """
    Remove old log files from the temporary directory if they exist.
    """
    log_files = ['callannote.log', 'callgrind.log']
    for log_file in log_files:
        log_file_path = os.path.join(temp_dir, log_file)
        if os.path.exists(log_file_path):
            os.remove(log_file_path)

def run_valgrind(binary_path, temp_dir):
    """
    Run the valgrind tool to generate callgrind.log.
    """
    valgrind_command = [
        'valgrind', '--tool=callgrind', '--trace-children=yes',
        '--callgrind-out-file=' + os.path.join(temp_dir, 'callgrind.log'),
        binary_path
    ]
    # Run the command and suppress stderr output
    with open(os.devnull, 'w') as devnull:
        subprocess.run(valgrind_command, stderr=devnull)

def run_callgrind_annotate(temp_dir):
    """
    Run the callgrind_annotate tool to generate callannote.log.
    """
    callgrind_annotate_command = [
        'callgrind_annotate', '--tree=both', os.path.join(temp_dir, 'callgrind.log')
    ]
    # Run the command and write the output to callannote.log
    with open(os.path.join(temp_dir, 'callannote.log'), 'w') as callannote_log:
        subprocess.run(callgrind_annotate_command, stdout=callannote_log)

def run_funstat(binary_path, temp_dir):
    """
    Run the funstat.py script with the required parameters.
    """
    func_list = get_func_trace(binary_path, os.path.join(temp_dir, 'callannote.log'))
    ptfunlist(func_list)

def run_valstat(binary_path, temp_dir="./tmp"):
    """
    Orchestrates the entire process: checking programs, creating directories,
    running valgrind, annotating, and running funstat.
    """

    print("Running valstat...")
    # Check if necessary programs are installed
    check_program_installed()

    # Create the temporary directory and clean up old log files
    create_temp_dir(temp_dir)
    clean_log_files(temp_dir)

    # Run valgrind to generate callgrind.log
    run_valgrind(binary_path, temp_dir)

    # Run callgrind_annotate to generate callannote.log
    run_callgrind_annotate(temp_dir)

    # Run the funstat.py script with the appropriate parameters
    run_funstat(binary_path, temp_dir)

if __name__ == "__main__":
    BINARYPATH = '/mnt/d/MYTOOLS/ValTrace/valtrace/valstat/testcase/statistics_func_test'
    TEMP_DIR = "./tmp"
    run_valstat(BINARYPATH, TEMP_DIR)
