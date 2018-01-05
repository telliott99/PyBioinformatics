.. _fluent:

##################
Increasing Fluency
##################

This section adds to our knowledge of Python with some very useful but simple constructs that we haven't introduced yet.  It's a bit of a grab-bag, however, they are all important standard parts of the language.

**Comments**

Comments were mentioned earlier.  All the text on a single line following the symbol ``#`` is ignored by Python, which allows the programmer to explain the code if it might be obscure or confusing (especially 6 months from now).  Of course, superfluous comments do not improve things.  The ``#`` may start at the first character, or after an instruction. 

**Extended strings**

We also talked about the fact that simple strings can be delimited with either 'two single quotes' or "two double quotes" but they have to match.  This is useful so as to quote quotes:  ``'He said "Be home soon"'`` (but not ``'He said "I'll be home soon"'``).

There is a third kind of string called a multi-line string.

.. sourcecode:: python

    '''A triple single-quote 
    starts and finishes a multi-line string.'''
    
Real programs should be self-documenting, and most functions (especially from real projects) should have ``docsstrings``.

>>> import math
>>> print math.log.__doc__
log(x[, base]) -> the logarithm of x to the given base.
If the base not specified, returns the natural logarithm (base e) of x.

Doing ``help(x)`` should give useful information about x.  Of course, GIYF.   :)

**Tuple assignment**

We have two (or more) variables:

>>> a = 10
>>> b = 5
>>> print a,b
10 5

>>> temp = a
>>> a = b
>>> b = temp
>>> print a,b
5 10

>>> a,b = b,a
>>> print a,b
10 5

If we want to assign multiple variables at the same time, all the assignments can be at once, as shown on the bottom.  

The middle section is how we might do this in C.  But in Python, we don't need the temporary variable.

**Variable length function arguments**

Here is a common idiom in ``matplotlib`` functions:

.. sourcecode:: python

    def f(*args, **kwargs):
        print args,
        print kwargs

    f()
    L = list('abc')
    f(*L)
    D = dict(zip(L,range(len(L))))
    f(*L,**D)

.. sourcecode:: python

    > python script.py 
    () {}
    ('a', 'b', 'c') {}
    ('a', 'b', 'c') {'a': 0, 'c': 2, 'b': 1}

This method is used to pass a variable number of arguments to a function, either in a list, or a dictionary or both.  Python docs:

http://docs.python.org/tutorial/controlflow.html#more-on-defining-functions

The arguments can be named anything you like.  Also, there can be other, non-variable, arguments preceding these.  

**Command-line arguments**

.. sourcecode:: python

    import sys
    for arg in sys.argv:
        print arg

.. sourcecode:: python

    > python script.py
    script.py
    > python script.py a b c
    script.py
    a
    b
    c

This mechanism is frequently used (for example) to call a script and provide the name of the file that the script should open to find some data.  A fancier but relatively easy mechanism is to use the ``argparse`` module

http://docs.python.org/library/argparse.html#module-argparse

**Assert**

Suppose you have a complicated segment of code, where you think you've anticipated all the cases, so you are absolutely sure that a variable is (say) a list of length 1 at this point.  Just use ``assert`` to tell you when something happens to violate your assumption:

>>> L = [1]
>>> assert len(L) == 1
>>> L.append(0)
>>> assert len(L) == 1
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AssertionError

**Running time**

Usually, you won't need to worry about the effect of small changes in your programs on running time.  If some code takes forever to finish, you will probably need to rewrite it substantially.  However, you might be curious about whether one approach is faster than another.  The ``timeit`` module is for just this situation.

http://docs.python.org/library/timeit.html

For example, I often ``pop`` from the 'front' of a list using ``pop(0)``, rather than reversing it and using ``pop()``.  What is the difference?

.. sourcecode:: python

    > python -m timeit 'N = 100;  L = range(N)' 'while L:' '    L.pop(0)'
    10000 loops, best of 3: 31.8 usec per loop
    > python -m timeit 'N = 1000;  L = range(N)' 'while L:' '    L.pop(0)'
    1000 loops, best of 3: 421 usec per loop
    > python -m timeit 'N = 100;  L = range(N)' 'while L:' '    L.pop()'
    100000 loops, best of 3: 19.3 usec per loop
    > python -m timeit 'N = 1000;  L = range(N)' 'while L:' '    L.pop()'
    10000 loops, best of 3: 195 usec per loop

