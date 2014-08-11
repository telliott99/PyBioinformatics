.. _unix:

############
Command Line
############

**Unix spoken here**

We've been working from the command line since the beginning, but now I want to focus in this section on the general Unix environment.  We won't be doing much that is Python-specific here. 

The 'shell' is the standard way for programmers to interact with the computer.  It's possible, indeed normal, for a system administrator to configure and maintain a "headless" server (with no monitor) at a distance, over an LAN or even from another continent via the web, by using the command line and the shell.  

The default shell in OS X is ``bash``---it's a shell, as well as a scripting language.  It's important to get comfortable moving around the directory structure in the shell.  The basic commands are ``cd``, ``pwd`` and ``ls``::

    > pwd
    /Users/telliott
    > cd Desktop
    > pwd
    /Users/telliott/Desktop
    > cd project/
    > ls
    Counter.py      add to errors.txt
    Makefile        conf.py
    _build          index.rst
    _static         section1
    _templates      section2
    > cd ..
    > pwd
    /Users/telliott/Desktop

``cd`` with no argument sends me to the 'home' directory for my account.  ``cd some_path`` sends me to the specified directory.  Paths come in two flavors, 'relative' and 'absolute'.  An absolute path is specified from the root of the file system and starts with the path separator symbol (in Unix it is ``/``).  A relative path is specified with respect to the current directory, and does not start with ``/``.

An example of an absolute path for me would be ``/Users/telliott/Desktop``.  ``pwd`` prints the working directory.  ``ls some_path`` lists the contents of the given path (or the current directory is the default when no path is given).  Frequently one does ``ls -al`` to give additional information::

    > ls -al
    total 72
    drwxr-xr-x  13 telliott  staff   442 Sep  5 10:56 .
    drwx------+ 35 telliott  staff  1190 Sep  5 10:57 ..
    -rw-r--r--@  1 telliott  staff  6148 Sep  5 09:56 .DS_Store
    -rw-r--r--@  1 telliott  staff  6300 Sep  5 09:56 Counter.py
    -rw-r--r--@  1 telliott  staff  3160 Sep  3 16:21 Makefile
    ..

A shorthand notation is available for absolute paths starting with your home directory.  The symbol ``~`` (tilde) means the same as ``/Users/telliott``::

    > echo ~
    /Users/telliott


I want to show how to install and run a simple program.  We'll also 'build' a piece of software written in C.  To run or execute software, it must have the appropriate 'permissions'.  An example is shown in the above output, where each entry like::

    -rw-r--r--@  1 telliott  staff  6300 Sep  5 09:56 Counter.py

starts with 11 symbols (1 + 3 + 3 + 3 + 1).  The first is a notation as to whether the 'file' is a directory.  The next 3 groups of 3 are permissions in order (read, write, execute) for that file for the current user (me), my 'group', or everyone (the 'world').  Let's not worry about the last symbol for now.

A link to the FTP server that has the 'legacy' BLAST executables is on this page

http://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download

There is a new collection of BLAST programs, but for now we'll stick with what we know.

I downloaded and unzipped the appropriate one for my machine, and then copied the whole thing into the directory named ``bin``, which is directly under my home directory.  (Note:  an experienced Unix user would probably just put things into ``/usr/local/bin`` so that it would be available to all users of the machine.)

I actually did this a while ago so the version is not the latest BLAST that's available::

    > ls ~/bin/blast-2.2.22/bin
    bl2seq      copymat      impala      seedtop
    blastall    fastacmd     makemat     y.txt
    blastclust  formatdb     megablast
    blastpgp    formatrpsdb  rpsblast

Now, we could run one of these programs by giving the complete path to the file::

    > ~/bin/blast-2.2.22/bin/blastall

    blastall 2.2.22   arguments:
    ..

But it's more convenient to be able to just give the program name, and also to issue the command regardless of what directory we're in.  The way I do that is I have a file in my home directory called ``.bash_profile``.  We use the command ``cat`` to look at the contents of that file::

    > cat ~/.bash_profile 
    PATH=$HOME/bin:$PATH;  export PATH
    PS1="> ";  export PS1

``.bash_profile`` isn't visible in the Finder (it's a hidden file that is marked with a 'dot':   ``.``  The commands in ``.bash_profile`` are executed by the shell when I first launch Terminal.  The initial line adds the directory ``~/bin`` to my ``$PATH``.  Now, when the shell is looking for a file or trying to figure out how to run some command I've given, it will search for the name in ``~/bin`` first.

Editing invisible files is a little tricky.  One can use a shell editor like ``nano``, but another way to do it is to copy the file to a name that is visible, edit it in the usual way with TextEdit or whatever, and then copy it back where it belongs.::

    > cp ~/.bash_profile ~/Desktop/x.txt
    
Edit, then::

    > mv ~/Desktop/x.txt ~/.bash_profile
    
``cp`` makes a copy, ``mv`` removes the old one and moves it to the new location.
    
