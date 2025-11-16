import time
import sys
import shutil
import subprocess
import datetime
import webbrowser
import pprint
import os

GREEN = '\033[92m'
TITLE1 = '\033[94m'
TITLE2 = '\033[95m'
WARNING = '\033[91m'
RESET = '\033[0m'

commands = {"exit", "echo", "type", "web", "python", "env"}

#executing file
def exec_file(execSpl):
    def not_found(execSpl):
        print(f"{WARNING}{execSpl[1]}file not found in the PATH.{RESET}")
        return
    
    execPath = shutil.which(execSpl[1])

    if os.access(str(execPath), os.X_OK) == True:
            print(f"{GREEN}Opening the file /{RESET}", execPath)
            time.sleep(1)
            subprocess.run(execPath)

    elif os.access(str(execPath), os.X_OK) == False:
        not_found(execSpl)
    else:
        not_found(execSpl)

#opens websites
def open_web(cmdSpl, cmd):
    if cmd == "web":
        error(cmd, cmdSpl)
    else:
        print(f"{GREEN}Accessing website{RESET} / {cmdSpl[1]}")
        webbrowser.open(cmdSpl[1])
        return

#Checking environment variables   
def environ_check(cmdSpl, cmd):
    envar = os.environ
    if cmd == "env": 
        pprint.pprint(dict(envar), width=1) 
        return
    elif cmdSpl[1] == "PATH":
        envar = os.environ['PATH']
        pprint.pprint(str(envar)) 
        return
    else: error(cmdSpl, cmd)


#error message
def error(cmd, cmdSpl):
    print(f"{WARNING}", end="")

    match cmdSpl[0]:
        case "type":
            print(f"{cmd}: not found",sep="")
        case _:
            print(f"{cmd}: command not found")

    print(f"{RESET}", end="")
    return

#echo command
def echo_cmd(cmdSpl):
    print(* cmdSpl[1:])
    return

#exit command
def exit_cmd(cmdSpl):
    match cmdSpl[0]:
        case "exit":
            sys.exit(0)
        case _:
            error(cmdSpl) 
    return

#type command
def type_cmd(cmdSpl, cmd):
    if cmd == "type":
        error(cmd, cmdSpl)
        return
    
    type_file = shutil.which(cmdSpl[1])
    if cmdSpl[1] in commands:
        print(cmdSpl[1], "is a shell builtin")
        return  
    elif cmdSpl[1] != commands and not type_file:
        error(cmd, cmdSpl)            
    else: 
        print(cmdSpl[1],"is", type_file)
    return

#executing commands
def cmdexec():
    sys.stdout.write(f"{GREEN}$ {RESET}")
    cmd = input()
    file_prefix = cmd.find(".")
    cmdSpl = cmd.split(" ")
    execSpl = cmd.split(".")

    match cmdSpl[0]:
        case "":
            return
        case "echo":
            echo_cmd(cmdSpl)
        case "exit":
            exit_cmd(cmdSpl)
        case "type":
            type_cmd(cmdSpl, cmd)
        case "web":
            open_web(cmdSpl, cmd)
        case "python":
            print(sys.version)
        case "env":
            environ_check(cmdSpl, cmd)
        case _:
            if  file_prefix == 0:
                exec_file(execSpl)
                return
            elif cmd not in commands:
                error(cmd, cmdSpl)
            else: error(cmd, cmdSpl)

def main():
    date = datetime.datetime.now()
    print(f"{TITLE1}tt-shell{RESET} / {TITLE2}{date}{RESET}")
    while True:
        cmdexec()

if __name__ == "__main__":
    main()