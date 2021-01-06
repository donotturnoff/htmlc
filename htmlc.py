import optparse
import os.path
import subprocess
import sys

escapable = ["{", "}", "\\"]
esc = "\\"

def error(msg):
    print("[-] " + msg)
    exit()

def compile(in_path, out_path, dry):
    contents = None
    fin = open(in_path, "r")
    contents = fin.read()
    fin.close()
    if contents == None:
        error("Failed to read " + in_path)

    fout = (open(out_path, "w") if not dry else sys.stdout)
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
    if not dry:
        fout.close() 

def traverse(in_path, out_path, dry):
    if os.path.isfile(in_path):
        compile(in_path, out_path, dry)
    elif os.path.isdir(in_path):
        if not dry and not os.path.exists(out_path):
            os.mkdir(out_path)
        subs = os.listdir(in_path)
        for sub in subs:
            traverse(in_path + "/" + sub, out_path + "/" + sub, dry)
    else:
        error("Could not find " + in_path)

usage = "usage: %prog input [output]"
parser = optparse.OptionParser(usage=usage)
parser.add_option("-d", "--dry-run", action="store_true", dest="dry", default=False, help="Write generated HTML to stdout instead of the specified file")

(opts, args) = parser.parse_args()

if len(args) != 1 and len(args) != 2:
    parser.error("expected 1 required positional argument (input) with one optional positional argument (ouput)")

in_path = args[0]
out_path = "."
if len(args) == 2:
    out_path = args[1]

traverse(in_path, out_path, opts.dry)
