import pprint
import shlex
import time, datetime
import sys, os, shutil
import asyncio
from bleak import BleakScanner
import subprocess, webbrowser
from collections import deque
from pathlib import Path
import socket, json

GREEN = '\033[92m'
TITLE1 = '\033[94m'
TITLE2 = '\033[95m'
WARNING = '\033[91m'
RESET = '\033[0m'

history = deque(maxlen=35)

#general error handler (relic that will be removed / refactored)
def error_handler(command, command_split):
    print(f"{WARNING}Invalid syntax{RESET} <<< {command}")
    return

#bleak bluetooth discover
async def ble_discover(command, command_split):
    if len(command_split) == 1:
        print(f"{WARNING}Caution{RESET} >> keyboard interrupt to end scan")
        print(f"{GREEN}Bluetooth discover{RESET} >> Starting")
        try:
            devices = await BleakScanner.discover()
            for device in devices:
                print(f"{device}")
                await asyncio.sleep(0.2)

        except asyncio.CancelledError: raise   
        except KeyboardInterrupt: 
            print(f"{WARNING}KeyboardInterrupt{RESET}")
            return
    
    else: error_handler(command, command_split)

def shell_directory():
    script_directory = Path(__file__).parent
    return script_directory

#helper functions for connection portal
def socketErrno_reader():
    script_directory = shell_directory()
    file_path = script_directory / 'socketErrno.json'
    with file_path.open('r') as file:
        sock_data = json.load(file)
        return sock_data

def valid_range(PORT: int) -> bool:
    maximum_port = 65535
    return 0 <= PORT <= maximum_port

