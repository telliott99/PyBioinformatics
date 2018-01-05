.. _import:

######
Import
######

Python has a large number of functions and classes which aren't loaded when it runs initially, but can be accessed using the ``import`` statement.  I'll have more to say about this 'standard library' later, but here is a good place to do a very short introduction.  Let's import the ``string`` module:

>>> import string
>>> string.uppercase
'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

Alternatively:

>>> from string import uppercase
>>> uppercase
'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

The docs are here:

http://docs.python.org/library/

If you want to know what's available in the module x, you can also just do ``dir(x)`` (after first importing ``x``).

The ``random`` module has what you might expect.  For example:

>>> import random, string
>>> uc = string.uppercase
>>> for i in range(5):
...     print random.choice(uc),
... 
Y M P B L

We can use these functions to construct random passwords:

>>> N = 25
>>> L = [random.choice(uc) for i in range(N)]
>>> print ''.join(L)
PWWTWTABYKYVXJUFHQGPKJZYX

Such passwords wouldn't be accepted by most systems these days.  But we can also do this:

>>> string.digits
'0123456789'
>>> string.printable[:36]
'0123456789abcdefghijklmnopqrstuvwxyz'

(There's more to ``printable``, I just truncated it).

A disadvantage of the extended symbols is that the password is much harder to type.  Also, we might want to break it up into chunks to make it easier to read.  You would skip the spaces in the output when entering the password.

>>> def chunks(L,d=5):
...     rL = list()
...     for i in range(0,len(L),d):
...          rL.append(L[i:i+d])
...     return rL
... 

We did something just like that in :ref:`loops`.

>>> N = 25
>>> L = list()
>>> for i in range(N):
...     L.append(random.choice(uc))
>>> for item in chunks(L):
...     print ''.join(item),
... 
ZHZAR CZYSI XAGYT TWEMY GCBLP

That's an excellent password.  Especially in a world where the dark hats assume everyone has used digits and special symbols.  I can enter it accurately with ease.