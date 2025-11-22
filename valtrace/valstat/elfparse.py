from typing import List, Dict
from elftools.elf.elffile import ELFFile


def get_funclist_messages(elf_path: str, names: List[str]) -> List[Dict]:
    """
    在 ELF 的 .symtab 和 .dynsym 中精确匹配函数名并返回符号信息列表。

    参数:
      - elf_path: ELF 文件路径
      - names: 需要精确匹配的名字列表（可以包含多个）

    返回:
      - 列表，每项为 dict（见模块头部说明）。如果未找到，返回空列表。
    """
    if not names:
        raise ValueError("names 列表不能为空（需要至少一个函数名用于精确匹配）")

    # prepare match set
    name_set = set(names)
    
    def _matches(n: str) -> bool:
        return n in name_set

    results = []
    with open(elf_path, "rb") as f:
        elffile = ELFFile(f)
        for secname in (".symtab", ".dynsym"):
            sec = elffile.get_section_by_name(secname)
            if not sec:
                continue
            try:
                for sym in sec.iter_symbols():
                    # only functions
                    try:
                        st_type = sym["st_info"]["type"]
                    except Exception:
                        st_type = None
                    if st_type != "STT_FUNC":
                        continue
                    name = sym.name
                    if not name:
                        continue
                    if _matches(name):
                        info = {
                            "section": secname,
                            "name": name,
                            "vaddr": int(sym["st_value"]),
                            "size": int(sym["st_size"]),
                            "bind": sym["st_info"]["bind"],
                            "type": st_type,
                            "shndx": sym["st_shndx"],
                        }
                        results.append(info)
            except Exception:
                # robustly skip malformed symbol tables
                continue
    return results


def get_function_messages(elf_path: str, name: str) -> List[Dict]:
    """
    在 ELF 的 .symtab 和 .dynsym 中精确匹配函数名并返回符号信息列表。

    参数:
      - elf_path: ELF 文件路径
      - name: 需要精确匹配的函数名

    返回:
      - 列表，每项为 dict（见模块头部说明）。如果未找到，返回空列表。
    """
    if not name:
        raise ValueError("name 不能为空（需要至少一个函数名用于精确匹配）")

    results = []
    with open(elf_path, "rb") as f:
        elffile = ELFFile(f)
        for secname in (".symtab", ".dynsym"):
            sec = elffile.get_section_by_name(secname)
            if not sec:
                continue
            try:
                for sym in sec.iter_symbols():
                    try:
                        st_type = sym["st_info"]["type"]
                    except Exception:
                        st_type = None
                    if st_type != "STT_FUNC":
                        continue
                    sym_name = sym.name
                    if not sym_name:
                        continue
                    if sym_name == name:  # 精确匹配函数名
                        info = {
                            "section": secname,
                            "name": sym_name,
                            "vaddr": int(sym["st_value"]),
                            "size": int(sym["st_size"]),
                            "bind": sym["st_info"]["bind"],
                            "type": st_type,
                            "shndx": sym["st_shndx"],
                        }
                        results.append(info)
            except Exception:
                # 跳过格式不正确的符号表
                continue
    return results



def get_function_address(elf_path: str, name: str) -> List[Dict]:
    funcs = get_function_messages(elf_path, name)
    if len(funcs) == 0:
        return None
    else:
        if len(funcs) > 1:
            print(f"Warning: 找到多个函数 {name} 的符号信息，返回第一个匹配项的地址")
        return funcs[0]["vaddr"]

if __name__ == "__main__":
    elfpath = "/mnt/d/MYTOOLS/ValTrace/valtrace/valstat/testcase/statistics_func_test"
    func_name = "main"
    funcs = get_function_messages(elfpath, func_name)
    if not funcs:
        print(f"未找到函数 {func_name} 的符号信息")
    if len(funcs) > 1:
        print(f"找到多个函数 {func_name} 的符号信息：")
    

    for r in funcs:
        print(f'{r["name"]}\taddr=0x{r["vaddr"]:x}\tsize={r["size"]}\tsection={r["section"]}')
    
    
    res = get_function_address(elfpath, func_name)
    print(f"函数 {func_name} 的地址: 0x{res:x}")