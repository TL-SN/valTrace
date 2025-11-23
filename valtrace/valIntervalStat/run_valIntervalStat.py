import subprocess,shutil,os,time,threading
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




# valgrind --tool=callgrind --trace-children=yes --callgrind-out-file=callgrind.log.log  --instr-atstart=no ./test_func 2> /dev/null
def run_valgrind_with_noinstr(binary_path:str, run_params:str,temp_dir:str):
    """
    Run the valgrind tool to generate callgrind.log.
    """
    valgrind_command = [
        'valgrind', '--tool=callgrind', '--trace-children=yes',
        '--callgrind-out-file=' + os.path.join(temp_dir, 'callgrind.log'),
        '--instr-atstart=no',
        binary_path, run_params
    ]
    # Run 
    # subprocess.run(valgrind_command)
    
    subprocess.Popen(valgrind_command)
    

def set_callgrind_instr_off():
    while True:
        callgrind_control_command = [
            'callgrind_control', '--instr=off'
        ]
        result = subprocess.run(callgrind_control_command, capture_output=True, text=True)
        if "No active callgrind runs detected." in result.stdout or "No active callgrind runs detected." in result.stderr:
            time.sleep(0.5)
        else:
            print("valgrind instrumentation turned on. wait 1s...")
            time.sleep(1)
            return 


def prompt_set_instr(turnon_event):
    while not turnon_event.is_set():
        time.sleep(3)
        print("[+]Whether set Valgrind's instr=on? (yes or no)",flush=True)


def set_callgrind_instr_on():
    """
    Set callgrind to start instrumentation.
    """
    while True:
        callgrind_control_command = [
            'callgrind_control', '--instr=on'
        ]
        result = subprocess.run(callgrind_control_command, capture_output=True, text=True)
        if "No active callgrind runs detected." in result.stdout or "No active callgrind runs detected." in result.stderr:
            time.sleep(0.5)
        else:
            print("Valgrind instrumentation turned on. plz wait 1s...")
            time.sleep(1)
            return 

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
    return func_list


def prompt_user(stop_event):
    while not stop_event.is_set():  # 直到接收到停止信号
        time.sleep(3)  # 每5秒输出一次提示
        print("[-]Confirm whether valgrind is tracking the end... (yes or no): ", flush=True)


def run_valIntervalStat(binary_path:str,run_params:str,  temp_dir="./tmp"):
    """
    Orchestrates the entire process: checking programs, creating directories,
    running valgrind, annotating, and running funstat.
    """

    print("Running valIntervalStat...")

    # Check if necessary programs are installed
    check_program_installed()
    # Create the temporary directory and clean up old log files
    create_temp_dir(temp_dir)
    clean_log_files(temp_dir)



    # async Run valgrind with --instr-atstart=no to generate callgrind.log
    run_valgrind_with_noinstr(binary_path,run_params, temp_dir)

    turnon_event = threading.Event()
    turnon_thread = threading.Thread(target=prompt_set_instr,args=(turnon_event,),daemon=True)
    turnon_thread.start()
    
    while True:
        isturnon = input("[+]Whether set Valgrind's instr=on? (yes or no)\n").strip().lower()
        if isturnon == "" or nextstep == "yes":
            turnon_event.set()
            set_callgrind_instr_on()
            print("now Valgrind will collect run messages...")
            
            break

    
    turnon_thread.join()






    stop_event = threading.Event()  # 创建一个停止事件对象
    thread = threading.Thread(target=prompt_user, args=(stop_event,), daemon=True)
    thread.start()
    while True:
        nextstep = input("[-]Confirm whether valgrind is tracking the end... (yes or no): \n").strip().lower()
        if nextstep == "" or nextstep == "yes":
            print("now start callgrind_annotate...")
            stop_event.set()
            time.sleep(1)
            break






    thread.join()
    run_callgrind_annotate(temp_dir)
    # Run the funstat.py script with the appropriate parameters
    return run_funstat(binary_path, temp_dir)

if __name__ == "__main__":
    BINARYPATH = '/mnt/d/MYTOOLS/ValTrace/valtrace/valstat/testcase/statistics_func_test'
    TEMP_DIR = "./tmp"
    run_valIntervalStat(BINARYPATH, TEMP_DIR)
