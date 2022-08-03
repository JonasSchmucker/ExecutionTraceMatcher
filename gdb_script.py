import re

import gdb
from pathlib import Path


def main():
    gdb.execute("start", False, True)
    gdb.execute("break exit", False, True)
    gdb.execute("record btrace bts", False, True)
    gdb.execute("continue", False, True)

    inferiors_output = gdb.execute("info inferiors", False, True)
    inferiors_output_split = inferiors_output.split(" ")
    inferiors_output_split = list(filter(lambda element: element is not '', inferiors_output_split))
    inferior_path = inferiors_output_split[-2]
    inferior = Path(inferior_path).resolve().name

    info_record_output = gdb.execute("info record", False, True)
    info_record_output_line = info_record_output.split('\n')[-2]
    m = re.match(
        r"Recorded (\d+) instructions in .*",
        info_record_output_line
    )
    recorded_instruction_amount = m.group(1)

    print("Saving " + recorded_instruction_amount + " traced instructions")
    gdb.execute("pipe record instruction-history 1," + recorded_instruction_amount + " | python3 ./trace_reader.py " + inferior)
    gdb.execute("continue", False, True)
    gdb.execute("quit", False, True)


if __name__ == '__main__':
    main()