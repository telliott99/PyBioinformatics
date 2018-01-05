.. _sequences:

#########
Sequences
#########

Strings and lists are sequences, collections of objects with a defined linear relationship, that thus have a notion of 'length' for the collection as well as 'order' for the individual items.  'order' leads to 'index', the concept of a slot or location where each item resides.  

The individual elements of a sequence can be accessed using square brackets ``[ ]``.  This is what is technically called the ``getitem`` operator.  

A possibly unexpected feature of the indexing is that we always start counting from 0:

>>> s = 'abc'
>>> s[1]
'b'
>>> s[0]
'a'
>>> L = list(s)
>>> L[0]
'a'

The zero-based indexing derives from the use of pointer arithmetic in C.

http://en.wikipedia.org/wiki/Pointer_(computing)

The variable name given to an array (say A) of a sequence of integers is used as a kind of pointer to the location in memory of the first item.  ``A[0]`` refers to the first element of the array.  To get to the second, do ``A[1]``, etc.  Where ``A[1]`` is equal to ``A + 1``.

We can also count backward from the end:

>>> s = 'abc'
>>> s[-1]
'c'
>>> s[-2]
'b'

It is an error to ask for an index that is not contained in the sequence:

>>> s = 'abc'
>>> s[3]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: string index out of range

We obtain a contiguous subsequence of items with something called a ``slice`` which is the ``getitem`` operator with an additional ``:`` inside  and optionally, indexes:

>>> s = 'abcde'
>>> s[1:3]
'bc'

``s[1:3]`` returned the values at positions 1 and 2 as a list.  It did not return the value at index 3, i.e. it returns up to but not including the index we specified as the sentinel to end the slice.  In math, this is called a half-open interval

http://en.wikipedia.org/wiki/Interval_(mathematics)

If the first index isn't specified we start from the beginning, and if the last index isn't specified we proceed all the way to the end.  We can also do both:

>>> s = 'abcde'
>>> s[:2]
'ab'
>>> s[1:]
'bcde'
>>> s[-2:]
'de'
>>> s[:]
'abcde'

It's a bit perverse, but this works

>>> s[-3:5]
'cde'

We can also use the [ ] operator to *assign* a new value to one or more items in a list:

>>> L = list('abc')
>>> L
['a', 'b', 'c']
>>> L[1] = 'z'
>>> L
['a', 'z', 'c']

A big difference between strings and lists is that the former can't be changed (at least directly).  We say they are 'immutable'.  Trying the same thing we just did but using a string gives an error:

>>> s = 'abc'
>>> s[1] = 'z'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'str' object does not support item assignment

If you really want to do this, you can either convert the data to a list and do the assignment (since lists *are* mutable) and then convert it back to a string again, or assemble the pieces by hand:

>>> t = s[0] + 'z' + s[2]
>>> t
'azc'

Also, you may have noticed that I used the addition operator to concatenate these strings.  This operator is defined for both strings and lists.

The multiplication operator is also defined for use on strings and lists.

>>> L = list('abc')
>>> 2*L
['a', 'b', 'c', 'a', 'b', 'c']
>>> L*2
['a', 'b', 'c', 'a', 'b', 'c']
>>> s = 'abc'
>>> 2*s
'abcabc'
>>> s*2
'abcabc'

One of the operands must be an integer for this to work.