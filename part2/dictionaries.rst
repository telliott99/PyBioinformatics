.. _dictionaries:

############
Dictionaries
############

Lists are great but they have a serious limitation:  they don't scale very well.

If we have a large list of items, it can be hard to tell whether an item is present or not, and to retrieve its associated data if it's a complex object.  If the items have a notion of ordering, then a sorted list can be searched rapidly by binary search but it's still a pain, because when an item is added the list must either be kept in sorted order (or re-sorted).

Dictionaries solve this problem by "hashing" the key to something that allows rapid lookup.

The dictionary is the third fundamental data type in Python after strings and lists.  A dictionary maps keys to values.  For example, one could have the 64 codons as keys to a dictionary whose values are the corresponding amino acids.

If a code segment has a calculation that will be repeated often, one can cache the results of the calculation in a dictionary.

http://docs.python.org/tutorial/datastructures.html#dictionaries

A dictionary can be defined placing just the right something between curly braces (like pairs of key:value):

>>> D = { 'a':1, 'b':2, 'c':3}
>>> D['a']
1
>>> D['d']
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'd'
>>> 'a' in D
True
>>> for k in D:
...     print k, D[k]
... 
a 1
c 3
b 2
>>> D.keys()
['a', 'c', 'b']
>>> D.values()
[1, 3, 2]
>>> D.items()
[('a', 1), ('c', 3), ('b', 2)]
>>> for k,v in D.items():
...     print k,v
... 
a 1
c 3
b 2

Dictionaries are conveniently constructed using a pair of lists joined together with ``zip``, and calling the function ``dict``:

>>> zip('abc',[1,2,3])
[('a', 1), ('b', 2), ('c', 3)]
>>> D = dict(zip('abc',[1,2,3]))
>>> D
{'a': 1, 'c': 3, 'b': 2}

Dictionaries have important restrictions.  The key values must be immutable---so you can't use a list as the key, for example.  However, a list can be converted into a tuple.  Second, the keys should be unique, or rather, if they are not unique the values associated with all but the last instance of the duplicated key will be lost.

>>> D
{'a': 1, 'c': 3, 'b': 2}
>>> D['a']=4
>>> D
{'a': 4, 'c': 3, 'b': 2}

Also, you may have noticed that the order of the keys is not usually the sorted order (or even the input order).  See :ref:`tidbits` for a bit more about this.

>>> L = [1] * 6
>>> D = dict(zip('abcdef',L))
>>> D
{'a': 1, 'c': 1, 'b': 1, 'e': 1, 'd': 1, 'f': 1}
>>> D2 = dict(zip('fedcba',L))
>>> D2
{'a': 1, 'c': 1, 'b': 1, 'e': 1, 'd': 1, 'f': 1}

In a lot of code, you would call ``sort`` on the list of keys before you use them:

>>> L = sorted(D.keys())
>>> for k in L:
...     print k, D[k]
... 
a 1
b 2
c 3

I often use a dictionary as a method to count the number of occurrences of something (nucleotides, codons, etc.).  This simple though perhaps inelegant code does that:

>>> D = dict()
>>> L = list('abcadb')
>>> for k in L:
...     if k in D:
...         D[k] += 1
...     else:
...         D[k] = 1
... 
>>> D
{'a': 2, 'c': 1, 'b': 2, 'd': 1}

If the keys are all known in advance, one can do this:

>>> kL = list('abc')
>>> D = dict(zip(kL,[0]*len(kL)))
>>> D
{'a': 0, 'c': 0, 'b': 0}

And if your version of Python has ``collections``, you can use a ``defaultdict``.

>>> from collections import defaultdict
>>> D = defaultdict(int)
>>> for k in L:
...     D[k] += 1
... 
>>> D
defaultdict(<type 'int'>, {'a': 2, 'c': 1, 'b': 2, 'd': 1})

Oddly, using 0 as the argument (for the default value) won't work.  The reason is that the designers felt that it's nice to be able to use a function to generate the default value, and ``int`` is actually a function.  When called with no argument the result is ``0``:

>>> int()
0

There is also ``Counter``, added to Python 2.7.  See here for a discussion of the :ref:`Counter <Counter-class>` class.

In Python 2.7 and later, you might just use a special type of dictionary called an OrderedDict.

>>> import collections
>>> D = collections.OrderedDict(zip('edcba',range(5)))
>>> for k in D:
...     print k
... 
e
d
c
b
a

An ``OrderedDict`` doesn't sort its keys but it does remember the order in which they were entered.

The Genetic Code is a perfect use case for a dictionary:

.. sourcecode:: python

    def makeCode():
        nt = 'TCAG'
        L = list(nt)
        codons = [n1+n2+n3 for n1 in L for n2 in L for n3 in L]
        aa = 'FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRR' +\
             'IIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG'
        return dict(zip(codons, list(aa)))

    GC = makeCode()
    print GC['GTT']

.. sourcecode:: python

    > python script.py 
    V

This code is fairly condensed.  The fourth line is a list comprehension.  Consider:

>>> Pu = list('AG')
>>> Py = list('TC')
>>> [n1+n2 for n1 in Pu for n2 in Py]
['AT', 'AC', 'GT', 'GC']

This has an outer loop and an inner loop.  The outer loop starts with 'A' and then sequentially generates 'AT' and 'AC' in the inner loop.  It finishes with 'GT' and 'GC'.  Similarly, the fourth line in the function ``makeCode`` is a triple list comprehension.  It generates 64 codons starting from 'TTT' and ending with 'GGG'.

