from pprint import pprint
import sys 

commands = {
    "exit": lambda command, command_split: sys.exit(0),
    "python": lambda command, command_split: print(sys.version),
    "echo": lambda command, command_split: print(*command_split[1:]),
    "com": lambda command, command_split: pprint.pprint(dict(commands), width = 5),
    "ble": bleak_adapter,
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