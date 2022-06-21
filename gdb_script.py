import argparse
import gdb
from pathlib import Path


def handle_arguments():
    # Create the parser and add arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('inputFile',
                        metavar='inputFile',
                        type=ascii,
                        nargs=1,
                        help='the program to be analyzed'
                        )

    # Parse and print the results
    args = parser.parse_args()
    return args.inputFile


def main():
    # input_file = handle_arguments()
    # input_path = Path(input_file).resolve()
    # if not input_path.exists():
    #     gdb.execute("echo " + ERROR_SIGNAL)
    #     exit("Input File does not exist")
    # input_file_name = input_path.name

    gdb.execute("start")
    gdb.execute("break exit")
    gdb.execute("record btrace bts")
    gdb.execute("continue")
    gdb.execute("pipe record instruction-history 1,1000000 | python3 ./trace_reader.py")
    gdb.execute("continue")
    gdb.execute("quit")


if __name__ == '__main__':
    main()
