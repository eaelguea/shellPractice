## Lab 2: Unix Shell

This second lab tasks us to create a basic shell program to run ona virtual machine or terminal designated to a 
particular OS system. The shell takes basic commands from the user, forks the child process to run that command, and
runs that particular program selected.

### How to Use
The shell, when opened, presents an opening prompt to the user, tasking them to enter the specific bash command to run
on the shell. A couple commands that work are as follows:

~~~
ls
~~~
- presents the list of files in the current directory

~~~
which ls
~~~
- displays the current file path that the user is currently in

~~~
cat output.txt
~~~
- runs and displays the output values on the .txt file

~~~
wc myshell.py > output.txt
~~~
- send the program output to the .txt file

~~~
cat README.md
~~~
- runs and displays the README file

~~~
wc myshell.py
~~~
- displays output of shell program

~~~
exit
~~~
- basic exit prompt to kill the shell

### References
This assignment was prepared in a manner consistent with the instructor's requirements. 
All significant collaboration or guidance from external sources is clearly documented. 

These include:
- p3-execv.py and p4-redirect.py; the shell seen here was built based on the structure of these demo programs 
provided by Dr. Freudenthal.  
- p5-pipe-fork: heavily used for the pipeTheChild() method and the child() method. When the pipe is detected in the 
child: piping read and write and redirecting to the pipe is understood, but they have not yet been modified to 
run programs using the pipe's contents. 

### Bugs
The command `cd` has an issue to where it will not go to a directory specified. This happens also when I create a new
directory and try to go back to that directory. See `def parent()... if 'cd' in args:` for reference.