``pop(0)`` takes a bit longer, and increases a bit faster with ``N``, but it doesn't seem to be a big deal.  To set up more sophisticated tests, save the code in a function in ``script.py`` and then do ``import script`` and call the function.

**Listing a directory**

Suppose you have a directory with files full of sequences, and you don't know exactly how many files there are or even (perhaps) their names.  You just want to grab them all, and load the data.

.. sourcecode:: python

    import os
    p = os.getcwd()
    print p
    L = os.listdir(p + '/project')
    for fn in L:
        print fn

.. sourcecode:: python

    > python script.py
    /Users/telliott/Desktop
    .DS_Store
    _build
    _static
    _templates
    code
    conf.py
    index.rst
    Makefile
    section1
    section2

The first line of output comes from doing ``os.getcwd()`` and printing the result.  We can provide a path to any directory and then list all the files in it.  There may be files you don't want to process, such as the ones that start with '.'.  The file ``.DS_Store`` is present in all directories on OS X.  Just skip it with the string method ``startswith``.


>>> L = ['.DS_Store', 'code']
>>> for e in L:
...     if e.startswith('.'):
...          continue
...     print e
... 
code

**Scope**

Names defined inside a module or function do not mask those outside.  For example:

>>> def plus(x):
...     return x+1
... 
>>> def f(x):
...     def plus(y):
...         return y + 2
...     return plus(x)
... 
>>> plus(2)
3
>>> f(2)
4

The redefinition of ``plus`` inside ``f`` doesn't change what it means outside ``f``.  But be careful when redefining standard names known to Python.  I once called a script ``new.py``, and it caused some problems in a particular library which we'll see later (``matplotlib``).

Similarly, if you're still in the function ``f``, then ``plus`` means what you said it does.

**Functions as objects**

>>> def plus(n):
...     return n + 1
... 
>>> def minus(n):
...     return n - 1
... 
>>> for f in [plus,minus]:
...     f(3)
... 
4
2

In the example above we constructed two functions, then we put them in a list. We took each one at a time and assigned them to the variable ``f`` and then called that function.

We can also pass functions to or receive them back from other functions.  Here is a 'factory' function.

>>> def my_factory(n):
...     def f():
...         return n + 1
...     return f
... 
>>> g = my_factory(5)
>>> g()
6

Here is another rather silly factory function:

>>> import time
>>> def get_timer():
...     t = time.time()
...     def f():
...         return time.time() - t
...     return f
... 
>>> g = get_timer()
>>> g()
1.6319341659545898
>>> g()
3.4238669872283936
>>> g()
8.7889640331268315

There is a lot of magic that can be done with functions in Python, including just to start with, generators and decorators.

http://wiki.python.org/moin/Generators

http://wiki.python.org/moin/PythonDecoratorLibrary

But I think it's best not to worry about all that for now.

**Anonymous functions**

Some people think it's neat that you can define a function without giving it a name, using ``lambda``.  Here is a math example from

http://www.secnetix.de/olli/Python/lambda_functions.hawk

It's the Sieve of Eratosthenes:

>>> L = range(2,50)
>>> for i in range(2,8):
...     L = filter(lambda x: x == i or x % i, L)
... 
>>> L
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

How does this work?  ``filter`` takes a function and a list and filters the list for values where the function returns ``True``.  To begin with L contains 2 . . 49.  In the loop with i = 2 the unnamed function checks whether x == 2 (returning ``True`` for x = 2) or whether ``x % i`` is non-zero.  At each pass through the loop the list is filtered by checking against a different i up till equals 7, the ``sqrt`` of the largest number in the original list.

This code could be criticized on the basis that only the prime numbers need to be checked as divisors (the tests for i = 4 and i = 6 are unnecessary).

I'm not a big fan of lambdas.  Although I like Alonzo Church's work a lot:

http://en.wikipedia.org/wiki/Lambda_calculus

We could just as easily do this:

