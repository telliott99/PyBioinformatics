.. _preparation:

###########
Preparation
###########

Python is widely used on all three of the major platforms---Mac OS X, Linux, and Windows.  My goal is to make this a platform-independent presentation.  Which is not to say I'm agnostic, I really like Macs, and I'd love to explain it to you over a beer or two.

If you're working on OS X, you already have Python installed.  It is sometimes called the "System" Python, since it's used by the Operating System.

Similarly Python comes bundled with a standard installation of Linux.  Currently mine is Ubuntu 11.04.  

On Windows, I would recommend installing Linux in a virtual machine (I like Virtual Box), but you can certainly obtain and install Python from python.org.  Get the binary installer.  There is lots of good material on the web for getting going with Python under Windows.  (Note for Windows:  I have used Unix file paths in this book).

It is confusing that Python comes in two major flavors at present, version 2 and version 3.  Since the 3.x series is 'backwards-incompatible' with 2.x, that's a difficulty.  Clearly Python 3 is the future of Python, but it seems that the future is still some distance away from us.

This text uses only Python 2.x, primarily because that's what ships with OS X and Linux, and it's all I've ever used seriously.  However, if you absolutely have to run Python 3.x, there are only a few code-killing differences (especially ``print`` statements).  Read more here:

http://wiki.python.org/moin/Python2orPython3

**Let's begin**

Open up a Terminal (on OS X under Applications > Utilities > Terminal) or another command-line application and enter

.. sourcecode:: python

   > python
   
You should see something like this::

   Python 2.6.1 (r261:67515, Jun 24 2010, 21:47:49) 
   [GCC 4.2.1 (Apple Inc. build 5646)] on darwin
   Type "help", "copyright", "credits" or "license" for more information.
   >>>

The first ``>`` is the "shell prompt", that's the OS telling us it awaits input.  To start Python, I typed ``python`` and hit return.  The interpreter program is then launched;  it prints some information about the version, followed by its own special prompt:  ``>>>``.

If you want to quit the interpreter, just quit Terminal (``CMD-q``) or see the end of this section for another technique.

**Interpreter and command line**

There will be two different types of code in this book, corresponding to two different ways of running Python.

Examples bearing the ``>>>`` symbol are meant to be pasted into the interpreter.  For example, I typed (or you can paste) ``2 + 3`` and then hit return.  


>>> 2 + 3
5

But don't paste the prompt!

Inserting the prompt ``>>>`` will result in an error, specifically at the second '>' symbol;  that's the point at which Python realizes we've made a mistake with our code.

>>> >>> 2 + 3
  File "<stdin>", line 1
    >>> 2 + 3
     ^
SyntaxError: invalid syntax

The interpreter is very convenient for short examples, and it's nice because the output is interleaved with the code, so you can tell what caused a particular bit of output to appear.

But this method has significant limitations, so I'll also run code using a second approach.  When I first launch the Terminal application in OS X, I change directories or ``cd`` to the Desktop.  I can ask where I am by doing ``pwd`` (print working directory) or your prompt may already show the current directory::

    > cd Desktop
    > pwd
    /Users/telliott/Desktop

If I now enter:: 

    > python script.py

Python will execute the instructions in the file ``script.py``, *provided it can find the file*.  

The first place Python looks for files is the directory that the shell was in when Python launched.  If this single line is the listing for ``script.py``::

    print (2 + 3)

and the file is in the Desktop directory ('on' the Desktop), then we'll see this in Terminal::

    > python script.py 
    5
    >

Of course, you can always use a full path such as ``/Users/telliott/Desktop/script.py``, but that's not very convenient.

It's possible to modify Terminal Preferences to always ``cd Desktop`` when it launches.  The default is to stay in your home directory.

There are other ways to execute Python code but I don't use them much and won't talk about them now.  We'll run simple examples in the interpreter, and put anything more substantial into a file.  I'll try to remember to always call that file ``script.py``.  In the examples below, I won't usually identify where we are, but you can tell that it's the interpreter if you see the ``>>>`` prompt, and conversely we're running from the command line if you see ``> python script.py``.

**Plain Text**

I presume you know what plain text is and how to generate a file containing plain text.  You could use TextEdit or another program.  I like `TextMate <http://macromates.com/>`_.  

We can still execute scripts if the file suffix is ``.txt`` (doing ``python script.txt``), but ``.py`` is uniformly used.

The subject of text and its representations is really complex.  We'll nearly always use plain text, a sequence of characters each encoded in a single byte, with the high-value bit set equal to 0.  Read up on ASCII here:

http://en.wikipedia.org/wiki/ASCII

Some ASCII characters are not printable, but often occur in text anyway, where they control the way the text appears.  The ones that cause particular confusion are those that signal a new line (newline).  The confusion arises from the fact that Unix and Windows employ different symbols for a newline.  Also, the pre-historic Mac OS used a third approach (before 1999), but now OS X is just Unix.  

