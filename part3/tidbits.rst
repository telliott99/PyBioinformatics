.. _tidbits:

##############
Python Tidbits
##############

**Dictionary keys**

The order of keys in a Python dictionary depends on each key's ``hash`` value.  

There is an explanation from the effbot

http://effbot.org/zone/python-hash.htm

of how the hash is calculated, which seems to be no longer quite correct (probably due to my 64-bit machine).

In any case, the ``hash`` function is designed to give a unique result for each value.  For example:

>>> hash('a')
12416037344
>>> hash('b')
12544037731
>>> hash('c')
12672038114

For a dictionary of a given size, the ``slot`` where a given key's value is stored is computed from the ``hash`` and a mask which is 1 less than the number of slots in the dictionary.  If another object is already stored at the target slot, then additional steps will be taken.

In this example:

>>> L = [1] * 6
>>> D = dict(zip('abcdef',L))
>>> D
{'a': 1, 'c': 1, 'b': 1, 'e': 1, 'd': 1, 'f': 1}
>>> D.keys()
['a', 'c', 'b', 'e', 'd', 'f']
>>> mask = 31
>>> L = [(hash(k) & mask, k) for k in D.keys()]
>>> L.sort()
>>> L
[(0, 'a'), (2, 'c'), (3, 'b'), (4, 'e'), (5, 'd'), (7, 'f')]

The reason why 'c' comes before 'b' in ``D.keys()`` is that 

>>> hash('c') & 31 < hash('b') & 31
True

If you're curious, see Chapter 18 in 'Beautiful Code'.

http://www.amazon.com/gp/product/0596510047

However, the value of ``mask`` will change with a bigger dictionary.  For example, the size of the next dictionary appears to be 1024 since the mask of 1023 gives the expected results.  (And I know from reading that the goal is to have a dictionary about two-thirds full):

>>> from string import lowercase as lc
>>> L = [x + y for x in lc for y in lc]
>>> len(L)
676
>>> D = dict(zip(L,[0]*len(L)))
>>> print D.keys()[:5]
['gw', 'gv', 'gu', 'gt', 'gs']
>>> kL = [(hash(k) & 1023, k) for k in D.keys()]
>>> kL.sort()
>>> print kL[:5]
[(0, 'gw'), (1, 'gv'), (2, 'gu'), (3, 'gt'), (4, 'gs')]
>>> D.keys() == kL
False

I expect that the last equality comparison fails because collisions have forced the implementation to look for new slots for some of the keys.

If you're interested, heed the Python motto:

   Use the source, Luke.
   
The relevant commentary is at the top of ``Objects/dictobject.c``.

More discussion at:

http://www.laurentluce.com/posts/python-dictionary-implementation/

**Flatten a list**

Suppose we have list of lists, say, a two-dimensional array::

    L = [[1,2,3],[4,5,6],[7,8,9]]

And we'd like to generate the flattened list, with all elements at the same (first) level.  ``sum`` will do it:

>>> L = [[1,2,3],[4,5,6],[7,8,9]]
>>> sum(L,[])
[1, 2, 3, 4, 5, 6, 7, 8, 9]

It'll work for strings too:

