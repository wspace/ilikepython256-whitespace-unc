#!/usr/bin/env python
import cgi,sys,os
import cgitb
cgitb.enable()
print("Content-Type: text/html")
print("")

def _goto(link, reDir = True, relative=False):
    if(relative):
        i = "'" + link + "'"
    else:
        if(link.startswith("https://") or link.startswith("http://")):
            i = "'" + link + "'"
        else:
            i = "'http://" + link + "'"
    if(reDir):
        print("<script>window.location.replace(" + i + ");</script>")
    else:
        print("<script>window.location = " + i + ";</script>")

def _status(dct,value):
    if(value in dct):
        return dct[value]
    else:
        return False

def _cleanup(raw):
    ret = {}
    raw = raw.replace("+"," ")
    while "%" in raw:
        i = raw.index("%")
        char = chr(int(raw[i+1:i+3],16))
        if(raw[i:i+6] == "%0D%0A"):
            char = ""
        elif(char == "&"):
            char = ""
        elif(char == "="):
            char = ""
        elif(char == "%"):
            char = ""
        raw = raw[:i] + char + raw[i+3:]
    for j in raw.split("&"):
        i = j.replace("","&").replace("","%")
        if("=" in i):
            ret.update({i.split("=")[0].replace("","="):"=".join(i.split("=")[1:]).replace("","=")})
        else:
            ret.update({i:True})
    if(ret == {'':True}):
        ret = {}
    return ret

RAW_POST = sys.stdin.read()
_POST = _cleanup(RAW_POST)

RAW_GET = os.getenv('QUERY_STRING')
_GET = _cleanup(RAW_GET)
#!/usr/bin/env python3
if "code" in _POST:
    args = _POST["code"]
else:
    args = ""
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
need_arg = ["MOD.PUSH", "MOD.COPY", "MOD.SLDE", "FLOW.LABL",
             "FLOW.SUB", "FLOW.JUMP", "FLOW.JMPZ", "FLOW.JMPN"]
print("<link rel='stylesheet' href='https://fonts.googleapis.com/icon?family=Material+Icons'>" +
"<h1>Whitespace Compiler " +
"<a href=\"https://tio.run/#whitespace\"><img alt=\"TryItOnline\" height=30 src=" +
"\"https://avatars3.githubusercontent.com/u/24327566?s=200&v=3\"></a>" +
"<a href=\"WhitespaceHelp.html\"><button>?</button></a></h1>")
print("Commands:<br>")
for i in cmds:
    print("<b>" + i + ": </b>" + ", ".join(cmds[i]) + "<br>")
print("""Examples: <script src="WhitespaceExamples.js"></script>
Code:<br>
<form action="WhitespaceWeb.py" method="post">
    <textarea id="textbox" name="code" rows="12" cols="30">""" + args + """</textarea><br><br>
    <input type="submit" value="Compile!" style="border: dashed">
</form>""")

def error(message, line):
    print("<h3>Error at line " + str(line+1) + " (" + ".".join(i[:-1]) + ("" if i[-1] == None else " " + i[-1]) + "):</h3>")
    print("<p>" + message + "</p>")
    exit()

if args != "":
    file = args
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
    print("""<style>pre {background-color: lightgrey;border: 2px solid black;border-radius: 5px;padding: 5px;}
.space {background-color: blue; color:white;}
.tab {background-color: red;}
.space, .tab {margin-right: 1px;}</style>""")
    tmp = ""
    for i in code:
        if i == " ":
            tmp += "<font class='space'> </font>"
        elif i == "\t":
            tmp += "<font class='tab'>\t</font>"
        else:
            tmp += i
    print("<pre><code>" + tmp + """<br></code></pre>
<button onclick="copy('""" + code.replace("\n", "\\n") + """')"><i class="material-icons">file_copy</i></button>
<span id="copied"></span><br>
<span class='space'>Space</span>
<span class='tab'>Tab</span>""")