I always use Unix newlines (symbolized as ``\n``) in text.  If you have input from a file and it contains Windows newlines (``\r\n``), you'll have to make adjustments.  You might change your newlines to be Unix-style newlines, by the approach we'll sketch out in the next chapter, or you could just modify the examples.  For example, you could define ``newline = \r\n`` and then substitute ``newline`` for the freestanding ``\n`` in my code.  (If the ``\n``  is embedded in a ``string`` it's more complicated).

Since we're on the subject of text and characters let's do a simple example (in ``script.py``) that looks ahead a few chapters, using a 'loop' to examine all the characters in a ``string`` of text.  We designate ``'abcde'`` as a string by putting quote marks around it.  

By the way, I use single quotes routinely because they're easier to type.  Python allows the use of either single or double quote marks, as long as they match.  In the html and pdf formats the quote mark looks kind of fancy, but the key I press is the usual one, just to the right of the semicolon on my keyboard.

>>> s = 'abc'
>>> for c in s:  
...     print c, ord(c)
... 
a 97
b 98
c 99

We assigned the label ``s`` to refer to a string, which is a single object that contains a sequence of text characters.  Then we loop through each character of the string, assign that value to ``c``, and then print both the value that ``c`` holds as well as its decimal equivalent.  Let's try it again with ``'\n'``

.. sourcecode:: python

    >>> s = 'abc\n'
    >>> for c in s:
    ...     print c, '*', ord(c)
    ... 
    a 97
    b 98
    c 99
    
    10

When we did the print there, we actually got the newline.

To understand this example, start with the idea that each byte in this data specifies a different character.  A byte has 8 bits and so 2e8 (2 to the 8th power) or 256 possible values, numbered starting at 0 and extending to 255.  The decimal or integer value for the character 'a' is 97.  We can use the interpreter to print two other representations:

>>> i = ord('a')
>>> i
97
>>> bin(i)
'0b1100001'
>>> hex(i)
'0x61'

The binary representation of the integer 97 is '01100001'.  Python prints a leading '0b' to identify this as (the string representation of) a binary value, and the left-most zero has also been removed.  That's 

2e6 + 2e5 + 2e0 = 64 + 32 + 1 = 97.  

The hexadecimal representation is identified by a leading '0x' and its value is '61'

6 times 16 + 1 = 97

The statement ``bin(i)`` 'calls' the function ``bin`` (which is pre-defined in Python) and feeds to it the value of the variable ``i`` (the integer 97).  The function gives us back ('returns') a string containing the binary version of the number 97.  We could also have done it without involving the variable as an intermediate:

>>> bin(97)
'0b1100001'

These are not *actual* binary or hexadecimal values.  They are string representations of binary or hexadecimal values.  Much later, we'll work through an example of actually using binary data in Python in :ref:`bytes`.

However, for the most part we'll focus on strings in our programming.  Each string is considered a single character or byte at a time.  Even the Unix newline ``\n`` is really a single byte, the forward slash just indicates that the following 'n' is not really the character n but a special symbol:

>>> ord('\n')
10
>>> ord('n')
110

At this point, we already know enough to understand how Python reads and writes data to files.  We're going to use two more names (these are functions, but we won't worry about the details yet of exactly what a function is), that Python knows about called ``open`` and ``read``.  

There is one file that I'm certain we have available to us if you are actually following along as you should.  It's the ``script.py`` file from before.  In the interpreter:

>>> FH = open('script.py')
>>> data = FH.read()
>>> data
'print 2 + 3'

The first line 'opens' the file for reading.  The second line actually reads the data from the file into a string in memory and assigns the label (variable name) ``data`` to it.  

The third line results in the interpreter printing what is in the data variable.  You don't need an explicit ``print`` in the interpreter, but it is required when using the script method.  It's common to 'examine' the value of variables in the interpreter by just typing the name:

>>> i = 97
>>> i
97
>>> s = 'abcde'
>>> s
'abcde'

The variable ``data`` refers to or 'contains' or 'holds' a string, as indicated by the surrounding single quotes.

There is a bit more to say about the example.  First, it's good practice to close a file after reading:

>>> FH.close()

although Python will close the file for us when it exits.

Second, notice that the very first byte in the file really is the 'p' of our text.  That would not be the case if we used TextEdit to save our file as say, rich text format:

>>> FH = open('script.rtf')
>>> data = FH.read()
>>> data[:40]
'{\\rtf1\\ansi\\ansicpg1252\\cocoartf1038\\coc'

I've used a trick (``data[:40]``) to truncate the output here.  Don't worry about that just yet.

We don't want to deal with meta-data like this when we're programming, unless that's part of our problem statement.  Use plain text.

Finally, it's important to know how to quit the interpreter.  In OS X, the easiest way is to type ``CTL-z``

>>> 
[1]+  Stopped                 python
>

The command we entered doesn't show up on the output, but the single ``>`` indicates that we're back in the shell.  Exactly the same technique will work with a script.  Put this (silly) code into ``script.py`` and then do ``python script.py`` as before::

    while True:
        print 'Hi'

This will never finish without intervention.  Type ``CTL-z``::

    Hi^Z

    [2]+  Stopped                 python script.py
    >

You may want to tidy up by clearing the screen.  In Terminal, that's ``CMD-k`` (``CMD`` is the Apple symbol).  In Linux, do ``clear``.

Although this may look like a lesson it was just a warmup.  Now, we're finally ready to begin.