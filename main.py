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

commands = {"exit", "echo", "type", "web", 
            "python", "env", "file", "con", 
            "history", "morph", "git", "curl"}

#history stores as a global list
history = []

#connectivity tester
def connection_scan(command_split, command):
    match len(command_split):
        case 3:
            sock = socket.socket(socket.AF_INET, socket. SOCK_STREAM)
            sock.settimeout(10)
            HOST = socket.gethostbyname(str(command_split[1]))
            PORT = int(command_split[2])

            if not (0 <= PORT <= 65535):
                print(f"{WARNING}Port invalid{RESET} / (Not in range 0/65535)")
                sock.close()
                return

            status = sock.connect_ex((HOST, PORT))
            if status == 0:
                print(f" {command_split[1]} / {GREEN}RESPONDED{RESET}")
            elif status > 0: 
                print(f"{command_split[1]} / {WARNING}UNREACHABLE{RESET}")
            else: 
                print(f"{command_split[1]} / {WARNING}UNREACHABLE{RESET}")
            sock.close()

        case _: 
            if command_split[1] == "range":
                port_scan(command_split, command)
            else: error(command, command_split)

#port scanning
def port_scan(command_split, command):
    input(f"{WARNING}Portscan (localhost) / Press enter to continue{RESET} ")
    match len(command_split):
        case 4:
            LOCALHOST = "127.0.0.1"
            for scan_number in range(int(command_split[2]), int(command_split[3]) + 1):
                sock = socket.socket(socket.AF_INET, socket. SOCK_STREAM)
                sock.settimeout(0.5)
                PORT = scan_number
                status = sock.connect_ex((LOCALHOST, int(PORT)))
                if status == 0:
                    print(f"PORT / {scan_number} / {GREEN}RESPONDED{RESET}")
                elif status > 0: 
                    print(f"PORT / {scan_number} / {WARNING}UNREACHABLE{RESET}")
                else: 
                    print(f"PORT / {scan_number} / {WARNING}UNREACHABLE{RESET}")
                sock.close()
        case _: error(command, command_split)

#executing file
def execute_file(command_split):
    def not_found(command_split):
        print(f"{WARNING}{command_split[1]} file not found in the PATH{RESET}")
        return
    
    if len(command_split) < 2:
        command_split.append(" ")
        execute_file(command_split) 
        return
    
    execute_path = shutil.which(command_split[1])
    if os.access(str(execute_path), os.X_OK) == True:
        input(f"{WARNING}Opening file / Press enter to continue{RESET}")
        print(f"{GREEN}Opening the file /{RESET}", execute_path)
        time.sleep(1)
        subprocess.run(execute_path)

    elif os.access(str(execute_path), os.X_OK) == False:
        not_found(command_split)
    else: not_found(command_split)

def wrapper(command, command_split):
    #curl wrapper
    def curl_wrap(command):
        return os.system(command)
    #git wrap
    def git_wrap(command):
        return os.system(command)
    
    match command_split[0]:
        case "curl":
            curl_wrap(command)
        case "git":
            git_wrap(command)
        case _:
            error(command, command_split)

#opens websites
def open_website(command_split, command):
    input(f"{WARNING}Entering website / Press enter to continue{RESET}")
    
    if len(command_split) < 2:
        command_split.append('127.0.0.1')
        open_website(command_split, command)
    else:
        print(f"{GREEN}Accessing website{RESET} / {command_split[1]}")
        webbrowser.open(command_split[1])
        command_split.clear()
        return

#checking environment variables   
def environ_print(command_split, command):
    match len(command_split):
        case 1:
            envar = os.environ
            pprint.pprint(dict(envar), width=5, indent=5) 
        case _: error(command_split, command)
    return

#error message
def error(command, command_split):
    print(f"{WARNING}", end="")
    match command_split[0]:
        case "type":
            print(f"{command}: not found",sep="")
        case _:
            print(f"{command}: command not found")
            
    print(f"{RESET}", end="")
    return

#exit command
def exit_command(command_split):
    match command_split[0]:
        case "exit":
            sys.exit(0)
        case _:
            error(command_split) 
    return

#type command
def type_command(command_split, command):
    if len(command_split) < 2:
        error(command, command_split)
        return
    
    type_file = shutil.which(command_split[1])
    if command_split[1] in commands:
        print(command_split[1], "is a shell builtin")
        return  
    
    elif command_split[1] != commands and not type_file:
        error(command, command_split)    
        
    else: print(command_split[1],"is", type_file)
    return

#morph one text into another
def morph(command_split):
    morph = list(str(command_split[2]))
    target = list(str(command_split[1]))

    m = len(morph) 
    t = len(target)
    value = m-t
        
    #shift into positive
    if value < 0:
        absolute_value = value * -1
    if value > 0:
        absolute_value = value

    if morph != target:
        for n in range(100):
            if len(morph) != len(target):
                for i in range(absolute_value):

                    if len(target) > len(morph):
                        morph.append(target[i])
                        result = "".join(morph)
                        print(f"{GREEN}{result}{RESET} // +1")

                    if len(target) < len(morph):
                        result = "".join(morph)
                        print(f"{WARNING}{result}{RESET} // -1")
                        morph.pop(-1)

            result = "".join(morph)
            print(f"{GREEN}{result}{RESET} // SHIFT")
            if morph == target:
                print(f"Morph complete // {GREEN}{result}{RESET}")
                return

            if len(morph) == len(target):
                morph[n] = target[n]
            
    else: 
        print("Morph not needed / text already morphed")
        return

#history (work in progress)
def modify_history(command_split):
    match len(command_split):
        case 2:
            if command_split[1] == "clear":
                history.clear()
        case _:
            print(F"\n{GREEN}Command history{RESET}")
            for i in history: print(i)

#executing commands
def command_execute():
    sys.stdout.write(f"{GREEN}$ {RESET}")
    command = input()
    command_split = command.split(" ") 

    history.append(str(command))
    if len(history) == 25:
        history.pop()

    match command_split[0]:
        case "":
            return
        case "python":
            print(sys.version)
        case "type":
            type_command(command_split, command)
        case "echo":
            print(*command_split[1:])
        case "file":
            execute_file(command_split)       
        case "web":
            open_website(command_split, command)
        case "env":
            environ_print(command_split, command)    
        case "con":
            connection_scan(command_split, command)   
        case "curl":
            wrapper(command, command_split)
        case "exit":
            exit_command(command_split)  
        case "history":
            modify_history(command_split)
        case "morph":
            morph(command_split)
        case "git":
            wrapper(command, command_split)
        case _:
            error(command, command_split)

def main():
    date = datetime.datetime.now()
    print(f"{TITLE1}tt-shell{RESET} / {TITLE2}{date}{RESET}")
    while True:
        command_execute()

if __name__ == "__main__":
    main()