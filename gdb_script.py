import gdb


def main():
    gdb.execute("start")
    gdb.execute("break exit")
    gdb.execute("record btrace bts")
    gdb.execute("continue")
    gdb.execute("pipe record instruction-history 1,1000000 | python3 ./trace_reader.py")
    gdb.execute("continue")
    gdb.execute("quit")


if __name__ == '__main__':
    main()
