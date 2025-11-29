import pprint
import time, datetime
import sys, os, shutil
import subprocess, webbrowser
import socket

GREEN = '\033[92m'
TITLE1 = '\033[94m'
TITLE2 = '\033[95m'
WARNING = '\033[91m'
RESET = '\033[0m'

commands = {"exit", "echo", "type", "web", "python", "env", "file", "port"}

def connection_scan(cmdSpl):
    s = socket.socket(socket.AF_INET, socket. SOCK_STREAM)
    s.settimeout(10)
    HOST = socket.gethostbyname(str(cmdSpl[1]))
    status = s.connect_ex((HOST, int(cmdSpl[2])))

    if status == 0:
        print(f"{cmdSpl[1]} / {GREEN}RESPONDED{RESET}")
    elif status > 0: 
        print(f"{cmdSpl[1]} / {WARNING}UNREACHABLE{RESET}")
    else: 
        print(f"{cmdSpl[1]} / {WARNING}UNREACHABLE{RESET}")
    s.close()


#executing file
def exec_file(cmdSpl):
    def not_found(cmdSpl):
        print(f"{WARNING}{cmdSpl[1]} file not found in the PATH.{RESET}")
        return
    
    if len(cmdSpl) < 2:
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

#curl wrapper
def curl(cmdSpl):
    input(f"{WARNING}curl system command / press enter at your own risk!{RESET}")

    if len(cmdSpl) < 2:
        cmdSpl.append(" ")
        curl(cmdSpl)
    else: 
        return os.system(f'curl {cmdSpl[1]}')

#opens websites
def open_web(cmdSpl, cmd):
    if len(cmdSpl) < 2:
        cmdSpl.append('http://localhost')
        open_web(cmdSpl, cmd)
    else:
        print(f"{GREEN}Accessing website{RESET} / {cmdSpl[1]}")
        webbrowser.open(cmdSpl[1])
        return

#checking environment variables   
def environ_check():
    envar = os.environ
    pprint.pprint(dict(envar), width=5, indent=5) 
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
    print(*cmdSpl[1:])
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
    if len(cmdSpl) < 2:
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
        case "type":
            type_cmd(cmdSpl, cmd)
        case "echo":
            echo_cmd(cmdSpl)
        case "file":
            exec_file(cmdSpl)       
        case "web":
            open_web(cmdSpl, cmd)
        case "env":
            environ_check()    
        case "con":
            connection_scan(cmdSpl)   
        case "python":
            print(sys.version)
        case "curl":
            curl(cmdSpl)
        case "exit":
            exit_cmd(cmdSpl)   
        case _:
            error(cmd, cmdSpl)

def main():
    date = datetime.datetime.now()
    print(f"{TITLE1}tt-shell{RESET} / {TITLE2}{date}{RESET}")
    while True:
        cmdexec()

if __name__ == "__main__":
    main()