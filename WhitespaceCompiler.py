#!/usr/bin/env python3
import sys
args = " ".join(sys.argv[1:])
cmds = {"MOD":["PUSH", "DUPE", "COPY", "SWAP", "POP", "SLDE"],
        "MATH":["ADD", "SUB", "MULT", "DIV", "MOD"],
        "HEAP":["STOR", "RET"],
        "FLOW":["LABL", "SUB", "JUMP", "JMPZ", "JMPN", "RET", "HALT"],
        "IO":["OUT", "NOUT", "IN", "NIN"]
}
combos = {"MOD":[" ", "\n ", "\t ", "\n\t", "\n\n", "\t\n", " "],
        "MATH":["  ", " \t", " \n", "\t ", "\t\t", "\t "],
        "HEAP":[" ", "\t", "\t\t"],
        "FLOW":["  ", " \t", " \n", "\t ", "\t\t", "\t\n", "\n\n", "\n"],
        "IO":["  ", " \t", "\t ", "\t\t", "\t\n"]
}
def error(message, line):
    print("Error at line " + str(line+1) + " (" + ".".join(i[:-1]) + ("" if i[-1] == None else " " + i[-1]) + "):")
    print("    " + message)
    exit()
    
if args in ["--help", "-h", "--man", "--docs", ""]:
    print("Commands:")
    for i in cmds:
        print(i + ": " + ", ".join(cmds[i]))
    print("Useful RegEx: " + "|".join([i + "|" + "|".join(cmds[i]) for i in cmds]) + "|\\.|[0-9]*")
else:
    file = args
    f = open(file)
    file = f.read()
    f.close()
    code = ""
    while "\n\n" in file:
        file = file[:file.index("\n\n")] + file[file.index("\n\n")+1:]
    file = file.strip("\n").split("\n")
    file = [i.strip().split() + ([] if " " in i.strip() else [None]) for i in file]
    file = [i[0].upper().split(".") + [" ".join([("" if j==None else j) for j in i[1:]])] for i in file]
    for line in range(len(file)):
        i = file[line]
        if len(i) != 3:
            error("Invalid command \"" + ".".join(i[:-1]) + "\"", line)
        try:
            code += combos[i[0]][-1]
        except KeyError as e:
            error("Invalid command \"" + ".".join(i[:-1]) + "\"", line)
        try:
            code += combos[i[0]][cmds[i[0]].index(i[1])]
        except ValueError as e:
            if e.message.endswith("' is not in list"):
                error("Invalid command \"" + ".".join(i[:-1]) + "\"", line)
            else:
                raise
        if i[2] != "":
            if ".".join(i[:-1]) not in need_arg:
                error("\"" + ".".join(i[:-1]) + "\" needs no argument, but was given \"" + i[2] + "\"", line)
            try:
                i[2] = int(i[2])
            except ValueError as e:
                if e.message.startswith("invalid literal for int() with base 10: '"):
                    if i[2] == '"\\n"':
                        i[2] = '"\n"'
                    if len(i[2]) == 3 and i[2][0] + i[2][2] == '""':
                        i[2] = ord(i[2][1])
                    else:
                        error("Argument \"" + i[2] + "\" is not a number nor a character", line)
            code += ("\t" if i[2] < 0 else " ")
            code += bin(abs(i[2]))[2:].replace("0", " ").replace("1", "\t")
            code += "\n"
        else:
            if ".".join(i[:-1]) in need_arg:
                error("\"" + ".".join(i[:-1]) + "\" needs an argument, but was not given one", line)
    print(code)
