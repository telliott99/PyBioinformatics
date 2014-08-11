.. _listcomp:


##################
List comprehension
##################

Previously we had the problem of finding the positions of all the methionine codons in the translated form of the *mfg* sequence.

Here is a solution:

.. sourcecode:: python

    import utils

    data = utils.load_data('mfg.txt')
    seq = data.strip().split('\n', 1)[1]
    seq = ''.join(seq.split())

    sub = seq[731:1988]
    R = range(0,len(sub),3)
    L = list()
    for i in R:
        triplet = sub[i:i+3]
        L.append(triplet)

    M = 'ATG'
    print L.index(M)
    iL = [i for i in R if sub[i:i+3] == M]
    print iL
    
.. sourcecode:: python

    > python script.py 
    [0, 117, 300, 420, 624, 780, 819, 996]
    
This line

.. sourcecode:: python

    iL = [i for i in R if sub[i:i+3] == M]

is a list comprehension.

http://www.python.org/dev/peps/pep-0202/

**List comprehension**

>>> R = range(10)
>>> R
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> L = [i for i in R]
>>> L
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

The list comprehension is designed to replace these classical functional programming tools:  ``map``, ``filter`` and ``reduce``.  The examples in the tutorial are always good:

http://docs.python.org/tutorial/datastructures.html#functional-programming-tools

``map`` calls a given function on each item in a sequence and returns the list of values

>>> def cube(x):
...   return x**3
... 
>>> L = map(cube, range(1, 11))
>>> L
[1, 8, 27, 64, 125, 216, 343, 512, 729, 1000]

Using list comprehension:

>>> L = [cube(n) for n in range(1,11)]
>>> L
[1, 8, 27, 64, 125, 216, 343, 512, 729, 1000]

``filter`` returns a list of the items from an input sequence for which a function returns ``True``

>>> def f(n):
...     return n % 2 and n % 3
... 
>>> L = filter(f, range(2,25))
>>> L
[5, 7, 11, 13, 17, 19, 23]

Using list comprehension

>>> L = [n for n in range(2,25) if f(n)]
>>> L
[5, 7, 11, 13, 17, 19, 23]

``reduce`` returns a single value constructed by calling the function f on the first two items in the sequence, then on that result plus the third item, and so on:
    
>>> def add(x,y):
...     return x + y
... 
>>> L = reduce(add, range(1,11))
>>> L
55
    
We don't actually need it for this one:

>>> L = sum(range(1,11))
>>> L
55

We can use list comprehension to construct all 64 codons in a simple way:

>>> nt = 'TCAG'
>>> L = [a+b+c for a in nt for b in nt for c in nt]
>>> len(L)
64
>>> L[:3]
['TTT', 'TTC', 'TTA']
>>> L[-3:]
['GGC', 'GGA', 'GGG']

.. _matrix-columns:

**Columns of a matrix**

If you have a 3 x 3 matrix

>>> M = [[ 1, 2, 3], [4, 5, 6], [7, 8, 9]]
>>> M
[[1, 2, 3], [4, 5, 6], [7, 8, 9]]

You *could* use a list comprehension to transpose the matrix:

>>> T = [[row[i] for row in M] for i in [0,1,2]]
>>> T
[[1, 4, 7], [2, 5, 8], [3, 6, 9]]

This is a little weird, but the way to think about it is that the first new row is::

    [row[0] for row in M]

and so on.

A slightly obscure but very useful approach for this particular case is:

>>> T = zip(*M)
>>> T
[(1, 4, 7), (2, 5, 8), (3, 6, 9)]

For a discussion of that see 

http://telliott99.blogspot.com/2008/08/matrix-transposition.html