>>> L = [list('abc'),list('def'),list('ghi')]
>>> L
[['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i']]
>>> sum(L,[])
['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

If the list is nested more deeply or in a mixed way, the above approach fails.  Transforming this 

.. sourcecode:: python

    L = [1, 2, [3, 4], [5, [6, 7]]]

into 

.. sourcecode:: python

    L = [1, 2, 3, 4, 5, 6, 7]

is actually a bit complicated in the general case. .  

However, for this particular situation there *are* easy solutions:

>>> L = [1, 2, [3, 4], [5, [6, 7]]]
>>> s = str(L)
>>> L = [int(n) for n in s if n in '0123456789_']
>>> L
[1, 2, 3, 4, 5, 6, 7]

Another way, that can handle floats:

>>> L = [1.2, 2, [3.14, 4], [5, [6, 7]]]
>>> L2 = [c for c in `L` if not c in '[]']
>>> L3  = list(eval(''.join(L2)))
>>> L3
[1.2, 2, 3.1400000000000001, 4, 5, 6, 7]

The version above uses ``eval`` and the ````` symbol.  For the first, see:

http://docs.python.org/library/functions.html#eval

Here is the second:

>>> L = [1,2,3]
>>> `L`
'[1, 2, 3]'
>>> L.__repr__()
'[1, 2, 3]'

The answers they like best on Stack Overflow for 'flattening'

http://stackoverflow.com/questions/2158395

rely on ``isinstance``:

>>> L = list('abc')
>>> isinstance(L,list)
True
>>> isinstance('abc',str)
True
>>> from collections import Iterable
>>> isinstance(L,Iterable)
True

The solution works better as a function than a generator:

>>> def flatten(L):
...     result = list()
...     for e in L:
...         if hasattr(e, "__iter__") \
...         and not isinstance(e, basestring):
...             result.extend(flatten(e))
...         else:
...             result.append(e)
...     return result
... 
>>> 
>>> L = [1, 2, [3, 4], [5, [6, 7]]]
>>> flatten(L)
[1, 2, 3, 4, 5, 6, 7]

But in general, we don't ask Python objects what kind of object they are.  If it walks like a duck and quacks like a duck, it's a duck.

So if it doesn't quack, just handle the error:

>>> def flatten(L):
...     result = list()
...     for e in L:
...         try:
...             result.extend(flatten(e))
...         except TypeError:
...             result.append(e)
...     return result
...
>>> 
>>> L = [1, 2, [3, 4], [5, [6, 7]]]
>>> flatten(L)
[1, 2, 3, 4, 5, 6, 7]

I don't mind re-defining ``e`` inside a function, but some people wouldn't feel comfortable with that.

Looking ahead to :ref:`numpy`, its arrays have a ``flatten`` method, but a numpy array must be have all rows in a given dimension be the same length, so the above example won't work.  Here is a regular example::

    >>> import numpy as np
    >>> L = range(27)
    >>> A = np.array(L)
    >>> A.shape = (3,3,3)
    >>> A
    array([[[ 0,  1,  2],
            [ 3,  4,  5],
            [ 6,  7,  8]],

           [[ 9, 10, 11],
            [12, 13, 14],
            [15, 16, 17]],

           [[18, 19, 20],
            [21, 22, 23],
            [24, 25, 26]]])
    >>> A.flatten()
    array([ 0,  1,  2,  3, . . .

**Low value ints**

In the following code we use the ``id`` built-in function

http://docs.python.org/library/functions.html#id

    Return the “identity” of an object. This is an integer (or long integer) which is guaranteed to be unique and constant for this object during its lifetime. Two objects with non-overlapping lifetimes may have the same id() value.

    CPython implementation detail: This is the address of the object in memory.

>>> a = 3
>>> b = 3
>>> id(a) == id(b)
True

The low-value integers are pre-assigned to locations in memory in Python.  If you create a new variable with one of these values, you just get a copy, until you change it.

>>> a = 3
>>> b = 3
>>> id(a)
4297110016
>>> id(b)
4297110040
>>> c = 4
>>> id(c)
4297110016
>>> a += 1
>>> id(a)
4297110016

It turns out that the ints between -5 and 255 are special:  they are separated from each other by -24, except there are some jumps of 1952 (which didn't used to be there! before 64-bit):

>>> for i in range(-10,265):
...     diff = id(i+1) - id(i)
...     if diff != -24:
...         print i, diff
... 
-10 -264
-9 144
-8 -264
-7 -360
-6 -268120
35 1952
76 1952
117 1952
158 1952
199 1952
240 1952
256 262312
257 216
258 -144
259 -120
260 -120
261 -120
262 336
264 48

**What is Truth?**

``True`` and ``False`` are keywords in Python.  As a way of emphasizing the difference between assignment and equality testing (remembering that ``hex(id(x))`` gives the address of x):

>>> hex(id(True))
'0x1001163b0'
>>> hex(id(False))
'0x100116390'
>>> True = False
>>> hex(id(True))
'0x100116390'
>>> True == False
True
>>> b = (True == False)
>>> hex(id(b))
'0x1001163b0'
>>> b == False
False
>>>

In the first lines above, we see that ``True`` and ``False`` are ``objects`` with defined locations in memory.  Then, we make the mistake of assigning the label True to the object ``False``.  We were successful as shown by the changed address with ``hex(id(True))``.

The label True is not the real 'True' however, it's only what that label is attached to within the context of our program (our 'namespace').  Thus, the statement 'True == False' evaluates to 'True' because we've redefined the label True as we see it.  Don't do this.  It's a logical nightmare.

**Easter Eggs**

Try this::

    > /opt/local/bin/python2.7
    Python 2.7.1 (r271:86832, Jan  8 2011, 09:26:04) 
    [GCC 4.2.1 (Apple Inc. build 5664)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import antigravity

You'll get something like this (but only with 2.7 or 3.x):

http://xkcd.com/353/

Or try this::

    >>> import this
    The Zen of Python, by Tim Peters

    Beautiful is better than ugly.
    Explicit is better than implicit.
    Simple is better than complex.
    Complex is better than complicated.
    Flat is better than nested.
    Sparse is better than dense.
    Readability counts.
    Special cases aren't special enough to break the rules.
    Although practicality beats purity.
    Errors should never pass silently.
    Unless explicitly silenced.
    In the face of ambiguity, refuse the temptation to guess.
    There should be one-- and preferably only one --obvious way to do it.
    Although that way may not be obvious at first unless you're Dutch.
    Now is better than never.
    Although never is often better than *right* now.
    If the implementation is hard to explain, it's a bad idea.
    If the implementation is easy to explain, it may be a good idea.
    Namespaces are one honking great idea -- let's do more of those!
