.. _recursion:

#########
Recursion
#########

In recursion, a procedure is repeated until repetition is not necessary any more.  One type of problem involves improving an approximate answer until we reach a threshold that depends on the particular case.

Recursion is often associated with the idea of a function that calls itself after appropriately modifying its argument, but the function call isn't actually necessary.

Here's a simple example from Sedgewick

http://www.amazon.com/gp/product/0201350882

for computing the greatest common divisor of two numbers.  It is attributed to Euclid

>>> def gcd(m,n):
...     print 'gcd',m,n
...     if n == 0:
...         return m
...     return gcd(n, m % n)
... 
>>> gcd(314159,271828)
gcd 314159 271828
gcd 271828 42331
gcd 42331 17842
gcd 17842 6647
gcd 6647 4548
gcd 4548 2099
gcd 2099 350
gcd 350 349
gcd 349 1
gcd 1 0
1

These values for m and n are those in Sedgwick.  (They may seem kind of familiar).  m and n are *relatively prime*.  Try another:

>>> gcd(136,85)
gcd 136 85
gcd 85 51
gcd 51 34
gcd 34 17
gcd 17 0
17

As you can see, there are five successive calls to ``gcd`` before we return the value ``17``, which is the greatest common divisor of 136 (17 times 8) and 85 (17 times 5).

In the next example from SICP

http://mitpress.mit.edu/sicp/

Newton's method of successive approximation 

http://en.wikipedia.org/wiki/Newton's_method

is applied to calculate a square root.  We define a couple of accessory functions first.  They could be included in the loop without even being functions, but this approach makes the logic cleaner.  

In these, we're careful to always do float division.  I'm used to doing this manually by using ``*1.0`` or whatever is appropriate:

>>> def improve(x,guess):
...     def average(a,b):
...         return (a+b)/2.0
...     return average(guess,x*1.0/guess)
... 
>>> def error(x,guess):
...     return abs(x - guess*guess)
... 

The idea, as indicated by the name of the argument to ``error`` above, is to guess the square root of x.  The guess can then be improved if needed by averaging it together with the value x/guess.  I nested the definition of ``average`` under ``improve`` because that's the only place it's needed.

We add this code

>>> n = 5
>>> guess = 1.1
>>> err = 1e-6
>>> 
>>> while True:
...     print guess
...     if error(n,guess) < err:  break
...     guess = improve(n,guess)
...     
... 
1.1
2.82272727273
2.29703191334
2.23687697833
2.23606812379
>>> guess*guess
5.00000065425

We make an initial guess, then enter the loop.  Each time around, we test if the guess is good enough, and if so, ``break``.  Otherwise we call ``improve`` to get a better guess.

