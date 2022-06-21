#!/bin/sh
perf_event_paranoid_level=$(cat /proc/sys/kernel/perf_event_paranoid)
echo $perf_event_paranoid_level
if [ $perf_event_paranoid_level = 0 -o $perf_event_paranoid_level = 1 -o $perf_event_paranoid_level = -1 ]
then
  program_name=$1
  shift
  echo running: gdb -q -x ./gdb_script.py --args "$program_name" $@
  gdb -q -x ./gdb_script.py --args "$program_name" $@
else
  echo The value at /proc/sys/kernel/perf_event_paranoid needs to be less than 2 in order for hardware supported tracing to be available
fi