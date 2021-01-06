# htmlc
A system to compile static HTML pages from files and program output.

usage: `python3 htmlc.py input [-o output] [-n]`

Input files are raw HTML with executable commands enclosed within braces. To escape braces, use a backslash. To escape a backslash, use another backslash. See the htms and html directories for examples.

`-o` specifies the destination for compiled HTML.

`input` and `output` can be files or directories.

 - If they are both files, `input` will be compiled to `output`
 - If they both directories, `input` will be traversed and each file compiled to `output` with the same directory structure
 - If `input` is a file and `output` is a directory, `input` will be compiled directly insde `output`
 - If `input` is a directory and `output` is a file, an error is produced
 - If `output` does not exist, it will be created to match `input`

In each case, the output will overwrite any existing files.

If `-o output` is omitted, the output will be sent to stdout. 

If `-n` is set, any trailing newline characters produced by a command will be kept. Otherwise, they will be discarded.
