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

#current directory
script_directory = Path(__file__).parent

#global deque of command history
history = deque(maxlen=35)

#network status
def network_status():
    try:
        socket.create_connection(('8.8.8.8', 53))
        return True
    except Exception:
        return False
    
#general error handler (relic that will be removed / refactored)
def error_handler(command, command_split):
    print(f"{WARNING}Invalid syntax{RESET} <<< {command}")
    return

#bleak bluetooth monitor
async def ble_monitor(command, command_split):
    if len(command_split) == 1:
        print(f"{WARNING}Caution{RESET} >> keyboard interrupt to end monitor")
        print(f"{GREEN}Bluetooth Monitor{RESET} >> Starting")
        try:
            devices = await BleakScanner.discover()
            for device in devices:
                print(f"{device}")
                await asyncio.sleep(0.1)

        except asyncio.CancelledError: raise   
        except KeyboardInterrupt: 
            print(f"{WARNING}KeyboardInterrupt{RESET}")
            return
    
    else: error_handler(command, command_split)

def scan(PORT, sock_data, sock, status):
    if status == 0:
        print(f"Port >>> {PORT} >>> {GREEN}{sock_data[str(status)]}{RESET}")
    if status > 0: 
        print(f"Port >>> {PORT} >>> {WARNING}{sock_data[str(status)]}{RESET}")
    sock.close()
    return

#connectivity tester and port scanner
def connection_portal(command, command_split):
    maximum_port = 65535
    def port_valid(port: int) -> bool:
        return 0 <= port <= maximum_port

    if len(command_split) > 2:
        file_path = script_directory / 'socketErrno.json'
        with file_path.open('r') as file:
            sock_data = json.load(file)

        if command_split[1] == 'range':
            if len(command_split) <= 3:
                print(f"{WARNING}Invalid Arguments{RESET} (3 Given >>> 4 Expected)")
                return

            print(f"{GREEN}Starting Scan From {command_split[2]} To {command_split[3]}{RESET}")
            scanrange_minimum = int(command_split[2])
            scanrange_maximum = int(command_split[3]) + 1
            for port_iterator in range(scanrange_minimum, scanrange_maximum):

                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    LOCALHOST = '127.0.0.1'
                    PORT = int(port_iterator)
                    portscan_state = False

                    if PORT == int(maximum_port):
                        print(f"{GREEN}Scan Succesful{RESET} >>> Returning")
                        portscan_state = True

                    if not port_valid(PORT):
                        print(f"{WARNING}Port ({port_iterator}) Invalid{RESET} (Not In Range)")
                        sock.close()
                        return
                    
                    elif portscan_state == True: return
                    
                    status = sock.connect_ex((LOCALHOST, PORT))
                    scan(PORT, sock_data, sock, status)  

                except KeyboardInterrupt: 
                    print(f"{WARNING}KeyboardInterrupt{RESET}")

        else:   
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)

            try:
                HOST = socket.gethostbyname(str(command_split[1]))
            except socket.gaierror: 
                print(f"{WARNING}socket.gaierror{RESET} / Unable To Open Website")
                return
            
            PORT = int(command_split[2])

            if not port_valid(PORT):
                print(f"{WARNING}Port Invalid{RESET} / (Not In Range 0-65535)")
                sock.close()
                return
            
            print(f"{GREEN}Connnecting To {HOST} From {PORT}{RESET}")
            status = sock.connect_ex((HOST, PORT))
            scan(PORT, sock_data, sock, status) 
            return

    else: 
        error_handler(command, command_split)
        return

#executing file
def execute_file(command, command_split):
    if len(command_split) < 2:
        error_handler(command, command_split)
        return
    
    execute_path = shutil.which(command_split[1])
    if execute_path is None:
        print(f"{WARNING}File Not Found{RESET} >>> ({command_split[1]})")
        return
    
    if os.access(str(execute_path), os.X_OK):
        print(f"{GREEN}Opening File{RESET} >>> ({execute_path})")
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
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)

            HTTPS_PORT = 443
            try: HOST = socket.gethostbyname(str(command_split[1]))
            except socket.gaierror:
                print(f"{WARNING}socket.gaierror{RESET} / Unable To Open Website")
                return
            
            print(f"Connection Test >>> {GREEN}Connection To {HOST} From {HTTPS_PORT}{RESET}")
            status = sock.connect_ex((HOST, HTTPS_PORT))

            if status == 0:
                print(f"Connection Succesful >>> {GREEN}Accessing Website{RESET} >>> {command_split[1]}")
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

