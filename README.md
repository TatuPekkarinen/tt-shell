Minimal Python Shell

This project is a small command-line shell written in Python. It supports a few simple built-in commands and can also run executable files in the current directory. The goal is to provide a lightweight example of how a shell parses input and decides what to do with it.

The shell recognizes three built-ins: echo, type, and exit.

echo prints whatever arguments you give it.

type tells you whether a command is a built-in or an external program, and shows the path if it’s found on the system.

exit quits the shell with status code 0.

Commands starting with ./ are treated as executables located in the working directory and are run using Python’s subprocess module. Anything else that isn’t a built-in or a valid executable results in an error message similar to what a normal shell would print.

Part of the codecrafters challenge but I plan to make this my own thing. No AI usage at all other than for README

STARTER CODE PROVIDED BY CODECRAFTERS

      import sys
      
      def main():
          sys.stdout.write("$ ")
          pass
      
      if __name__ == "__main__":
          main()
