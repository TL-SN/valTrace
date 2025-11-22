import argparse ,re

def ptfunlist(fun_list):
    print(f"Executed functions [{len(fun_list)}]: ")
    print("[",end="")
    for func in fun_list:
        print(func,end=",")
    print("]")

def parse_func_addr(line:str):
    colon_idx=line.find(":")
    if colon_idx==-1:
        return None
    sub_line=line[colon_idx+1:].strip()
    pattern = r'0x[0-9a-fA-F]+'
    search_match = re.search(pattern, sub_line)
    if search_match:
        return search_match.group()
    else:
        return None

def get_func_trace(binary_path:str,path:str):
    fp=open(path, "r")
    lines=fp.readlines()
    fp.close()
    
    executed_funcs=set()

    for i in range(len(lines)):
        line=lines[i]
        if binary_path in line:
            func_addr=parse_func_addr(line)
            if func_addr:
                executed_funcs.add(func_addr)


    # sorted the executed functions
    executed_funcs = sorted(executed_funcs)
    return executed_funcs



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a binary file with optional parameters.")
    parser.add_argument("--binarypath", "-b", required=True, help="Path of the binary file")
    parser.add_argument("--callgrindlogpath", "-d", required=True, help="Path to the callgrind log file")
    args = parser.parse_args()

    binary_path = args.binarypath
    call_annotate_path = args.callgrindlogpath

    execfunlist=get_func_trace(binary_path,call_annotate_path)

    ptfunlist(execfunlist)