We can use this to translate our protein.  Paste the ``makeCode`` function into the ``utils.py`` file.  Define a new function ``get_seq`` and paste that in ``utils.py`` as well:

.. sourcecode:: python

    def get_seq(fasta_data):
        seq = fasta_data.strip().split('\n', 1)[1]
        seq = ''.join(seq.split())
        return seq

Now we can import all three functions including ``makeCode``, using them like this:

.. sourcecode:: python

    import utils

    data = utils.load_data('mfg.txt')
    seq = utils.get_seq(data)
    GC = utils.makeCode()
    hemA = seq[731:1988]

    R = range(0,len(hemA),3)
    codons = [hemA[i:i+3] for i in R]
    aa = [GC[cod] for cod in codons]
    print ''.join(aa)[:20]

.. sourcecode:: python

    > python script.py 
    MTLLALGINHKTAPVSLRER

A common Python idiom is to do this:

.. sourcecode:: python

    from utils import load_data

or even:

.. sourcecode:: python

    from utils import *

The wild card imports all the names from ``utils``.  With either of these, we can call the function ``load_data`` without qualifying the name:

.. sourcecode:: python

    load_data('mfg.txt')

This is convenient, but can lead to bugs in a more complex project because it's hard to know where a name is actually defined.  Free-floating names also "pollute our namespace" and may shadow another function of the same name imported from a different file, or even one of the standard built-in functions.

*Any* list can be sorted by calling ``sort``.  If the objects are complex, Python may not do what you're expecting.  We'll see that later.

>>> L = list('cba')
>>> L
['c', 'b', 'a']
>>> L.sort()
>>> L
['a', 'b', 'c']

But as we see by reading the docs, or by doing this:

>>> print list.sort.__doc__
L.sort(cmp=None, key=None, reverse=False) -- stable sort *IN PLACE*;
cmp(x, y) -> -1, 0, 1
>>>

sort can take 3 optional named arguments.  One of them is ``key``

>>> def f(c):  
...     return -ord(c)
... 
>>> L
['a', 'b', 'c']
>>> L.sort(key=f)
>>> L
['c', 'b', 'a']

So, if we were perverse enough not to use the argument reverse which is provided for just this purpose (i.e. ``reverse=True``), we could define a function that converts our objects (the strings 'a', 'b', 'c') to integers (97, 98, 99) and then returns them as negative integers (-97, -98, -99).  Since f(c) returns -99 and f(b) returns -98 and -99 < -98, 'c' is sorted in front of 'b' using this function as the key.

We can do more sophisticated things with ``cmp``.  ``cmp`` takes two values to compare, does whatever computation you like, and then returns one of -1, 0, or 1 depending on whether the first argument is logically before, not different in order from, or after the second argument.

Although ``cmp`` is a bit complex  :) in this case it's perfect because the order of the keys in the Genetic Code dictionary is indeterminate.  Further, the order we would like is the traditional one of 'TCAG'.  The problem with using key here is that the codons have 3 nucleotides.  Thus, we need ``cmp``.

.. sourcecode:: python

    import utils

    data = utils.load_data('mfg.txt')
    GC = utils.makeCode()
    kL = GC.keys()
    print kL[:6]

    def codon_comp(x,y):
        for i in range(3):
            j = 'CTAG'.index(x[i])
            k = 'CTAG'.index(y[i])
            if j < k:  return -1
            if k < j:  return 1
        return 0

    kL.sort(cmp=codon_comp)
    print kL[:6]

#-------------------

.. sourcecode:: python

    > python script.py 
    ['CTT', 'TAG', 'ACA', 'ACG', 'ATC', 'AAC']
    ['CCC', 'CCT', 'CCA', 'CCG', 'CTC', 'CTT']

That's some pretty sophisticated sorting.

There is also a built-in function ``sorted`` that works similarly:

>>> L = list('acb')
>>> print sorted(L)
['a', 'b', 'c']

This takes a list as an argument and returns a new, sorted list.

>>> print sorted.__doc__
sorted(iterable, cmp=None, key=None, reverse=False) --> new sorted list
>>>

There is a lot more we can do with the Genetic Code.

Here are two blog posts on point

http://telliott99.blogspot.com/2008/05/fun-with-genetic-code.html

http://telliott99.blogspot.com/2010/12/tracking-evolution-of-coding-sequences.html

.. _set:

**Sets**

Python also has a ``set`` data type.  A set is an unordered collection with no duplicates.  A typical use might be to check that a list has only unique elements:

>>> L = list('abcde')
>>> assert len(set(L)) == len(L)

Let's do some definitions:

>>> S0 = set('ab')
>>> S1 = set('abcde')
>>> S2 = set('efghi')
>>> S3 = set('xyz')

A few examples:

>>> S1 > S0
True
>>> S2.isdisjoint(S3)
True
>>> S1.intersection(S2)
set(['e'])
>>> S1 & S2
set(['e'])
>>> S1 - S2
set(['a', 'c', 'b', 'd'])
>>> S1 ^ S2
set(['a', 'c', 'b', 'd', 'g', 'f', 'i', 'h'])

The first test is whether S1 is a *superset* of S0.  The second is whether S2 and S3 are *disjoint*---i.e. their union is the empty set.  ``&`` is shorthand for ``intersection`` (also ``-`` for ``difference`` and ``^`` for ``symmetric_difference``).

These two are equivalent:

>>> S1 & S2 == S1.intersection(S2)
True

http://docs.python.org/library/stdtypes.html