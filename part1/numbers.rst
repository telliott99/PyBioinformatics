.. _numbers:

#######
Numbers
#######

Python has several different data types for numbers.  We've already used integers (the ``int`` type) for the index of an item in a list, or to keep track of the iteration of a loop.  These include both the negative and positive integers.

One nice thing in Python is the ``long`` type, which are integers with unlimited precision.

>>> from math import factorial
>>> n = factorial(10000)
>>> len(str(n))
35660
>>> type(n)
<type 'long'>

The basic numeric types are described in the docs

http://docs.python.org/library/stdtypes.html#numeric-types-int-float-long-complex

The ``float`` type stands for a 'floating point number', familiar to every scientist as scientific notation.  By default, a floating point number will be printed with a large number of trailing places:

>>> 1.0/3
0.33333333333333331

and a rounding error at the end.  Beware of this:

>>> L = [0.1 for i in range(10)]
>>> sum(L)
0.99999999999999989

The above is in Python 2.6.  In Python 2.7 we get something aesthetically more pleasing:

>>> 0.1
0.1

But as noted in the docs:

     It’s important to realize that this is, in a real sense, an illusion: the value in the machine is not exactly 1/10, you’re simply rounding the display of the true machine value.

http://docs.python.org/tutorial/floatingpoint.html

If you want to do math with floating point numbers and you expect a certain result, what you need to do is test whether the result is 'close enough' to the expected value.

**Division**

Division in Python (before version 3.x) has been integer division.  For example:

>>> t = (2,3,4)
>>> for i in t:
...     print i/3,
... 
0 1 1
>>> for i in t:
...     print i%3,
... 
2 0 1

In the first part, we do integer division.  The result of 2/3 is 0, while 4/3 is equal to 1.  In the second part we get the remainder or modulus with the ``%`` operator.

If you want to do standard division, either the numerator or the denominator must be a float.


>>> i = 2
>>> type(i)
<type 'int'>
>>> f = float(i)
>>> type(f)
<type 'float'>
>>> f/3
0.66666666666666663

If you can't guarantee that one or the other will be a float, then just multiply by ``1.0`` (or do ``float(i)``).

>>> i = 6
>>> j = 10
>>> k = 1.0*i/j
>>> k
0.59999999999999998
>>> '%3.2f' % k
'0.60'

Another way to have only standard division is to do:

>>> from __future__ import division
>>> 1/3
0.33333333333333331

**Printing numbers**

Frequently one wants to print a number as part of a string.  Printing of floating point values can be cleaned up by using formatting codes.  This is a complex subject.  If you're interested, see the docs

http://docs.python.org/library/stdtypes.html#string-formatting-operations

One standard usage is:

>>> import math
>>> print '%3.8f' % math.pi
3.14159265
>>> print '%3.2f' % math.pi
3.14

The ``%`` here is not the modulus from above but a formatting operator.  The ``3.2`` consists of the ``3`` part, which specifies a minimum field width of 3, and the ``.2`` part, which directs that there should be two significant digits after the decimal point.

The field width doesn't come into play very often.  In the above example it might as well be ``1``, or even left out altogether:

>>> import math
>>> print '%.2f' % math.pi
3.14
>>> print '%6.2f' % math.pi
  3.14

I sometimes use the combination of ``str`` and ``round`` to accomplish the same thing

>>> f = 2.0/3
>>> f
0.66666666666666663
>>> round(f,2)
0.67000000000000004
>>> str(round(f,2))
'0.67'

**Bits**

I don't ever use it, but it's interesting to know that Python will 'bit-shift' ints:

>>> i = 5
>>> bin(i)
'0b101'
>>> i << 2
20
>>> bin(20)
'0b10100'
>>> i >> 2
1

We have the standard mathematical operators:  '+ - * /'

I explained the modulus operator before, it just gives the remainder.

>>> 5 % 2
1
>>> 5/2
2

It can be handy for printing values from a loop only rarely:

>>> for i in range(10000):
...     if i and not i % 1000:
...         print i
... 
1000
2000
3000
4000
5000
6000
7000
8000
9000

The mathematical operator we haven't seen yet is the exponentiation operator:

>>> 3**2
9
>>> 3**3
27
>>> pow(3,2)
9
>>> pow(3,3)
27

``pow`` actually can take a modulus as the third argument

http://docs.python.org/library/math.html#math.pow

The ``log`` function is the natural logarithm, so I've often written an explicit ``log2`` function

>>> from math import log, e
>>> log(e)
1.0
>>> log(4)/log(2)
2.0

Of course, that is true for any base.  Let's try base 2:

>>> def log2(n):
...     return log(n)/log(2.0)
... 
>>> log2(4)
2.0

I notice in looking at the docs above there is a ``log10`` function and also an extra possible argument of a base to ``log``.  I didn't know that!

>>> log(4,2)
2.0
>>> math.log10(2)
0.3010299956639812

All these years writing my own log2 function.  Oh well.  That brings up a small point:  it's difficult to unlearn old habits.  Sometimes my code might not be the latest and greatest, I'm just happy if it works.  YMMV.

