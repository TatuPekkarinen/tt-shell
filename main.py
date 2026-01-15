import pprint
import time, datetime
import sys, os, shutil
import subprocess, webbrowser
from collections import deque
from pathlib import Path
import socket, json

GREEN = '\033[92m'
TITLE1 = '\033[94m'
TITLE2 = '\033[95m'
WARNING = '\033[91m'
RESET = '\033[0m'

#current directory
script_directory = Path(__file__).parent

#global deque of command history
history = deque(maxlen=25)

#error handler
def error_handler(command, command_split):
    print(f"{WARNING}{command}: command not found{RESET}")
    return

#connectivity tester and port scanner
def connection_scan(command, command_split):
    def scan():
        if status == 0:
            print(f"Port / {current_port} / {GREEN}{sock_data[str(status)]}{RESET}")
        elif status > 0: 
            print(f"Port / {current_port} / {WARNING}{sock_data[str(status)]}{RESET}")
        else: 
            print(f"Port / {current_port} / {WARNING}{sock_data[str(status)]}{RESET}")
        sock.close()

    def port_valid(port: int) -> bool:
        return 0 <= port <= 65535

    if len(command_split) > 2:
        file_path = script_directory / 'socket.json'
        with file_path.open('r') as file:
            sock_data = json.load(file)

        if command_split[1] == 'range':
            if len(command_split) <= 3:
                print(f"{WARNING}invalid arguments {RESET}: 3 given / 4 expected")
                return

            print(f"{GREEN}Starting scan from {command_split[2]} to {command_split[3]}{RESET}")
            for port_range in range(int(command_split[2]), int(command_split[3]) + 1):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                LOCALHOST = '127.0.0.1'
                PORT = int(port_range)

                if not port_valid(PORT):
                    print(f"Port ({port_range}) invalid / {WARNING}Not in range{RESET}")
                    sock.close()
                    return

                current_port = PORT
                status = sock.connect_ex((LOCALHOST, PORT))
                scan()  

        else:   
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            HOST = socket.gethostbyname(str(command_split[1]))
            PORT = int(command_split[2])

            if not port_valid(PORT):
                print(f"{WARNING}Port invalid{RESET} / (Not in range 0/65535)")
                sock.close()
                return
            
            print(f"{GREEN}connnecting to {HOST} from {PORT}{RESET}")

            current_port = PORT
            status = sock.connect_ex((HOST, PORT))
            if status >= 0: scan()
            else: error_handler(command, command_split)
    else: error_handler(command, command_split)

#executing file
def execute_file(command, command_split):
    if len(command_split) < 2:
        error_handler(command, command_split)
    
    execute_path = shutil.which(command_split[1])
    if os.access(str(execute_path), os.X_OK) == True:
        print(f"{GREEN}Opening the file /{RESET}", execute_path)
        time.sleep(1)
        subprocess.run(execute_path)

    elif os.access(str(execute_path), os.X_OK) == False:
        print(f"{WARNING}{command_split[1]} file not found in the PATH{RESET}")
    else: return

#website opener
def open_website(command, command_split):
    if len(command_split) < 2:
        command_split.append('127.0.0.1')
        open_website(command_split, command)
    else:
        print(f"{GREEN}Accessing website{RESET} / {command_split[1]}")
        webbrowser.open(command_split[1])
        return
    
#morph strings
def morph_command(command, command_split):
    morph = list(str(command_split[2]))
    target = list(str(command_split[1]))

    morph_value = len(morph) 
    target_value = len(target)
    value = morph_value - target_value
        
    #shift into positive
    if value < 0:
        absolute_value = value * -1
    if value > 0:
        absolute_value = value

    if morph is not target:
        for n in range(absolute_value):
            if len(morph) != len(target):
                for iterator in range(absolute_value):

                    if len(target) > len(morph):
                        morph.append(target[iterator])
                        result = "".join(morph)
                        print(f"{GREEN}{result}{RESET} // +1")

                    if len(target) < len(morph):
                        result = "".join(morph)
                        print(f"{WARNING}{result}{RESET} // -1")
                        morph.pop(-1)

            result = "".join(morph)
            print(f"{GREEN}{result}{RESET} // SHIFT")
            if morph == target:
                print(f"Morph complete => {GREEN}{result}{RESET}")
                return

            if len(morph) == len(target):
                morph[n] = target[n]
            
    else: 
        print(f"{GREEN}{morph} <=> {target}{RESET}")
        return

#environment variables   
def environ_print(command, command_split):
    if len(command_split) == 1:
            envar = os.environ
            pprint.pprint(dict(envar), width=5, indent=5) 
    else:  error_handler(command, command_split)
    return

#builtin checker
def type_command(command, command_split):
    def file_check() -> bool:
        if type_file is not None:
            return os.access(type_file, os.X_OK)

    match len(command_split):
        case 2:
            type_file = shutil.which(command_split[1])
            if command_split[1] in commands:
                print(f"{command_split[1]} // {commands.get(command_split[1])}")
                return  

            if file_check() == True:
                print(f"{command_split[1]} => {type_file}")
                return 
            
            else: error_handler(command, command_split)
        case _: print(f"{WARNING}invalid arguments {RESET}: 1 given / 2 expected")

#history
def modify_history(command, command_split):
    if len(command_split) == 2:
        match command_split[1]:
            case 'clear':
                history.clear()
            case _: error_handler(command, command_split)

    if len(command_split) == 1:
        if command_split[0] == 'history':
            print(F"\n{GREEN}Command history{RESET}")
            for element in history: print(f"{GREEN}=>{RESET} {element}")
            return
    return

#all usable commands
commands = {
    "exit": lambda command, command_split: sys.exit(0),
    "python": lambda command, command_split: print(sys.version),
    "echo": lambda command, command_split: print(*command_split[1:]),
    "com": lambda command, command_split: pprint.pprint(dict(commands), width = 5),
    "git": lambda command, command_split: os.system(command),
    "curl": lambda command, command_split: os.system(command),
    "type": type_command,
    "web": open_website,
    "env": environ_print,
    "file": execute_file,
    "con": connection_scan,
    "history": modify_history,
    "morph": morph_command
}

#executing commands
def command_execute():
    sys.stdout.write(f"[{script_directory}]{GREEN} => {RESET}")
    command = input()
    command_split = command.split(" ") 
    history.append(command)

    if command_split[0] == "":
        return

    if command_split[0] in commands:
        execute = commands.get(command_split[0], error_handler)
        execute(command, command_split)
    
    else: error_handler(command, command_split)


def main():
    date = datetime.datetime.now()
    print(f"{TITLE1}tt-shell{RESET} / {TITLE2}{date}{RESET}")
    while True:
        command_execute()

if __name__ == "__main__":
    main()