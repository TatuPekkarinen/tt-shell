import pprint
import time, datetime
import sys, os, shutil
import subprocess, webbrowser

GREEN = '\033[92m'
TITLE1 = '\033[94m'
TITLE2 = '\033[95m'
WARNING = '\033[91m'
RESET = '\033[0m'

commands = {"exit", "echo", "type", "web", "python", "env", "file"}

#executing file
def exec_file(cmdSpl):
    def not_found(cmdSpl):
        print(f"{WARNING}{cmdSpl[1]}file not found in the PATH.{RESET}")
        return
    
    if len(cmdSpl) == 1:
        cmdSpl.append(" ")
        exec_file(cmdSpl) 
        return
        
    execPath = shutil.which(cmdSpl[1])
    if os.access(str(execPath), os.X_OK) == True:
            print(f"{GREEN}Opening the file /{RESET}", execPath)
            time.sleep(1)
            subprocess.run(execPath)

    elif os.access(str(execPath), os.X_OK) == False:
        not_found(cmdSpl)
    else: not_found(cmdSpl)

#opens websites
def open_web(cmdSpl, cmd):
    if len(cmdSpl) == 1:
        error(cmd, cmdSpl)
    else:
        print(f"{GREEN}Accessing website{RESET} / {cmdSpl[1]}")
        webbrowser.open(cmdSpl[1])
        return

#Checking environment variables   
def environ_check(cmdSpl, cmd):
    envar = os.environ
    pprint.pprint(dict(envar), width=10, indent=10) 
    return

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
    if len(cmdSpl) == 1:
        error(cmd, cmdSpl)
        return
    type_file = shutil.which(cmdSpl[1])
    if cmdSpl[1] in commands:
        print(cmdSpl[1], "is a shell builtin")
        return  
    elif cmdSpl[1] != commands and not type_file:
        error(cmd, cmdSpl)            
    else: print(cmdSpl[1],"is", type_file)
    return

#executing commands
def cmdexec():
    sys.stdout.write(f"{GREEN}$ {RESET}")
    cmd = input()
    cmdSpl = cmd.split(" ") 
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
        case "file":
            exec_file(cmdSpl)
        case _:
            error(cmd, cmdSpl)

def main():
    date = datetime.datetime.now()
    print(f"{TITLE1}tt-shell{RESET} / {TITLE2}{date}{RESET}")
    while True:
        cmdexec()

if __name__ == "__main__":
    main()