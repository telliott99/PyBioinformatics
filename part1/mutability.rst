.. _mutability:

##########
Mutability
##########

The fact that lists are mutable and strings are not has the consequence that many list methods change the list in place and do not return any result, while string methods like ``strip`` return a copy of the original string.

>>> s = 'abc '
>>> t = s.strip()
>>>
>>> hex(id(s))
'0x10acd2fc0'
>>> hex(id(t))
'0x10accf580'

Don't worry about how ``hex(id(s))`` works, just notice from its address that t is located in a different place in memory.  It's a copy of what results from modifying the string ``s``.

It's fairly common that I forget to assign the result of a string method: 

>>> s = 'abc '
>>> s.strip()
'abc'
>>> s
'abc '

Oops.  

Or we might do something destructive with a list, but forget to make a copy first.  That can be a tricky bug to find.

The expression ``L[:]``, which we saw previously, is an idiomatic way of obtaining a copy of a list.

Although the addition operator is defined for list operands (and is a rare example of a function used with lists that does return a result):

>>> ['a','b'] + ['c']
['a', 'b', 'c']

it is more common to use the list methods ``append``, ``extend``, ``insert``, and ``pop``:

>>> L = list('abc')
>>> L
['a', 'b', 'c']
>>> L.append('z')
>>> L
['a', 'b', 'c', 'z']
>>> L.pop()
'z'
>>> L
['a', 'b', 'c']
>>> L.pop(0)
'a'
>>> L
['b', 'c']
>>> L.append('j')
>>> L
['b', 'c', 'j']
>>> L.extend(list('xyz'))
>>> L
['b', 'c', 'j', 'x', 'y', 'z']
>>> L.insert(3,'k')
>>> L
['b', 'c', 'j', 'k', 'x', 'y', 'z']

This works but is probably not what you want:

>>> L = list('abc')
>>> L.append(list('xyz'))
>>> L
['a', 'b', 'c', ['x', 'y', 'z']]

The appended list is a sub-list.  L is a list with 4 items, the first three are strings of length one, and the last is a list.  This also points up the perhaps surprising property that Python lists do not have to be homogeneous elements:

>>> L = [1, 2, 3,'infinity']
>>> L
[1, 2, 3, 'infinity']

Yet another handy list method is ``reverse``:

>>> L = list('abc')
>>> L
['a', 'b', 'c']
>>> L.reverse()
>>> L
['c', 'b', 'a']

Notice that the reverse function did not return anything (nothing was printed in the interpreter).  L was modified in place instead.

There is a very slick and idiomatic way to reverse a string:

>>> s = 'abc'
>>> s[::-1]
'cba'