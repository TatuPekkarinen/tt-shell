### Minimal Python Shell (WORK IN PROGRESS) ###

### Programmed in Python version 3.14.0 ###

This project is a small command-line shell written in Python. It supports a few basic builtin commands and can also run executable files from the current directory. The goal is to provide a lightweight example of how a shell parses input and decides what to do with it.

Initially a codecrafters challenge I did without AI that includes a couple of differences to the initial challenge. Mostly made for me to tinker with like adding colorization making the file run commands as I actually need them to be alongside other commands that will be added.

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
(c) Microsoft Corporation. Kaikki oikeudet pidätetään.'

(Opens Windows commandline)
```       

### python - outputs current python version ###

```        
$ python
3.14.0 (tags/v3.14.0:ebf955d, Oct  7 2025, 10:15:03) [MSC v.1944 64 bit (AMD64)]
```        
    
### env - prints environment variables ###

```
$ env
(environment variables)
```    

### CODECRAFTERS STARTER CODE ###

```            
import sys
            
def main():
    sys.stdout.write("$ ")
            
if __name__ == "__main__":
    main()
```
