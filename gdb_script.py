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
    gdb.execute("pipe record instruction-history 1,1000000 | python3 ./trace_reader.py " + inferior)
    gdb.execute("continue", False, True)
    gdb.execute("quit", False, True)


if __name__ == '__main__':
    main()