def socket_initialize(HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(5)
        status = sock.connect_ex((HOST, PORT))
        return status

def scan_initialize(PORT, status):
    sock_data = socketErrno_reader()
    if status == 0:
        print(f"Port >> {PORT} >> {GREEN}{sock_data[str(status)]}{RESET}")
    if status > 0: 
        print(f"Port >> {PORT} >> {WARNING}{sock_data[str(status)]}{RESET}")
    return

#connectivity tester and port scanner   
def connection_portal(command, command_split):
    match len(command_split):
        case 4:
            if command_split[1] == 'range':
                print(f"{GREEN}Starting Scan From {command_split[2]} To {command_split[3]}{RESET}")
                scanrange_min = int(command_split[2])
                scanrange_max = int(command_split[3]) + 1

                for port_iterator in range(scanrange_min, scanrange_max):
                    #this address shouldn't be changed
                    HOST = '127.0.0.1' 
                    PORT = int(port_iterator)

                    if not valid_range(PORT):
                        print(f"{WARNING}Port ({port_iterator}) Invalid{RESET} (Not In Range)")
                        return

                    status = socket_initialize(HOST, PORT)
                    scan_initialize(PORT, status)  
                return

        case 3:
            try: HOST = socket.gethostbyname(str(command_split[1]))
            except socket.gaierror: 
                print(f"{WARNING}socket.gaierror{RESET} / Unable To Find Hostname")
                return
            
            PORT = int(command_split[2])
            if not valid_range(PORT):
                print(f"{WARNING}Port Invalid{RESET} / (Not In Range 0-65535)")
                return
            
            print(f"{GREEN}Connnecting To {HOST} From {PORT}{RESET}")
            status = socket_initialize(HOST, PORT)
            scan_initialize(PORT, status)  
            return
            
        case _: error_handler(command, command_split)

#executing file
def execute_file(command, command_split):
    if len(command_split) < 2:
        error_handler(command, command_split)
        return
    
    execute_path = shutil.which(command_split[1])
    if execute_path is None:
        print(f"{WARNING}File Not Found{RESET} >> ({command_split[1]})")
        return
    
    if os.access(str(execute_path), os.X_OK):
        print(f"{GREEN}Opening File{RESET} >> ({execute_path})")
        time.sleep(1)
        subprocess.run(execute_path, check=True, shell=False)
        return
    
    else: 
        error_handler(command, command_split)
        return

#website opener
def open_website(command, command_split):
    match len(command_split):
        case 2:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(5)

                PORT = 443
                try: HOST = socket.gethostbyname(str(command_split[1]))
                except socket.gaierror:
                    print(f"{WARNING}socket.gaierror{RESET} / Unable To Open Website")
                    return
                
                print(f"Connection Test >> {GREEN}Connection To {HOST} From {PORT}{RESET}")
                status = sock.connect_ex((HOST, PORT))
                if status == 0:
                    print(f"Connection Succesful >> {GREEN}Accessing Website{RESET} >> {command_split[1]}")
                    webbrowser.open(command_split[1])
                    return
                
                else: 
                    print(f"{WARNING}Connection Failed{RESET} / Unable To Open Website")
                    return
        case _: 
            error_handler(command, command_split)
            return
    
#environment variables   
def environ_print(command, command_split):
    if len(command_split) == 1:
        envar = os.environ
        pprint.pprint(dict(envar), width=5, indent=5) 
        return
    else: 
        error_handler(command, command_split)
        return

#builtin commands checker
def type_command(command, command_split):
    def file_check() -> bool:
        if type_file is not None:
            return os.access(type_file, os.X_OK)

    match len(command_split):
        case 2:
            type_file = shutil.which(command_split[1])
            if command_split[1] in commands:
                print(f"{command_split[1]} >> {commands.get(command_split[1])}")
                return
            if file_check() == True:
                print(f"{command_split[1]} >> {type_file}")
                return 
            else: 
                error_handler(command, command_split)
                return
        case _: 
            print(f"{WARNING}Invalid Arguments{RESET} (1 given >> 2 expected)")
            return

#change current working directory
def change_directory(command, command_split):
    script_directory = shell_directory()

    if len(command_split) > 1:
        directory = str(command_split[1])

        if command_split[1] == 'reset':
            os.chdir(script_directory)
            return
        
        if not os.path.exists(directory):
            print(f"{WARNING}No Such Path{RESET} >> {directory}")
            return
        
        if not os.path.isdir(directory):
            print(f"{WARNING}No Such Directory{RESET} >> {directory}")
            return
        
        try: 
            os.chdir(str(directory))
            return
        
        except FileNotFoundError: 
            print(f"Exception - {WARNING}FileNotFoundError{RESET}")
            return
    else: 
        error_handler(command, command_split)
        return

#external tool wrappers 
def external_tools(command, command_split):
    invalid_argument = lambda: print(f"{WARNING}subprocess.CalledProcessError (Invalid Arguments){RESET} >> {command}")
    match command_split[0]:
        case 'curl' | 'git':
            try: 
                subprocess.run(command_split, check=True)
                return
            
            except subprocess.CalledProcessError: 
                invalid_argument()
                return
        case _: 
            error_handler(command, command_split)
            return

#access history deque
def modify_history(command, command_split):   
    if len(command_split) == 1:
        print(f"{GREEN} >> Command History{RESET}")
        for element in history:
            print(f">> {element}")
        return     
    if len(command_split) == 2:
        match command_split[1]:
            case 'clear':
                history.clear()
                return
            case _: error_handler(command, command_split)
    else: error_handler(command, command_split)
            
#all usable commands
commands = {
    "exit": lambda command, command_split: sys.exit(0),
    "python": lambda command, command_split: print(sys.version),
    "echo": lambda command, command_split: print(*command_split[1:]),
    "com": lambda command, command_split: pprint.pprint(dict(commands), width = 5),
    "ble": lambda command, command_split: asyncio.run(ble_discover(command, command_split)),
    "git": external_tools,
    "curl": external_tools,
    "type": type_command,
    "web": open_website,
    "env": environ_print,
    "file": execute_file,
    "change": change_directory,
    "con": connection_portal,
    "history": modify_history
}

#executing commands
def command_execute(current_directory):
    MAX_TOKEN_LENGTH = 63
    sys.stdout.write(f"[{current_directory}]{GREEN} >> {RESET}")

    try:
        command = input()
        history.append(command)
        if command == '': return
        try: command_split = shlex.split(command) 

        except ValueError: 
            print(f"Exception - {WARNING}ValueError{RESET} - {command}")
            return
        
        for element in range(len(command_split)):
            if len(command_split[element]) >= MAX_TOKEN_LENGTH:
                print(f"{WARNING}Command Too Long{RESET} >> 63 (Limit)")
                return
    
        if command_split[0] in commands:
            execute = commands.get(command_split[0], error_handler)
            execute(command, command_split)
        
        else: error_handler(command, command_split)

    except KeyboardInterrupt: 
        print(f"\n{WARNING}KeyboardInterrupt{RESET}")
        return
    
def main():
    print(f">> {GREEN}Connecting{RESET}")
    HOST = '1.1.1.1'
    PORT = 53
    try:
        with socket.create_connection((HOST, PORT)) as s:
            s.settimeout(1)
            print(f"Initial Network Status >> {GREEN}Online{RESET}")
    
    except OSError:
        print(f"Initial Network Status >> {WARNING}Offline{RESET}")

    date = datetime.datetime.now()
    print(f"{TITLE1}tt-shell [{sys.argv[0]}]{RESET} / {TITLE2}{date}{RESET}")
    while True:
        current_directory = os.getcwd()
        command_execute(current_directory)

if __name__ == "__main__":
    main()