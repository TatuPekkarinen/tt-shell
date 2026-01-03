### Minimal Python Shell ###

### Programmed in Python version 3.14.0 ###

This project is a small command-line shell written in Python. It supports a few basic built-in commands and can also run executable files from the current directory. The goal is to give a simple, lightweight example of how a shell parses user input and decides what action to take.

Should work cross platform atleast on Linux and Windows from personal experience.

### LIST OF USABLE COMMANDS WITH EXAMPLES ###

### exit - exits the program ###

```    
$ exit
PS C:\Users\-\tt-shell\tt-shell> 
```    

### type - tells if the file is in the directory or if the command is builtin ###

```        
$ type cmd
cmd is C:\Windows\system32\cmd.EXE
```
```        
$ type echo
echo is a shell builtin
```        

### echo - echoes the text ###

```
$ echo Hello World!
Hello World!
```
        
### web - open websites ###

```
$ web facebook.com
Accessing website / facebook.com
(Opens Facebook.com)¨
```   

### file - executes a given file ###

```        
$ file cmd
Opening the file / C:\Windows\system32\cmd.EXE
Microsoft Windows [Version 10.0.26200.7171]
(c) Microsoft Corporation. Kaikki oikeudet pidätetään.

(Opens Windows commandline)
``` 

### con - TCP connectivity check ###

```
/ connection test

$ con google.com 443
connnecting to 216.58.209.174 from 20
google.com / RESPONDED

```

```
$ con google.com 20
connnecting to 216.58.209.174 from 20
Port / 20 / RESOURCE TEMPORARILY UNAVAILABLE

/ port scan functionality (uses localhost for obvious reasons)

$ con range 0 5
PORT / 0 / UNREACHABLE
PORT / 1 / UNREACHABLE
PORT / 2 / UNREACHABLE
PORT / 3 / UNREACHABLE
PORT / 4 / UNREACHABLE
PORT / 5 / UNREACHABLE
```  

### morph - morph one string into another (I tought this was cool for a moment) ###

```
$ morph hello world
world // SHIFT
horld // SHIFT
herld // SHIFT
helld // SHIFT
helld // SHIFT
hello // SHIFT
Morph complete // hello
```

### history - access past command history ###

```
- history is stored as a list with a cap of 25 max items in history

history 
(prints out command history)

history clear 
(clears history)

```

### WRAPPERS - functionalities outside of the shell ###

```
- supports git commands
- supports cUrl commands
```

### Commands that are for debugging and basically useless for most ###

```
$ comms
{print of the commands dictionary}

$ env
{environment variables}

$ python
3.14.0 (tags/v3.14.0:ebf955d, Oct  7 2025, 10:15:03) [MSC v.1944 64 bit (AMD64)]

```
