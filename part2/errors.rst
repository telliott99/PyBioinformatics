.. _errors:

######
Errors
######

There are several different types of errors in computer programming.  

It's pretty obvious when you write code, that you're dealing with these two types right from the beginning---although they can blur together.

The first happens when Python detects an error condition during execution

>>> 1/0
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ZeroDivisionError: integer division or modulo by zero
>>> L = list('abc')
>>> L.index('d')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: list.index(x): x not in list
>>> L[5]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: list index out of range
>>> D = {'a':1}
>>> D['b']
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'b'
>>> if True print 'x'
  File "<stdin>", line 1
    if True print 'x'
                ^
SyntaxError: invalid syntax
>>> print c
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'c' is not defined
>>> 2 + '2'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for +: 'int' and 'str'

Each one shows the line number on which the error occurred.  That's not much help here, but when we're doing

.. sourcecode:: python

    python script.py

it's a big help.  Also, if you look carefully at the SyntaxError example, notice the caret in the line, showing the point where Python diagnosed a problem

.. sourcecode:: python

        if True print 'x'
                    ^

Above we saw:

* IndexError
* KeyError
* NameError
* TypeError
* ValueError
* ZeroDivisionError

More are shown in the Python docs 

http://docs.python.org/tutorial/errors.html#errors-and-exceptions

* IndentationError
* I/OError
* OverflowError

Often an error in your code will announce itself in this way, and your job as a "debugger" is to find and fix the error.  It's very helpful that Python logs the line number of the instruction that caused the error

.. sourcecode:: python

    import utils
    data = utils.load_data()

    > python script.py 
    Traceback (most recent call last):
      File "script.py", line 2, in <module>
        data = utils.load_data()
    TypeError: load_data() takes exactly 1 argument (0 given)

Sometimes errors due to faulty input data can be anticipated (or perhaps, encountered the first time you try to run your code).  In a very large list of items, suppose a few are malformed or only contain 6 columns instead of 7, or one entry has tabs rather than spaces.  Perhaps 1 in 10,000 Genbank records lacks a field that you need to read, and so on.

In that case use, ``try`` and ``except``

>>> bad = list()
>>> L = zip('abc',range(3))
>>> L.append('d')
>>> L
[('a', 0), ('b', 1), ('c', 2), 'd']
>>> for i, item in enumerate(L):
...     try:
...         print item[1]
...     except IndexError:
...         bad.append(i)
... 
0
1
2
>>> bad
[3]

If you don't want to do anything with the exceptional cases, just substitute ``pass`` or ``continue`` if there is more dependent code.  In advanced programming, user-defined exceptions are common, as is the possibility to ``raise`` on exception on encountering an error.

The last Python idiom for exceptions is that they carry additional information

>>> try:
...     1/0
... except ZeroDivisionError, e:
...     print e
... 
integer division or modulo by zero
