Minimal Python Shell

This project is a small command-line shell written in Python. It supports a few basic builtin commands and can also run executable files from the current directory. The goal is to provide a lightweight example of how a shell parses input and decides what to do with it.

Initially a codecrafters challenge I did without AI that includes a couple of differences to the initial challenge. Currently at the process of making this I am reading Python crash course by Eric Mathews and that and most documentation online is my only source of info. Mostly made for me to tinker with like adding colorization making the file run commands as I actually need them to be alongside other commands that will be added.

LIST OF USABLE COMMANDS WITH EXAMPLES

    Exit - exits the program
        $ exit
        PS C:\Users\-\tt-shell\tt-shell> 

    Type - tells if the file is in the directory or if the command is builtin
        $ type cmd
        cmd is C:\Windows\system32\cmd.EXE
        
        $ type echo
        echo is a shell builtin

    Echo - echoes the text (example : echo Hello World!)
        $ echo Hello World!
        Hello World!

    web - open websites
        $ web facebook.com
        Accessing website / facebook.com
        (Opens Facebook.com)

    Prefix "." - executes a given file
        $.cmd
        Opening the file / C:\Windows\system32\cmd.EXE
        Microsoft Windows [Version 10.0.26200.7171]
        (c) Microsoft Corporation. Kaikki oikeudet pidätetään.

        (cmd) C:\Users\-\tt-shell\tt-shell>
            
CODECRAFTERS STARTER CODE
            
    import sys
            
    def main():
        sys.stdout.write("$ ")
            
    if __name__ == "__main__":
        main()
