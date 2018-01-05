.. _loops:

#####
Loops
#####

At this point we've introduced functions and the concept of truth testing, and we've worked with strings and lists and seen most of their methods.  Now it's time to fill in the gaps with a few of the other fundamental concepts of the language.  Many of these are logical constructs that control flow.

The most common thing to do with a sequence like a string or a list is to loop through it, grabbing each item and doing something with it.  There are three common idioms

.. sourcecode:: python

    for item in sequence:
        doSomething(item)

    for index in range(len(sequence)):
        item = sequence[index]
        doSomething(item)

    for index,item in iterate(sequence):
        doSomething(item)

The first one is straightforward:

>>> s = 'ACGT'
>>> for c in s:
...     print c
... 
A
C
G
T

The ``len`` of a sequence returns its length, as we saw before.  This length can then be used as a sentry at the end of a range.  Remembering the slice operator:

>>> s = 'ACGT'
>>> n = len(s)
>>> print n
4
>>> print s[1:n]
CGT

``range`` is a versatile function.  In its simplest form it generates all the integers starting at 0 up to but not including its single argument (i.e. the half-open range):

>>> range(6)
[0, 1, 2, 3, 4, 5]
>>> s = 'ACGT'
>>> for i in range(len(s)):
...     print i, s[i]
... 
0 A
1 C
2 G
3 T

``enumerate`` just does the same thing automatically:

>>> s = 'ACGT'
>>> for i,c in enumerate(s):
...     print i, c
... 
0 A
1 C
2 G
3 T

The instruction ``continue`` allows us to quit processing an item and proceed to the next one:

>>> s = 'ACGT'
>>> for c in s:
...     if c in 'CT':
...          continue
...     print c
... 
A
G

The above situation could be handled with ``if`` ``else`` logic (see below), but this is cleaner.

A common operation is to 'group' sequences into chunks.

Probably the best way to do that is to construct an appropriate ``range``

>>> s = 'ATGACCTGCGCCTGA'
>>> delta = 3
>>> N = len(s)
>>> R = range(0,N,delta)
>>> R
[0, 3, 6, 9, 12]
>>> for i in R:
...     print s[i:i+delta]
... 
ATG
ACC
TGC
GCC
TGA

Another common operation is to filter a sequence for items with a specified characteristic.  One way to do that is to start with a second, empty list and 'append' the items we want to save.  (There is an even better way, called a list comprehension, that we'll get to later).

>>> rL = list()
>>> L = list('AGCT')
>>> for i, nt in enumerate(L):
...     if nt == 'A' or nt == 'G':
...         rL.append((i,nt))
... 
>>> print rL
[(0, 'A'), (1, 'G')]

This example is a bit contrived, but it gives me the opportunity to introduce the ``tuple``, which is a relative of the list.  A tuple is a sequence bounded by parentheses (the arguments to a function are a special kind of tuple).  The difference with a list is that a tuple is immutable.  

It's also useful for this example, where we want to save two values together, because ``append`` takes only a single argument so we've grouped two elements together for each ``append`` using the tuple construct.

A second point about this example is the extended expression for the 'if' statement

.. sourcecode:: python

    if nt == 'A' or nt == 'G':

I think it should be obvious what this means.  The first test is

.. sourcecode:: python

    nt == 'A'

If that's true, then we descend into the nested code.  If it's not true, we carry out the second test.

But notice that the order of evaluation of the symbols matters.  Think what would happen if Python tested

.. sourcecode:: python

    if nt == 'A' or nt
    
That's always true!

It can be useful to add parentheses to such a compound statement to make sure it will be evaluated the way you expect

.. sourcecode:: python

    if (nt == 'A') or (nt == 'G'):
    
And here we could just have done

.. sourcecode:: python

    if nt in 'AG':
    
