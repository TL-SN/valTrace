# 🌟 **ValTrace - Valgrind Extension Tool Suite** 🌟

ValTrace is an extension tool suite based on **Valgrind**, designed to analyze and profile function execution during program runtime. It offers two distinct analysis modes to help developers gain in-depth insights into program execution flow and performance characteristics.

------

## 📜 **Project Overview**

ValTrace consists of **two core modules**:

- 🛠️ **`valstat`**: Collects statistics on all function calls during the program's entire execution.
- ⏱️ **`valIntervalStat`**: Collects function execution information within specific time intervals during program runtime.

------

## 🖥️ **System Requirements**

### 🔧 **Required Dependencies**

- **Valgrind**: Version 3.18.0 or higher
- **Python**: Version 3.7 or higher
- **callgrind_annotate**: Part of the Valgrind toolchain
- **callgrind_control**: Part of the Valgrind toolchain



------

## 🚀 **Installation and Usage**

### 1️⃣ **Install Dependencies**

```
pip install -r requirements.txt
```

### 2️⃣ **Verify System Tools**

Ensure that Valgrind and related tools are installed:

```
valgrind --version
which callgrind_annotate
which callgrind_control
```

------

## ⚙️ **Core Modules**

### 🔍 **`valstat` Module**

#### 📝 **Function Description**

Collects statistics on **all functions** called during the program's complete execution and generates a comprehensive function execution trace.

#### 🧑‍💻 **Usage**

```
from valtrace.valstat.run_valstat import run_valstat

# Specify the binary file path and runtime parameters
BINARYPATH = '/path/to/your/binary'
RUN_PARAMS = "your_parameters"

# Execute the statistics collection
executed_functions = run_valstat(BINARYPATH, RUN_PARAMS, temp_dir="./tmp")
```

#### 🔥 **Example**

```
from valtrace.valstat.run_valstat import run_valstat

BINARYPATH = '/mnt/d/MYTOOLS/ValTrace/valtrace/valIntervalStat/testcase/statistics_runtime_func'
RUN_PARAMS = "5"

run_valstat(BINARYPATH, RUN_PARAMS)
```

------

### ⏳ **`valIntervalStat` Module**

#### 📝 **Function Description**

Collects function execution information **within specific time intervals** during program runtime, allowing you to control the start and end points of monitoring.

#### 🧑‍💻 **Usage**

```
from valtrace.valIntervalStat.run_valIntervalStat import run_valIntervalStat

# Specify the binary file path and runtime parameters
BINARYPATH = '/path/to/your/binary'
RUN_PARAMS = "your_parameters"

# Execute the interval-based statistics collection
executed_functions = run_valIntervalStat(BINARYPATH, RUN_PARAMS, temp_dir="./tmp")
```

#### 🔥 **Example**

```
from valtrace.valIntervalStat.run_valIntervalStat import run_valIntervalStat

BINARYPATH = '/mnt/d/MYTOOLS/ValTrace/valtrace/valIntervalStat/testcase/statistics_runtime_func'
RUN_PARAMS = "5"

run_valIntervalStat(BINARYPATH, RUN_PARAMS)
```

------

## 🏗️ **Tool Architecture**

### 🧩 **Core Components**

#### 1. 🧳 **ELF Parser** (`valtrace/tools/elfparse.py`)

- Parses **ELF** file symbol tables (`.symtab` and `.dynsym`).
- Retrieves function addresses and symbol information.
- Supports precise function name matching.

#### 2. 📊 **Function Statistics Tool** (`valtrace/tools/funstat.py`)

- Parses `callgrind_annotate` output.
- Extracts function addresses and names.
- Generates a list of executed functions.

#### 3. 🎮 **Execution Controllers**

- **`valstat`**: Controls the full execution flow.
- **`valIntervalStat`**: Controls interactive interval-based monitoring.

------

### 🛠️ **Workflow**

1. **Program Check**: Verifies if Valgrind and related tools are available.
2. **Temporary Directory Management**: Creates and cleans up temporary files.
3. **Valgrind Execution**: Uses the `callgrind` tool to generate execution traces.
4. **Result Annotation**: Uses `callgrind_annotate` to process raw data.
5. **Function Analysis**: Parses annotated results and extracts function information.
6. **Result Output**: Displays a list of executed functions.

------

## 🧪 **Test Cases**

The project includes two test cases to validate the functionality of the tools:

### 1️⃣ **Function Statistics Test** (`valtrace/valstat/testcase/`)

- **`statistics_func.c`**: A test program with multi-layer function calls.
- **Compilation command**: `gcc -s -no-pie ./statistics_func.c -o ./statistics_func_test -lm`

### 2️⃣ **Runtime Statistics Test** (`valtrace/valIntervalStat/testcase/`)

- **`statistics_runtime_func.c`**: A test program supporting command-line arguments.
- **Features**: Factorial calculations, power operations, recursive multiplication, etc.

### 🔬 **Test Scripts**

- **`test_valstat.py`**: Tests for the `valstat` module.
- **`test_valIntervalStat.py`**: Tests for the `valIntervalStat` module.



<video src="show____List the functions executed during the CVE-2023-33476_minidlnad POC runtime..mp4"></video>

------

## 📝 **Output Format**

After execution, the tool will output results in the following format:

```
Executed functions [15]: 
[0x400500, 0x400520, 0x400540, 0x400560, ...]
```

------

## 🌍 **Use Cases**

Function profiling and statistics collection.

------



## 🔥 **Some Bug**

Function statistics may have omissions. For example, in the case of `CVE-2023-33476_minidlnad`, `Valgrind` successfully tracks the `timevalfix` function, but after processing with `callgrind_annotate`, the trace information for `timevalfix` disappears.

The exact reason is unclear, but it is speculated that the low code coverage of the `timevalfix` function may have caused `callgrind_annotate` to ignore this function.



## 🚧 **TODO**

- Add **function trace** functionality.

------

🎉 **Enjoy analyzing and profiling your programs with ValTrace!** 🎉

