import sys
import re
import json

example1 = "6648	   0x00007ffff7d23ea3 <_IO_new_file_overflow+99>:	movzx  eax,bl"
example2 = "21370	   0x00005555555559da <decrypt+410>:	ret"
example3 = "1	   0x0000555555555211 <main+8>:	lea    rax,[rip+0xdf0]        # 0x555555556008"
example4 = "15834	   0x00007ffff7d24ea7 <__GI__IO_default_xsputn+103>:	movzx  esi,BYTE PTR [rcx]"
example5 = "4	   0x00005555555550b0 <puts@plt+0>:	endbr64"
example6 = "15	   0x00007ffff7cbf490 <*ABS*+0xa8720@plt+0>:	endbr64"


def parse_line(line):
    m = re.match(
        r"(?P<counter>\d+)"  # counter, group 1
        r"\s+"  # whitespace
        r"(?P<adress>0[xX][0-9a-fA-F]+)"  # adress, group 2
        r"\s+"  # whitespace
        r"<(?P<function_name>[\w+@\*]*)>:"  #function name, group 3
        r"\s+"  # whitespace
        r"(?P<mnemonic>[a-zA-Z0-9]+)"  # mnemonic, group 4
        r"\s*"  # whitespace
        #r"(?P<args>([a-zA-Z0-9]+)*(,[a-zA-Z0-9]+)*)"  # arguments, group 5+
        r"(?P<args>[^#]*)"  # arguments, group 5+
        r".*"  # rest
        ,
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


def main():
    instructions = list()
    while True:
        try:
            line = input()
        except EOFError:
            break

        counter, adress, long_text, mnemonic, args = parse_line(line)
        instructions.append((counter, adress, long_text, mnemonic, args))

    with open("gdb_trace.json", "w") as outfile:
        json.dump(instructions, outfile, indent=4)


if __name__ == '__main__':
    main()
