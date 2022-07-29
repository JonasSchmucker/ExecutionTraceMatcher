import argparse
import json
import re
from pathlib import Path

import numpy as np

example1 = "6648	   0x00007ffff7d23ea3 <_IO_new_file_overflow+99>:	movzx  eax,bl"
example2 = "21370	   0x00005555555559da <decrypt+410>:	ret"
example3 = "1	   0x0000555555555211 <main+8>:	lea    rax,[rip+0xdf0]        # 0x555555556008"
example4 = "15834	   0x00007ffff7d24ea7 <__GI__IO_default_xsputn+103>:	movzx  esi,BYTE PTR [rcx]"
example5 = "4	   0x00005555555550b0 <puts@plt+0>:	endbr64"
example6 = "15	   0x00007ffff7cbf490 <*ABS*+0xa8720@plt+0>:	endbr64"
example7 = "722	   0x0000555555564e4d:	mov    rdi,r14"

# __INSTRUCTION_MAPPING__ = "instruction_categories.json"
__INSTRUCTION_MAPPING__ = "reduced_instruction_categories.json"


def parse_line(line):
    m = re.match(
        r"(?P<counter>\d+)"                 # counter, group 1
        r"\s+"                              # whitespace
        r"(?P<address>0[xX][0-9a-fA-F]+)"   # address, group 2
        r"\s*"                              # optional whitespace
        r"(?P<function_name>[\w+@\*<>]*):"  # function name, group 3
        r"\s+"                              # whitespace
        r"(?P<mnemonic>[a-zA-Z0-9]+)"       # mnemonic, group 4
        r"\s*"                              # optional whitespace
        r"(?P<args>[^#]*)"                  # arguments, group 5+
        r".*",                              # rest
        line
    )

    (counter, address, function_name, mnemonic, args) = (
        int(m.group(1)),
        int(m.group(2), 16),
        m.group(3),
        m.group(4),
        m.group(5)
    )
    if args is None:
        args = ""
    if function_name is None:
        function_name = ""
    return counter, address, function_name, mnemonic, args


def calculate_embedding(categories_dict, categories_id_dict, dimension,
                        counter, address, function_name, mnemonic, args) -> np.array:
    np_array = np.zeros(dimension)
    category = categories_dict.get(mnemonic.upper(), -1)
    if category == -1:
        return None
    category_id = categories_id_dict[category]
    np_array[category_id] = 1
    return np_array


def load_categories() -> (dict, dict, int):
    with open(__INSTRUCTION_MAPPING__, "r") as categories_file:
        instruction_dict = json.load(categories_file)

    counter = 0
    categories_dict = dict()
    categories_dict[0] = 0
    with open("traces/embedding_info.txt", "w") as info_file:
        for value in set(instruction_dict.values()):
            info_file.write("One-hot coding at postion " + str(counter) + " equates to: " + value + "\n")
            categories_dict[value] = counter
            counter += 1

    return instruction_dict, categories_dict, counter


def handle_arguments():
    # Create the parser and add arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('inferior_filename',
                        metavar='inferior_filename',
                        type=Path,
                        nargs=1,
                        help='inferior filename'
                        )

    # Parse and print the results
    args = parser.parse_args()
    return args.inferior_filename


def main():
    args = handle_arguments()
    inferior = args[0].resolve().name
    categories_dict, categories_id_dict, dimension = load_categories()
    instructions = list()
    while True:
        try:
            line = input()
        except EOFError:
            break

        (counter, address, function_name, mnemonic, args) = parse_line(line)
        if mnemonic is None:
            print(line)

        next_instruction = calculate_embedding(
                categories_dict, categories_id_dict, dimension,
                counter, address, function_name, mnemonic, args
                                )
        if next_instruction is not None:
            instructions.append(next_instruction)

    full_np_array = np.stack(instructions)
    traces_directory = Path("./traces/").resolve()
    if not traces_directory.exists():
        traces_directory.mkdir()
    np.save("traces/" + inferior + "_trace", full_np_array)


if __name__ == '__main__':
    main()
