#! /usr/bin/env python3
# Shell Assignment: Eric Elguea
# Due date: 09/22/2019

import os, sys, re, fileinput

opening = "$ "  # opening prompt to mimic any terminal or command line; use for bash command


# parent function that calls upon the child to execute the specific bash commands as specified by the user
def parent():
    global opening
    while True:  # while statement that loops for bash commands by user until command to exit from the shell
        pid = os.getpid()

        if "PS1" in os.environ:
            opening = os.environ["PS1"]

        try:
            args: str = input(opening)
        except EOFError:
            sys.exit(1)

        type(args)

        if args.lower() == "exit":  # exit command kills the working shell; continues if command is left empty or blank
            sys.exit(1)
        elif args == "":
            continue

        args = args.split()  # splits args into functionable commands

        if 'cd' in args:  # should the user enter cd, the director shall change to the new one specified;
            # fails as there is only one directory used on my machine for this lab
            try:
                os.chdir(args[1])
            except FileNotFoundError:
                os.write(2, ("error: %s does not exist\n" % args[1]).encode())
                pass
            continue

        rc = os.fork()  # creates a child process by forking

        # code fragment that handles the forking. See p3-execv.py and p4-redirect.py for reference;
        # included in README.md
        if rc < 0:
            os.write(2, ("Fork has failed. Returning to: %d\n" % rc).encode())
            sys.exit(1)
        elif rc == 0:
            child(args)
        else:
            if '&' in args:
                continue
            else:
                childCode = os.wait()
                if childCode == 0:
                    os.write(2, ("Child program has been terminated. Exit code: %d\n" % childCode).encode())


def child(args):
    pid: int = os.getpid()

    if '>' in args:  # Redirect the output. Reference: p4-redirect.py; see README
        os.close(1)
        sys.stdout = open(args[args.index('>') + 1], "w")
        fd = sys.stdout.fileno()
        os.set_inheritable(fd, True)
        args.remove(args[args.index('>') + 1])
        args.remove('>')

    if '<' in args:
        os.close(0)
        sys.stdin = open(args[args.index('<') + 1], "r")
        fd = sys.stdin.fileno()
        os.set_inheritable(fd, True)
        args.remove('<')

    if '>>' in args:  # basic bash command: append a file in the shell
        os.close(1)
        sys.stdin = open(args[args.index('>>') + 1], "a")
        fd = sys.stdin.fileno()
        os.set_inheritable(fd, True)
        args.remove(args[args.index('>>') + 1])
        args.remove('>>')

    if '&' in args:  # removes the ampersand to kill a process in the shell; speeds up kill
        args.remove('&')

    if '|' in args:  # piping code fragment; see p5-pipe.py and README for reference.
        read, write = os.pipe()

        for i in (read, write):
            os.set_inheritable(i, True)
            os.write(2, ("Pipe: pr=%d pw=%d\n" % (read, write)).encode())
            rc = os.fork()

            if rc < 0:
                os.write(2, "Forking of child has failed.\n".encode())
            if rc == 0:
                pipeTheChild(args, read, write)
            if rc > 0:
                childPid = os.wait()
                os.close(0)
                os.dup(read)
                for fd in (read, write):
                    os.close(fd)

                for inputLine in fileinput.input():
                    os.write(2, ("Pipe child: %s" % inputLine).encode())

    for ch in args[0]:  # searching for a path...
        if '/' in args[0]:
            program = args[0]
            try:
                os.execve(program, args, os.environ)
            except FileNotFoundError:
                pass
            os.write(2, ("Could not execute %s on child: %d \n" % (pid, program)).encode())
            sys.exit(1)

    for directory in re.split(":", os.environ['PATH']):  # No path specified: tries each directory to find the program
        # Reference: p4-redirect.py
        # see README
        program = "%s/%s" % (directory, args[0])  # displays path of program
        try:
            os.execv(program, args)  # runs program
        except FileNotFoundError:
            pass
    os.write(2, ("Child %d: Could not exec %s \n" % (pid, program)).encode())
    sys.exit(1)


# Child pipe method. Writes to the pipe - see README for reference.
def pipeTheChild(args, read, write):
    # only reading and writing to the pipe is occuring; no args are used...
    os.close(1)
    os.dup(write)
    for i in (read, write):
        os.close(i)
    print("Welcome to myShell!")
    sys.exit(1)


parent()
