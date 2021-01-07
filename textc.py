#!/usr/bin/env python3

import argparse
import os.path
import subprocess
import sys
import re
from shutil import copyfile

cmd_start = "`"
cmd_end = "`"
esc = "\\"

yes = ["y", "yes"]

parser = argparse.ArgumentParser()
parser.add_argument("input", help="Input file or directory")
parser.add_argument("-o", "--output", action="store", dest="output", help="Write generated text to the given file or directory rather than stdout")
parser.add_argument("-n", "--keep-newlines", action="store_true", dest="keep_newlines", help="Prevent trailing newline being stripped from command output", default=False)
parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", help="Produce verbose output", default=False)
parser.add_argument("-a", "--ask", action="store_true", dest="ask", help="Ask before overwriting file", default=False)
parser.add_argument("-e", "--exclude", action="append", dest="excluded", help="Specify a regex matching files to exclude", default=[])
parser.add_argument("-c", "--cwd", action="store", dest="cwd", help="Set a CWD for all executed commands to use")

args = parser.parse_args()

def ask(msg):
    return input("[?] " + msg)

def info(msg):
    print("[i] " + msg)

def error(msg):
    print("[!] " + msg)
    exit()

def compile(in_path, out_path):
    if args.cwd is None:
        cwd = os.path.split(os.path.abspath(in_path))[0]
    else:
        cwd = os.path.abspath(args.cwd)

    if args.ask and out_path is not None and os.path.exists(out_path):
        if ask("Overwrite " + out_path + "? [y/N] ").lower() not in yes:
            if args.verbose:
                info("Skipping " + in_path + " (overwrite rejected manually)")
            return

    if args.verbose:
        if out_path == None:
            info("Compiling " + in_path)
        else:
            info("Compiling " + in_path + " -> " + out_path)

    contents = None

    fin = None
    try:
        fin = open(in_path, "r")
        contents = fin.read()
    except (PermissionError, IOError) as e:
        error("Failed to read " + in_path + ": " + str(e))
    except UnicodeDecodeError:
        copyfile(in_path, out_path)
        return
    finally:
        if fin is not None:
            fin.close()

    if contents is None:
        error("Failed to read " + in_path)

    fout = None
    try:
        fout = (open(out_path, "w") if out_path is not None else sys.stdout)

        cmd = None
        escaped = False
        for c in contents:
            if c == esc and args.verbose:
                info("Encountered escape character " + esc + " in " + in_path)

            if c == cmd_start and not escaped and cmd == None:
                cmd = ""
            elif c == cmd_end and not escaped and cmd != None:
                cmddir = os.path.split(subprocess.check_output("which \"" + cmd.split()[0] + "\"", cwd=cwd, shell=True, text=True).rstrip("\n"))[0] + "/"
                new_env = os.environ.copy()
                new_env["SCRIPTPATH"] = os.path.abspath(in_path)
                new_env["CMDDIR"] = cmddir
                out = subprocess.check_output(cmd, cwd=cwd, shell=True, text=True, env=new_env)
                if not args.keep_newlines:
                    out = out.rstrip("\n")
                fout.write(out)
                cmd = None
            elif c == esc and not escaped:
                escaped = True
            else:
                escaped = False
                if cmd != None:
                    cmd += c
                else:
                    fout.write(c)

        if out_path is not None:
            fout.close()
    except (PermissionError, IOError) as e:
        error("Failed to write to " + out_path + ": " + str(e))
    except subprocess.CalledProcessError as e:
        error("Failed to execute process " + cmd + " from file " + in_path + ": " + str(e))
    finally:
        if fout is not None and out_path is not None:
            fout.close()

def traverse(in_path, out_path):
    if os.path.isfile(in_path):
        for ex in args.excluded:
            if re.match(ex, in_path):
                if args.verbose:
                    info("Skipping " + in_path + " (matched excluded regex " + ex + ")")
                return
        compile(in_path, out_path)
    elif os.path.isdir(in_path):
        if out_path is not None and not os.path.exists(out_path):
            try:
                os.mkdir(out_path)
            except (PermissionError, IOError) as e:
                error("Failed to create directory " + out_path + ": " + str(e))
        try:
            subs = os.listdir(in_path)
        except (PermissionError) as e:
            error("Failed to read directory listing of " + in_path + ": " + str(e))
        for sub in subs:
            new_in = in_path + "/" + sub
            new_out = out_path + "/" + sub if out_path != None else None
            traverse(new_in, new_out)
    else:
        error("Could not find " + in_path)

in_path = args.input
out_path = args.output

in_f = os.path.isfile(in_path)
out_f = out_path is not None and os.path.isfile(out_path)
in_d = os.path.isdir(in_path)
out_d = out_path is not None and os.path.isdir(out_path)

if in_d:
    if out_f:
        error("Cannot compile directory into file")
    else:
        traverse(in_path, out_path)
else:
    if out_d:
        traverse(in_path, out_path + "/" + os.path.split(in_path)[1])
    else:
        traverse(in_path, out_path)
