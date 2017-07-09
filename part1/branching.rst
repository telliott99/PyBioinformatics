.. _branching:

#########
Branching
#########

**if -- else --**

We already introduced the concept of ``if``, but we need to do it more completely now.  ``if`` can be used by itself, but it's often seen in combination with ``elif`` and ``else``

.. sourcecode:: python

    if X:
        doSomething()
    else:
        doSomethingElse()

.. sourcecode:: python

    if X:
        doSomethingOutstanding()
    elif Y:
        doSomethingElsePrettyNice()
    else:
        doOurFallbackThing()

There can be as many ``elif`` expressions as you want.

Another common control element is the ``while`` statement.

>>> x = 2
>>> while x > 0:
...     print x
...     x -= 1
... 
2
1

The statement ``x > 0`` is the `termination condition <http://en.wikipedia.org/wiki/Loop_invariant>`_ for the loop.

Of course, if x is not altered within the loop, or x never reaches 0 because you did ``x += 1`` by mistake, then the loop will never finish.  And if x starts with a value less than or equal to 0 then the loop is just skipped.

.. _while-True:

A variant of the ``while`` loop is to set the truth test to a value that is always true, and then ``break`` out of the loop when desired.

>>> L = list()
>>> s = 'AGCTAGCT'
>>> while True:
...     i = s.find('A', i+1)
...     if i == -1:
...         break
...     L.append(i)
... 
>>> print L
[0, 4]

This construct solves a subtle problem with the logic of code to find all items of a particular type within a list.  We want to use i + 1 for the second argument of ``find``.  We also want to start the first ``find`` with i + 1 equal to 0.  Then i would be -1, but that's the condition we want to use to stop the loop.  This logic separates the test of value of i from the looping instruction itself.

**Equality**

I've already used the ``==`` symbol to test for equality a couple of times.  It's important to emphasize that this is completely different than a single equals sign ``=``.  The single version is only used for assignment (and ``==`` is only used for equality)

.. sourcecode:: python

    a = 7
    if a == 7:
        doSomething()

The first statement assigns the value 7 to the variable ``a``.  Whatever value it had previously (if any) is no longer available using that name.  The second statement tests whether the value a currently has is equal to 7.  Given the two statements in sequence, the if test evaluates to

.. sourcecode:: python

    if True:
        doSomething()

and the function ``doSomething()`` will be executed.

Certain objects evaluate to False.  The obvious one is the integer 0:

>>> 0 == False
True
>>> if not 0:
...     print 'Nope'
... 
Nope

In the above example we evaluate the nature of 0 in two different ways.  It's not such a big deal, but empty objects (like a list with no elements) evaluate to False only by the second test:

>>> a = [ ]
>>> a == False
False
>>> if not a:
...     print 'empty'
... 
empty
>>> not a
True

We don't need the explicit ``not``

>>> for obj in [[ ], ( ), '', { }, None]:
...     if obj:
...          print 'yes'
...     else:
...          print 'nope'
... 
nope
nope
nope
nope
nope

We can shorten the above example by using 'any' or 'all':

>>> L = [[ ], ( ), '', { }, None]
>>> any(L)
False
>>> all(L)
False
>>> not all(L)
True

**Caesar cipher**

Let's use what we've learned to construct a secret message.  According to 

http://en.wikipedia.org/wiki/Caesar_cipher

Julius Caesar used a substitution cipher where 'A' was substituted by 'D', and in general a character 'X' was substituted by ``chr(ord(X)+3)``.  The only difficulty is to wrap the sequences around so that 'Z' becomes 'C', and so on.

.. sourcecode:: python


    def caesar(s,offset=3,decrypt=False):
        rL = list()
        def f(c,n):
            if c == ' ':  return c
            x = ord(c) + n
            if x > ord('Z'):
                x -= 26
            if x < ord('A'):
                x += 26
            return chr(x)
        if decrypt:
            offset *= -1
        for c in list(s):
            rL.append(f(c,offset))
        return ''.join(rL)

    s = 'Gallia est omnis divisa in partes tres'
    plaintext = s.upper()
    print plaintext
    ciphertext = caesar(plaintext)
    print ciphertext
    print caesar(ciphertext, decrypt=True)

.. sourcecode:: python

    > python script.py
    GALLIA EST OMNIS DIVISA IN PARTES TRES
    JDOOLD HVW RPQLV GLYLVD LQ SDUWHV WUHV
    GALLIA EST OMNIS DIVISA IN PARTES TRES

It's fine for a short demonstration, but one problem with this example as it stands is that we didn't test the 'edge-cases'.  We should have an 'xyz' in our message to test the wrapping code.
