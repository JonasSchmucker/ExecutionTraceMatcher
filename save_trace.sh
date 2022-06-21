#!/bin/sh
perf_event_paranoid_level=$(cat /proc/sys/kernel/perf_event_paranoid)
echo $perf_event_paranoid_level
if [ $perf_event_paranoid_level = 0 -o $perf_event_paranoid_level = 1 -o $perf_event_paranoid_level = -1 ]
then
  gdb -q -x ./gdb_script.py --args ~/Desktop/Masterarbeit/RSA/compilations/rsa_GCC_O0
else
  echo The value at /proc/sys/kernel/perf_event_paranoid needs to be less than 2 in order for hardware supported tracing to be available
fi