>>> def f(x):
...     return x == i or x % i
... 
>>> L = range(2,50)
>>> for i in range(2,8):
...     L = filter(f,L)
... 
>>> L
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

**Sorting**

``lambda`` is frequently used for sorting.  Suppose we have three dicts in a list:

>>> O = {'a':1,'x':3}
>>> P = {'a':2,'x':2}
>>> Q = {'a':3,'x':1}
>>> L = [P,O,Q]
>>> L
[{'a': 2, 'x': 2}, {'a': 1, 'x': 3}, {'a': 3, 'x': 1}]

Now let's say we want to sort them:

>>> sorted(L)
[{'a': 1, 'x': 3}, {'a': 2, 'x': 2}, {'a': 3, 'x': 1}]

What has happened is that Python sorted based on the value of the first key.

>>> L[0].keys()
['a', 'x']

What if we wanted to sort based on the value of 'x'?

The ``lambda`` way:

>>> sorted(L, key=lambda o: o['x'])
[{'a': 3, 'x': 1}, {'a': 2, 'x': 2}, {'a': 1, 'x': 3}]

The 'write my own named function' way:

>>> def f(o):
...     return o['x']
... 
>>> sorted(L,key=f)
[{'a': 3, 'x': 1}, {'a': 2, 'x': 2}, {'a': 1, 'x': 3}]

And the way a real Pythonista would use:

>>> from operator import itemgetter as iget
>>> sorted(L, key=iget('x'))
[{'a': 3, 'x': 1}, {'a': 2, 'x': 2}, {'a': 1, 'x': 3}]

Except that they would never rename ``itemgetter``.

A similar syntax can be used with objects.

>>> class MyClass:
...     def __init__(self,s,i):
...         self.myatt = i
...         self.s = s
...     def __repr__(self):
...         return self.s
... 
>>> O = MyClass('O',3)
>>> P = MyClass('P',2)
>>> Q = MyClass('Q',1)
>>> 
>>> L = [Q,O,P]
>>> sorted(L)
[Q, P, O]

Actually, that was unexpected.  I guess Python is too smart for us.  It reached into the object and found ``myatt``, I think.

Anyway, the standard approaches would be, again:

The ``lambda`` way:

>>> L
[Q, O, P]
>>> sorted(L, key=lambda o: o.myatt)
[Q, P, O]

The named function way:

>>> def f(o):
...     return o.myatt
... 
>>> sorted(L, key=f)
[Q, P, O]

And the object attribute getter from ``operator``:

>>> from operator import attrgetter as aget
>>> sorted([O,P,Q], key=aget('myatt'))
[Q, P, O]
>>> sorted(L, key=aget('myatt'))
[Q, P, O]

Operator has a large number of 

    functions implemented in C corresponding to the intrinsic operators of Python
    
http://docs.python.org/library/operator.html

The one that goes with the two we just talked about is ``operator.methodcaller``.  I'm sure you can figure out how to use that one.

**Groups**

In :ref:`dna` (at the end), I showed a simple way of breaking up a sequence into chunks of a fixed size (like n=3):

>>> import string
>>> lc = string.lowercase
>>> n = 3
>>> R = range(0,len(lc),n)
>>> for i in R:
...     print lc[i:i+n]
... 
abc
def
ghi
jkl
mno
pqr
stu
vwx
yz

The 'Pythonic' way to do this is given here:

http://stackoverflow.com/questions/2095637
    
>>> from itertools import izip
>>> L = [iter(lc)]*n
>>> it = izip(*L)
>>> for group in it:
...     print group
... 
('a', 'b', 'c')
('d', 'e', 'f')
('g', 'h', 'i')
('j', 'k', 'l')
('m', 'n', 'o')
('p', 'q', 'r')
('s', 't', 'u')
('v', 'w', 'x')

This is kind of hard to understand, but it works.  The function ``iter`` returns an iterator for a sequence.  We make a list that contains three of them with ``[iter(lc)]*n``.  Somehow, when they are unpacked with ``*L`` and fed to ``izip``, the elements are generated in the correct sequence.

If you use ``izip_longest`` rather than ``izip`` you'll get one additional line of output::

    ('y', 'z', None)