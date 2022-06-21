#!/bin/sh
perf_event_paranoid_level=$(cat /proc/sys/kernel/perf_event_paranoid)
if [ $perf_event_paranoid_level = 0 -o $perf_event_paranoid_level = 1 -o $perf_event_paranoid_level = -1 ]
then
  program_name=$1
  shift
  gdb -q -x ./gdb_script.py --args "$program_name" $@
else
  echo The value at /proc/sys/kernel/perf_event_paranoid needs to be less than 2 in order for hardware supported tracing to be available. It is currently at
  echo $perf_event_paranoid_level
fi