#check builtin commands
def type_command(command, command_split):
    def file_check() -> bool:
        if type_file is not None:
            return os.access(type_file, os.X_OK)

    match len(command_split):
        case 2:
            type_file = shutil.which(command_split[1])
            if command_split[1] in commands:
                print(f"{command_split[1]} >>> {commands.get(command_split[1])}")
                return
            if file_check() == True:
                print(f"{command_split[1]} >>> {type_file}")
                return 
            else: 
                error_handler(command, command_split)
                return
        case _: 
            print(f"{WARNING}Invalid Arguments{RESET} (1 given >>> 2 expected)")
            return

#change current working directory
def change_directory(command, command_split):
    if len(command_split) > 1:
        directory = str(command_split[1])

        if command_split[1] == 'reset':
            os.chdir(script_directory)
            return
        if not os.path.exists(directory):
            print(f"{WARNING}No Such Path{RESET} >>> {directory}")
            return
        if not os.path.isdir(directory):
            print(f"{WARNING}No Such Directory{RESET} >>> {directory}")
        
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
    invalid_argument = lambda: print(f"{WARNING}subprocess.CalledProcessError (Invalid Arguments){RESET} >>> {command}")
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
        
#modify and access history deque
def shell_history(command, command_split):
    if len(command_split) == 1:
        if command_split[0] == 'history':    
            print(f"{GREEN} >> Command History{RESET}")
            for element in history:
                print(f">> {element}")

    if len(command_split) == 2:
        if command_split[1] == 'clear':
            history.clear()
            return       
    else: error_handler(command, command_split)
            
#all usable commands
commands = {
    "exit": lambda command, command_split: sys.exit(0),
    "python": lambda command, command_split: print(sys.version),
    "echo": lambda command, command_split: print(*command_split[1:]),
    "com": lambda command, command_split: pprint.pprint(dict(commands), width = 5),
    "ble": lambda command, command_split: asyncio.run(ble_monitor(command, command_split)),
    "git": external_tools,
    "curl": external_tools,
    "type": type_command,
    "web": open_website,
    "env": environ_print,
    "file": execute_file,
    "change": change_directory,
    "con": connection_portal,
    "history": shell_history
}

#executing commands
def command_execute(current_directory):
    sys.stdout.write(f"[{current_directory}]{GREEN} >>> {RESET}")

    try:
        command = input()
        history.append(command)
        if command == '': return
        try: command_split = shlex.split(command) 

        except ValueError: 
            print(f"Exception - {WARNING}ValueError{RESET} - {command}")
            return
        
        for element in range(len(command_split)):
            if len(command_split[element]) >= 63 or len(command) > 1024:
                print(f"{WARNING}Command too long{RESET} => 63 (limit)")
                return
    
        if command_split[0] in commands:
            execute = commands.get(command_split[0], error_handler)
            execute(command, command_split)
        
        else: error_handler(command, command_split)

    except KeyboardInterrupt: 
        print(f"\n{WARNING}KeyboardInterrupt{RESET}")
        return
    
def main():
    date = datetime.datetime.now()
    print(f"{TITLE1}tt-shell [{sys.argv[0]}]{RESET} / {TITLE2}{date}{RESET}")

    try: 
        if not network_status():
            print(f"Network Status >> {WARNING}Offline{RESET}")
        else:
            print(f"Network Status >> {GREEN}Online{RESET}")
            
    except Exception: 
        print(f"{WARNING}Error Fetching Network Status{RESET}")
        
    finally: pass

    while True:
        current_directory = os.getcwd()
        command_execute(current_directory)

if __name__ == "__main__":
    main()