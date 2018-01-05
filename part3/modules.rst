.. _modules:

#######
Modules
#######

Python programs can be built from reusable components through the module mechanism.  A module is just a file that contains a segment of code.  Back in :ref:`DNA <dna>` we used this simple function for loading data from a file

.. sourcecode:: python

    def load_data(fn):
        FH = open(fn, ’r’)
        data = FH.read()
        FH.close()
        return data
    
The ``load_data`` operation is so common that instead of writing the same 4-line function function over and over again, we can put it into a file named ``utils.py``, make sure that file is on our ``$PATH``, for example on the Desktop.  Now we can just do an ``import`` in one of three ways:

.. sourcecode:: python

    from utils import load_data
    from utils import *
    import utils
    
Just to be complete, there is another modification of #1 where we give the function a new name::

    from utils import load_data as my_nifty_function
    
The first statement ``from utils import load_data`` gives access to the single name ``load_data``, while the second makes available all the functions (and other variables) defined in ``utils.py``.  With the third, we still need to qualify the function with the module name:

>>> import utils
>>> data = utils.load_data('stuff.txt')

The third option is really nice, because it's clear where the new name comes from in your code.

This basic method works fine, but it can lead to a messy Desktop.  

Python has a standard directory to put user-defined modules called ``site-packages``.  On OS X it is under ``/Library/Python/`` plus more based on the version number.  Let's take a look:

>>> import sys
>>> L = sys.path
>>> for e in L:
...     if e.endswith('site-packages'):
...          print e
... 
/Library/Python/2.6/site-packages

On the most recent Mac OS X (Lion) you may have to use a trick to make the Library directory visible.  Or just use the command line like this:

.. sourcecode:: python

    cp utils.py /Library/Python/2.7/site-packages

My ``utils.py`` file has other useful functions like:

.. sourcecode:: python

    def write_data(fn,data):
        FH = open(fn,'w')
        FH.write(data)
        FH.close()
    
    def reverse_complement(seq):
        import string.maketrans
        tt = maketrans('ACGT','TGCA')
        return seq[::-1].translate(tt)

    def clean_fasta(s):
        title, seq = s.strip().split('\n',1)
        seq = ''.join(seq.strip().split())
        return title, seq

**The name is main**

A standard format for module code is to organize everything into classes or functions, and then have a statement like:

.. sourcecode:: python

    if __name__ == '__main__':
         test()

The code nested under the ``if`` is only executed if the module is run this way:

.. sourcecode:: python

    python my_module.py

If instead we do ``import my_module``, then those functions would be available, but ``test()`` is not run.  Put the following into ``script.py``:

.. sourcecode:: python

    def report():
        print __name__

    if __name__ == '__main__':
        report()

.. sourcecode:: python

    > python script.py
    __main__

>>> import script
>>> script.report()
script
>>>

Every module knows its __name__.  When run by ``python script.py``, it is ``__main__``, but when imported, it is ``script`` without the ``.py``.

**Built-in modules**

We've already employed system-defined modules at various points.  We used the ``string`` module to get ``letters``, and above we did ``import sys`` to get ``sys.path``, which is a list of directories that Python searches when looking for a name it doesn't know about yet.

There are many modules in the Python standard library 

http://docs.python.org/library

Some of the functions defined in the standard library are called 'built-ins'

http://docs.python.org/library/functions.html#built-in-functions

which means that no import is necessary to use them.  There are about 80 of these at latest count.  Others like the ``random`` and ``math`` modules aren't available until import.

Take the brief tour of the standard library sometime.

http://docs.python.org/tutorial/stdlib.html#brief-tour-of-the-standard-library

Let's look at ``math``:

>>> import math
>>> L = [e for e in dir(math) if not e[0] == '_']
>>> while L:
...     print L[:4]
...     L = L[4:]
... 
['acos', 'acosh', 'asin', 'asinh']
['atan', 'atan2', 'atanh', 'ceil']
['copysign', 'cos', 'cosh', 'degrees']
['e', 'exp', 'fabs', 'factorial']
['floor', 'fmod', 'frexp', 'fsum']
['hypot', 'isinf', 'isnan', 'ldexp']
['log', 'log10', 'log1p', 'modf']
['pi', 'pow', 'radians', 'sin']
['sinh', 'sqrt', 'tan', 'tanh']
['trunc']

The one that I'm looking for is ``mean``.  Since doesn't seem to be there, we'll have to define it ourselves:

.. sourcecode:: python

    def mean(L):
        return sum(L)*1.0/len(L)

We can put that into ``utils.py``.

There is an extension of the module mechanism that helps to keep complicated collections of modules more organized.  

Suppose I make a directory Foo on the Desktop (so it's on my $PATH) with two files in it.  The file ``__init__.py`` (which can be empty) lets Python know this directory is a package with modules in the other files.  In the example this is ``bar.py``.  Inside ``bar.py`` I put a print statement ``print 'baz'``.

>>> import os
>>> from Foo.bar import baz
>>> baz()
Hi there
>>> os.listdir('Foo')
['.DS_Store', '__init__.py', '__init__.pyc', 'bar.py', 'bar.pyc']

The files ending in ``.pyc`` are Python ``bytecode``.  Any time you do an import these will be generated.  You can read more about it:

http://effbot.org/zone/python-compile.htm




