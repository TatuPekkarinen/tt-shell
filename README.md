Minimal Python Shell

This project is a small command-line shell implemented in Python. It supports a few basic built-in commands and can also run executables from the current directory. The goal is to show, in a simple way, how a shell reads a command, decides what it means, and runs the right action.


Builtin Commands

The shell includes three builtins:

echo – prints the arguments you pass to it.

type – tells you whether a command is a builtin or an external program. If it’s an external program and can be found, it prints the program’s path.

exit – exits the shell with status code 0.


External Commands

If a command starts with "./" the shell treats it as an executable file in the current directory and runs it using Python’s subprocess module.


Error Handling

If a command isn’t a builtin and isn’t a valid executable, the shell prints an error message similar to what a standard shell would print.

CODECRAFTERS STARTER CODE
            
            import sys
            
            def main():
                sys.stdout.write("$ ")
            
            if __name__ == "__main__":
                main()