A few comments on the code above.  First, we resist the urge to call the error variable ``e`` (even though ``math.e`` isn't in scope).  This is just good practice, also we have another use for e in the special form ``1e-6``, which is shorthand for 0.000001.  This form gives a ``float``.  

Sometimes for large numbers (like the upper bound on a loop) we need an ``int``, which is obtained with ``int(1e6)``.  

We test the error before adjusting the guess, simply because we assigned our first guess before entering the loop.  I believe it's known that some guesses behave badly with this procedure but I'm not going to worry about that.

As an alternative could also wrap the code in a function but it doesn't really change the logic.

.. sourcecode:: python

    err = 1e-6

    def improve(x,guess):
        def average(a,b):
            return (a+b)/2.0
        return average(guess,x*1.0/guess)

    def error(x,guess):
        return abs(x - guess*guess)

    def newton(n, guess=None):
        if not guess:
            guess = 1.1
        if error(n,guess) < err:
            return guess
        guess = improve(n,guess)
        return newton(n,guess)

    print newton(5)        

We get::

    > python script.py
    2.23606812379


Eventually the function nested calls must reach some 'base case' where the function can actually return a value.  This is similar to the principle of an inductive proof.  

http://en.wikipedia.org/wiki/Mathematical_induction

Recursion isn't necessarily used a lot in Python, but when you need it, it's very useful.  And it is famous in computer science.

The factorial is another classic example

.. sourcecode:: python

    def factorial(n):
        if n < 0:
            return None
        if n == 0:
            return 1
        return n * factorial(n-1)
    
    print factorial(5)
    
Since we're all friends here, we do not check for pathological cases.  Or, shall we just call them non-integer cases.  That's better.

Output

.. sourcecode:: python

    > python script.py
    120

These recursive calls have a limit.  We can find it by adding this code to what is shown above with the definition of ``factorial``

.. sourcecode:: python

    i = 0
    while True:
        i += 1
        print i
        factorial(i)

Output::

    > python script.py
    1
    2
    ..
    998
    999
    Traceback (most recent call last):
      File "script.py", line 14, in <module>
        factorial(i)
      File "script.py", line 6, in factorial
        return n * factorial(n-1)
    ..
    RuntimeError: maximum recursion depth exceeded

This is horribly inefficient, in more ways than one.  We call ``factorial(998)`` which calls ``factorial(997)`` all the way to ``factorial(0)``, which then returns ``1`` to ``factorial(1)``, which returns ``1`` to ``factorial(2)``, which returns ``2`` and on and on.  The result builds up until we eventually get the answer for ``factorial(998)`` (not shown).  Then we start with ``factorial(999)`` which calls ``factorial(998)`` etc.

Nevertheless, Python is fast enough to do all this in a reasonable time.

It seems that if there are more than 999 recursive calls stacked up, something breaks.  

A more efficient way to deal with this, which gets around the limit for recursive calls, is to build our way out to the value we need, saving the intermediate results in a cache.  Something like this

.. sourcecode:: python

    def factorial(n):
        L = [1,1,2]
        i = 3
        while i < n + 1:
            L.append(i*L[-1])
            i += 1
        return L[n]
    
    print factorial(5)
    n = factorial(10000)
    print len(str(n))

Output::

    > python script.py 
    120
    35660

What's going on here?  The list L caches the values for the factorial.  L[2] = 2;  L[3] = 6;  L[4] = 24 and so on.  When ``factorial`` is called with an argument like 999, if the list is not long enough yet, we append values to it one by one until it is long enough.  Eventually we get to n and return the correct value.  In this case 'memoizing' beats recursion.

Caching values is a very important technique.

One trick here is that ``factorial(10000)`` is a large number (print it and see).  Rather than do that, I converted the decimal value to a string with ``str`` and then printed the ``len``, the length, of that string.  That's a lot of places.

And a last point about this specific function is that ``factorial`` has been included in the ``math`` module since Python 2.6

http://docs.python.org/library/math.html#math.factorial

>>> from math import factorial
>>> print len(str(factorial(1000)))
2568
>>> print len(str(factorial(10000)))
35660

**Towers of Hanoi**

http://en.wikipedia.org/wiki/Tower_of_Hanoi

After the examples we've mentioned already 
we've probably seen enough recursion.  However, let's look at the Towers as the last problem for this section, because it's such a great example, that is in Jones and Pevzner:

http://www.amazon.com/gp/product/0262101068

and it can be solved *with no code*.

It's a game of 3 pegs and a stack of disks.  Here is a picture of the starting position for a very simple N = 4 game.

.. image:: /figures/hanoi1.png
   :scale: 50 %

The goal is to move the complete stack of disks to the right hand peg.  The rules are:

* only one disk moves at a time
* no disk may ever be placed on top of a smaller disk

It's an excellent example of recursion because the solution can be specified so simply using that approach.  Given N disks, first move the top N-1 disks to the middle peg, then move the last disk to the right peg, and finally, put all the N-1 disks on top of the that one.  

We know this strategy will work, even if we don't at first know how to move N-1 disks.  In that case, reformulate the sub-problem in terms of N-2.  Eventually we'll get to a problem of 1 disk, which is trivial to solve.

What are the three moves that brought the game to this position?

.. image:: /figures/hanoi2.png
   :scale: 50 %

Now, using the colors of the disks in the above diagrams for reference, consider this special ruler.  

.. image:: /figures/hanoi3.png
   :scale: 100 %

This ruler gives the sequence of disks to be moved to solve the N = 4 game.  

There is one last thing:  if N is even, start by moving the first disk to the middle peg, otherwise start by moving it to the right peg.

If we have a bigger game and need to make a larger ruler, do it for N += 1 by constructing a tandem duplication of the ruler we have, and inserting one new vertical bar in the middle.

There is the last issue that we usually two possible destination pegs and we need to choose the right one.  I'll leave that for you.  Perhaps you can convert the ruler idea to Python code that will print the precise moves in order.

The actual sequence of moves is:

* cyan middle
* red right
* cyan right
* blue middle
* cyan left
* red middle
* cyan middle
* green right
* cyan right
* red left
* cyan left
* blue right
* cyan middle
* red right
* cyan right

We need to find a rule that gives the sequence of middle, right, left and so on.  I think I see a pattern developing here.  The sequence for the first (cyan) disk is 'middle','right','left', which then repeats.  The sequence for the second (red) disk is 'right','middle','left', which then starts to repeat.  The sequence for the third (blue) disk is 'middle','right', and I'm betting the next one will be left.

Maybe we do need some code after all.  We need to simulate the game to give the correct moves, so that we can test whether our ruler and simple rule give the correct moves without any code!

If you have Tkinter 

http://wiki.python.org/moin/TkInter

and the Python source you can check this out::

    . . /Python-2.6.6/Demo/tkinter/guido/hanoi.py


