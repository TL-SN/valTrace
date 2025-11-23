import argparse ,re
from .elfparse import get_function_address

def ptfunlist(fun_list):
    print(f"Executed functions [{len(fun_list)}]: ")
    print("[",end="")
    for func in fun_list:
        print(hex(func),end=",")
    print("]")

def parse_func_name(line:str):
    colon_idx=line.find(":")
    if colon_idx==-1:
        return None
    
    bracket_idx=line.find("[")
    if bracket_idx==-1:
        return None
    
    sub_line=line[colon_idx+1:bracket_idx]
    blank_idx=sub_line.find(" ")
    quota_idx=sub_line.find("'")
    if quota_idx==-1:
        if blank_idx==-1:
            return None
        else:
            func_name=sub_line[:blank_idx]
            return func_name.strip()
    else:
        func_name=sub_line[:quota_idx]
        return func_name.strip()
def parse_func_addr(line:str):
    colon_idx=line.find(":")
    if colon_idx==-1:
        return None
    
    bracket_idx=line.find("[")
    if bracket_idx==-1:
        return None
    
    sub_line=line[colon_idx+1:bracket_idx]
    pattern = r'0x[0-9a-fA-F]+'                     # Pattern to match hexadecimal addresses
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
            func_addr_str=parse_func_addr(line)
            if func_addr_str:
                func_addr=int(func_addr_str,16)
                executed_funcs.add(func_addr)
            else:
                func_name=parse_func_name(line)
                if func_name:
                    func_addr=get_function_address(binary_path,func_name)
                    if func_addr:
                        executed_funcs.add(func_addr)                    
                    else:
                        print(f"Warning: 未找到函数 {func_name} 的符号信息")

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

    # binary_path="/root/build/sbin/minidlnad"
    # call_annotate_path="/mnt/d/MYTOOLS/ValTrace/tmp/callannote.log"
    execfunlist=get_func_trace(binary_path,call_annotate_path)

    ptfunlist(execfunlist)