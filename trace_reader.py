import re
import numpy as np

example1 = "6648	   0x00007ffff7d23ea3 <_IO_new_file_overflow+99>:	movzx  eax,bl"
example2 = "21370	   0x00005555555559da <decrypt+410>:	ret"
example3 = "1	   0x0000555555555211 <main+8>:	lea    rax,[rip+0xdf0]        # 0x555555556008"
example4 = "15834	   0x00007ffff7d24ea7 <__GI__IO_default_xsputn+103>:	movzx  esi,BYTE PTR [rcx]"
example5 = "4	   0x00005555555550b0 <puts@plt+0>:	endbr64"
example6 = "15	   0x00007ffff7cbf490 <*ABS*+0xa8720@plt+0>:	endbr64"
example7 = "722	   0x0000555555564e4d:	mov    rdi,r14"


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
    if m is None:
        print("Line: " + line)
    return (
        int(m.group(1)),
        int(m.group(2), 16),
        m.group(3),
        m.group(4),
        m.group(5)
    )


def calculate_embedding(counter, address=None, function_name=None, mnemonic=None, args=None) -> np.array:
    return np.array((1, 0, 0))


def main():
    instructions = list()
    while True:
        try:
            line = input()
        except EOFError:
            break

        instructions.append(calculate_embedding(parse_line(line)))

    full_np_array = np.stack(instructions)
    np.save("trace_np_array", full_np_array)


if __name__ == '__main__':
    main()
