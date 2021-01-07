# textc
A system to compile static text files from files and program output.

usage: `textc [-h] [-o OUTPUT] [-n] [-v] [-a] [-e EXCLUDED] [-c CWD] [-d DIRECT] input`

Input files are raw text with executable commands enclosed within backticks. To escape backticks, use a backslash. To escape a backslash, use another backslash. See the src and dst directories for examples.

`-o` specifies the destination for compiled text.

`input` and `output` can be files or directories.

 - If they are both files, `input` will be compiled to `output`
 - If they both directories, `input` will be traversed and each file compiled to `output` with the same directory structure
 - If `input` is a file and `output` is a directory, `input` will be compiled directly insde `output`
 - If `input` is a directory and `output` is a file, an error is produced
 - If `output` does not exist, it will be created to match `input`

In each case, the output will overwrite any existing files.

If `-o output` is omitted, the output will be sent to stdout. 

If `-n` is set, any trailing newline characters produced by a command will be kept. Otherwise, they will be discarded.

If `-v` is set, verbose output will be produced.

If `-a` is set, a prompt will be displayed before overwriting a file.

`-e` specifies a regex used to exclude certain files. Several regexes can be specified using several `-e`s.

`-c` specifies a directory to use as the current working directory for any commands executed during compilation.

`-d` specifies a regex used to directly copy certain files from input to output without performing any compilation

The `CMDDIR` environment variable is made available to any commands executed during compilation. This represents the directory that the command itself resides in (determined by `which`), allowing for use of script-relative paths inside a script.

The `SCRIPTPATH` environment variable is made available to any commands executed during compilation. This represents the path of the script from which the command was called.
