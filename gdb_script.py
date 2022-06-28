import re

import gdb
from pathlib import Path


def main():
    gdb.execute("start", False, True)
    gdb.execute("break exit", False, True)
    gdb.execute("record btrace bts", False, True)
    gdb.execute("continue", False, True)

    inferiors_output = gdb.execute("info inferiors", False, True)
    inferior_path = inferiors_output.split(" ")[-2]
    print(inferior_path)
    inferior = Path(inferior_path).resolve().name

    info_record_output = gdb.execute("info record", False, True)
    info_record_output_line = info_record_output.split('\n')[-2]
    m = re.match(
        r"Recorded (\d+) instructions in .*",
        info_record_output_line
    )
    recorded_instructon_ammount = m.group(1)

    print("Saving " + recorded_instructon_ammount + " traced instructions")
    gdb.execute("pipe record instruction-history 1," + recorded_instructon_ammount + " | python3 ./trace_reader.py " + inferior)
    gdb.execute("continue", False, True)
    gdb.execute("quit", False, True)


if __name__ == '__main__':
    main()
