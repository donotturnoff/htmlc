import optparse
import os.path
import subprocess

escapable = ["{", "}", "\\"]
esc = "\\"

def error(msg):
    print("[-] " + msg)
    exit()

def compile(in_path, out_path):
    contents = None
    with open(in_path, "r") as fin:
        contents = fin.read();
    if contents == None:
        error("Failed to read " + in_path)
    with open(out_path, "w") as fout:
        cmd = None
        escaped = False
        for c in contents:
            if c == "{" and not escaped and cmd == None:
                cmd = ""
            elif c == "}" and not escaped and cmd != None:
                out = subprocess.check_output(cmd, shell=True, text=True).rstrip("\n")
                fout.write(out)
                cmd = None
            elif c == "\\" and not escaped:
                escaped = True
            else:
                escaped = False
                if cmd != None:
                    cmd += c
                else:
                    fout.write(c)

def traverse(in_path, out_path):
    if os.path.isfile(in_path):
        compile(in_path, out_path)
    elif os.path.isdir(in_path):
        if not os.path.exists(out_path):
            os.mkdir(out_path)
        subs = os.listdir(in_path)
        for sub in subs:
            traverse(in_path + "/" + sub, out_path + "/" + sub)
    else:
        error("Could not find " + in_path)

usage = "usage: %prog input output"
parser = optparse.OptionParser(usage=usage)

(opts, args) = parser.parse_args()

if len(args) != 2:
    parser.error("expected two arguments (input and output)")

in_path = args[0]
out_path = args[1]

traverse(in_path, out_path)
