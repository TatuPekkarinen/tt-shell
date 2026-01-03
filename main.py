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
script_dir = Path(__file__).parent

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
            print(f"Port / {port_mutable} / {GREEN}{sock_data[str(status)]}{RESET}")
        elif status > 0: 
            print(f"Port / {port_mutable} / {WARNING}{sock_data[str(status)]}{RESET}")
        else: 
            print(f"Port / {port_mutable} / {WARNING}{sock_data[str(status)]}{RESET}")
        sock.close()

    def port_valid(port: int) -> bool:
        return 0 <= port <= 65535

    if len(command_split) > 2:
        file_path = script_dir / 'socket.json'
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

                port_mutable = PORT
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

            port_mutable = PORT
            status = sock.connect_ex((HOST, PORT))
            if status >= 0: scan()
            else: error_handler(command, command_split)
    else: error_handler(command, command_split)

#executing file
def execute_file(command, command_split):
    def not_found(command_split):
        print(f"{WARNING}{command_split[1]} file not found in the PATH{RESET}")
        return
    
    if len(command_split) < 2:
        command_split.append(" ")
        execute_file(command_split) 
        return
    
    execute_path = shutil.which(command_split[1])
    if os.access(str(execute_path), os.X_OK) == True:
        print(f"{GREEN}Opening the file /{RESET}", execute_path)
        time.sleep(1)
        subprocess.run(execute_path)

    elif os.access(str(execute_path), os.X_OK) == False:
        not_found(command_split)
    else: not_found(command_split)

#wrappers 
def wrapper(command, command_split):
    curl_wrap = lambda command : os.system(command)
    git_wrap = lambda command : os.system(command)
    
    match command_split[0]:
        case "curl":
            curl_wrap(command)
        case "git":
            git_wrap(command)
        case _:
            error_handler(command, command_split)

#opens websites
def open_website(command, command_split):
    input(f"{WARNING}Entering website / Press enter to continue{RESET}")
    
    if len(command_split) < 2:
        command_split.append('127.0.0.1')
        open_website(command_split, command)
    else:
        print(f"{GREEN}Accessing website{RESET} / {command_split[1]}")
        webbrowser.open(command_split[1])
        return
    
#morph one text into another
def morph_command(command, command_split):
    morph = list(str(command_split[2]))
    target = list(str(command_split[1]))

    m = len(morph) 
    t = len(target)
    value = m - t
        
    #shift into positive
    if value < 0:
        absolute_value = value * -1
    if value > 0:
        absolute_value = value

    if morph != target:
        for n in range(sys.maxsize**10):
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

#checking environment variables   
def environ_print(command, command_split):
    match len(command_split):
        case 1:
            envar = os.environ
            pprint.pprint(dict(envar), width=5, indent=5) 
        case _: error_handler(command_split, command)
    return

#type command
def type_command(command, command_split):
    def file_check():
        if type_file and os.access(type_file, os.X_OK):
            return True
        else: return False

    type_file = shutil.which(command_split[1])

    if command_split[1] in commands:
        print(f"{command_split[1]} is a builtin command")
        return  
    
    if file_check() == True:
        print(f"{command_split[1]} is at {type_file}")
        return 
    
    else: error_handler(command, command_split)
    return

#history
def modify_history(command, command_split, history):
    match len(command_split):
        case 2:
            if command_split[1] == "clear":
                history.clear()
        case _:
            print(F"\n{GREEN}Command history{RESET}")
            for i in history: print(i)
    return

#all usable commands
commands = {
    "exit": lambda command, command_split: sys.exit(0),
    "python": lambda command, command_split: print(sys.version),
    "echo": lambda command, command_split: print(*command_split[1:]),
    "comms": lambda command, command_split: pprint.pprint(dict(commands), width = 5),
    "type": type_command,
    "web": open_website,
    "env": environ_print,
    "file": execute_file,
    "con": connection_scan,
    "history": modify_history,
    "morph": morph_command,
    "git": wrapper,
    "curl": wrapper,
}

#executing commands
def command_execute():
    sys.stdout.write(f"{GREEN}$ {RESET}")
    command = input()
    command_split = command.split(" ") 
    history.append(command)

    if command_split[0] in commands:
        execute = commands.get(command_split[0], error_handler)
        match command_split[0]:
            case "history":
                execute(command, command_split, history)
            case _:
                execute(command, command_split)
    else: 
        error_handler(command, command_split)


def main():
    date = datetime.datetime.now()
    print(f"{TITLE1}tt-shell{RESET} / {TITLE2}{date}{RESET}")
    while True:
        command_execute()

if __name__ == "__main__":
    main()