If the file doesn't exist yet, you can make a new one.

An import thing is that you get no second chances.  So if you ``cp`` and the destination already contains a file of that name, you are out of luck.  The old one is just gone.

To run our software program, the second thing we need to do is to 'link' the short name for the program of interest to a name in the ``bin`` directory.  For this example we do::

    > ln -s ~/bin/blast-2.2.22/bin/blastall ~/bin/blastall

Now, we can be in any directory and issue the command::

    > blastall

and the shell will run the ``blastall`` executable, which still resides at ``~/bin/blast-2.2.22/bin/blastall``.  You can see these links all over the file system.  I won't show it because the paths are so long but try ``ls -al /usr/bin/py*``.  (The * is a 'wildcard'.  It matches 0 or more characters).

Issuing ``blastall`` command won't actually do us much good yet.  We need to have a database (and format it) before this really works.  Save the following to a file ``db.txt`` on the Desktop::

    >A
    ACGTACGTACGTACGTACGT

    >B
    AAAAAAAAAAGGGGGGGGGG

    >C
    TCGATCGATCGATCGATCGA
    
Now do the following::

    > ln -s ~/bin/blast-2.2.22/bin/formatdb formatdb
    > formatdb -i db.txt -p F
    
Place the following sequence into another file ``x.txt``::

    >X
    ACGTGCGTACGTACGTACGT
    
Run this command from the Desktop::
    
    blastall -p blastn -i x.txt -d ~/Desktop/db.txt -m 1
    
A part of the output is::

    1_0 1  acgtgcgtacgtacgtacgt 20
    0   1  ....a............... 20
    0   20 ....a............... 1
    
I think that's got to be a homolog.

There is much more to say about how to run BLAST conveniently, but I'll save it for a later chapter.

Now, it's time to build some software.  Building requires a C compiler.  The best way to get one on OS X is to install the Developer's Tools.

http://developer.apple.com/technologies/tools/

On Linux, you should have ``gcc``.  You could just get that for OS X too if you wanted, but everyone uses Apple's tools.

http://telliott99.blogspot.com/2011/07/matplotlib-on-os-x-lion-revised.html

.. _FastTree:

**FastTree**

I'll use FastTree as an example

http://www.microbesonline.org/fasttree

We get the source code (in the C language) from this page

http://www.microbesonline.org/fasttree/#Install

Make sure to save it as ``FastTree.c``.

We also notice some 'build' instructions for OS X on the install page, which we copy into the command below.  You always want to pay attention to those. . .

We're in the Desktop directory, and have ``FastTree.c`` there.  We run this command::  

    > gcc -lm -O3 -finline-functions -funroll-loops -Wall -o FastTree FastTree.c
    
Look and see when it's done::

    > ls -al F*
    -rwxr-xr-x  1 telliott_admin  staff   333184 Sep  5 13:00 FastTree
    -rw-r--r--@ 1 telliott_admin  staff   378270 Sep  5 12:58 FastTree.c
    > ./FastTree 
    Usage for FastTree version 2.1.4 SSE3:
      FastTree protein_alignment > tree
      FastTree -nt nucleotide_alignment > tree
      FastTree -nt -gtr < nucleotide_alignment > tree . . .
      
Notice the required usage:  ``-nt``
    
It just works.  Now copy the executable into ``~/bin`` and link to it as we did before.  Run it from anywhere.

Before we leave this topic I want to talk briefly about shell scripting.  After all, that is Python's heritage.  If we have code in a textfile and the file has its permissions set to be executable, then we can try to execute by simply doing::

    ./script.py

Here is an example.  We put this into ``script.py``::

    #! /usr/bin/python
    print 'Hello world!'

and do the above from the command line::
 
    > ./script.py
    Hello world!

As you can see, the shell executed that script.  One weird thing is that the full path to Python is required.

From Python, we can do everything the shell can do, as I'll show you later, but sometimes it seems easier to just issue a shell command, or even a short sequence of the them.  As an example, I was tracking down a bug in the process of converting this document to a pdf.  

Unimaginatively, I was doing a version of caveman debugging, in which I rip out chunks of code until the problem goes away, then put them back until it appears again.  The complication was that there is a series of commands to do the build, and moreover, the test isn't really valid unless the ``_build`` directory is built fresh for each new round.  So I put the whole series of commands into the file ``script.sh``::

    #!/bin/bash

    cd ~/Desktop/project
    rm -r ~/Desktop/project/_build
    make html
    make latex
    cd ~/Desktop/project/_build/latex
    make all-pdf
    cp ~/Desktop/project/_build/latex/PythonforBioinformatics.pdf ~/Desktop/
    cd ~/Desktop/project

and now each time I want to test a new change I just issue this command::

    > ./script.sh
    
After it's done, I can look at the new pdf to check the changes, and proceed accordingly.

Here is a more extensive selection about Unix stuff.

http://telliott99.blogspot.com/search/label/Unix

