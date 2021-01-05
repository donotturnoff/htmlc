# htmlc
A system to compile static HTML pages from files and program output.

usage: `python3 htmlc.py input output`

`input` and `output` can be files or directories. If they are both files, `input` will be compiled to `output`. If they are directories, `input` will be traversed and each file compiled to `output` with the same directory structure.

.htms (HTML Script) files are raw HTML with executable commands enclosed within braces. To escape braces, use a backslash. To escape a backslash, use another backslash. See the htms and html directories for examples.
