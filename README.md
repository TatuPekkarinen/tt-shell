### Minimal Python Shell ###

### Programmed in Python version 3.14.0 ###

Monolithically written Python shell with various functionalities. Using OS-level libraries and subprocesses along with other interesting libraries. Parses with Shlex and it is possible to use Git and Curl with this shell. Usable for actual purposes, open source tinkering or whatever. My first real software project and this has taught me a lot about maintainability, the weight of decisions and technical debt.  

# Security caution
Not intended for any security critical usages. Not production hardened and for educational purposes only.





# tt-shell-python Documentation
All commands are executed from the shell prompt

---

## Running the Shell
```
bash
$ uv run main.py
tt-shell / <timestamp>
[/path/to/tt-shell-python/main.py] => 

```



# Connection Commands
Single Port Connection
```
[/path/to/tt-shell-python/main.py] => con <host> <port>
connecting to <host_ip> from <port>
Port / <port> / RESPONDED
```
Port Range Scan
```
[/path/to/tt-shell-python/main.py] => con range <start_port> <end_port>
Starting scan from <start_port> to <end_port>
Port / 1 / CONNECTION REFUSED
Port / 2 / CONNECTION REFUSED

```

# Bluetooth monitor
Bluetooth monitor
```
[/path/to/tt-shell-python/main.py] => ble
{Bluetooth devices}
=> KeyboardInterrupt
{ends monitoring}
```


# Type Command
Checks if a command is builtin or a system executable
```
[/path/to/tt-shell-python/main.py] => type <command>
<command> => <path or function info>

```

```
[/path/to/tt-shell-python/main.py] => type echo
echo // <function reference>

[/path/to/tt-shell-python/main.py] => type konsole
konsole => /usr/bin/konsole
```



# Echo Command
Prints text to the shell
```
[/path/to/tt-shell-python/main.py] => echo "Hello world!"
Hello world!
```



# Web Command
Opens a website and checks connectivity
```
[/path/to/tt-shell-python/main.py] => web <website>
CONNECTION TEST => Connection to <host_ip> from <port>
CONNECTION SUCCESSFUL => Accessing website / <website>
```



# File Execution
Runs a system file
```
[/path/to/tt-shell-python/main.py] => file <filename>
Opening file => <path_to_file>
```



# Change directory
changes current working directory
```
[/home/--/shell/tt-shell-python] => change /home
[/home] => change reset
[/home/--/shell/tt-shell-python] =>
```



# Command History
View and clear past commands
```
[/path/to/tt-shell-python/main.py] => history
Command history
=> <past commands>
```

```
[/path/to/tt-shell-python/main.py] => history clear
```



# Git Commands
Supports Git commands via wrapper

```
[/path/to/tt-shell-python/main.py] => git
usage: git <command> [<args>]
Common Git commands:
  clone, init, add, mv, restore, rm, bisect, diff, grep, log, show, status,
  backfill, branch, commit, merge, rebase, reset, switch, tag, fetch, pull, push
```



# cURL Wrapper
Supports curl commands
```
[/path/to/tt-shell-python/main.py] => curl <url>
# Example:
[/path/to/tt-shell-python/main.py] => curl google.com
<HTML>...
<TITLE>301 Moved</TITLE>
...
```



# Debugging Commands
com / Lists all available commands
```
[/path/to/tt-shell-python/main.py] => com
{
 'com': <function>,
 'con': <function>,
 'curl': <function>,
 'echo': <function>,
 'env': <function>,
 'exit': <function>,
 'file': <function>,
 'git': <function>,
 'history': <function>,
 'morph': <function>,
 'python': <function>,
 'type': <function>,
 'web': <function>
}
```
env / Displays environment variables
```
[/path/to/tt-shell-python/main.py] => env
{
 'HOME': '<user_home>',
 'PATH': '<env_paths>',
 'SHELL': '/usr/bin/bash',
 'USER': '<username>',
 'VIRTUAL_ENV': '<venv_path>',
 ...
}
```
python / Displays current python version
```
[/path/to/tt-shell-python/main.py] => python
[/path/to/tt-shell-python/main.py] => {python version}
```