# valTrace
Valgrind extension tool.

## valstat
Execution of statistical functions
使用方式:
```
from valtrace.valstat.run_valstat import run_valstat
BINARYPATH = '/mnt/d/MYTOOLS/ValTrace/valtrace/valstat/testcase/statistics_func_test'

run_valstat(BINARYPATH)
```


## valIntervalStat

收集程序运行时某段时间内的函数
使用方式：

```
from valtrace.valIntervalStat.run_valIntervalStat import run_valIntervalStat
BINARYPATH = '/mnt/d/MYTOOLS/ValTrace/valtrace/valstat/testcase/statistics_func_test'

run_valIntervalStat(BINARYPATH)
```

## TODO
Implement Function Trace by valgrind...