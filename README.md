The ExecutionTraceMatcher enables your computer to dynamically analyse executables, without the need for a long and tedious reverse engineering process. Executable traces are saved and can later be compared to the traces of other executables. Because the analysed program is actually being run, you will not be held back by obfuscated executables, where even a recursive descent disassembler might encounter problems.

The recording of the executable trace is sped up by relying on Intel's hardware supported instruction recording

## Instant Setup ##

Make sure you have [GDB 8.0 or higher](https://www.gnu.org/s/gdb) compiled with Python3.6+ bindings.
This tool requires the [Enhanced Features for gdb (gef)](https://github.com/hugsy/gef) package.


```bash
# clone from github repository
$ git clone https://github.com/JonasSchmucker/ExecutionTraceMatcher

# cd into it
$ cd ExecutionTraceMatcher

# run the tool
./save_trace.sh /path/to/your/executable --your --executables --args
```

## Intel Branch Tracing ##

For hardware supported instruction tracing to be enabled, the value at 
```bash
/proc/sys/kernel/perf_event_paranoid
``` 
needs to be less than 2.
This can be arranged by running:

```bash
sudo nano /proc/sys/kernel/perf_event_paranoid
```
and changing the value to e.g. 1. This will be reset after each reboot of your machine.

### Warning ###

In order to analyse the executable, the program is being run inside of gdb. Don't run any maliciouos code with this tool unless in a controlled environment, as it might affect your machine