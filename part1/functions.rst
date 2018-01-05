.. _functions:


#########
Functions
#########

At the most basic level, programs work with data organized into data structures, and define functions that operate on those data structures.  Here is a simple example using the integer or ``int`` data type:

>>> def plus(x,y):
...     return x + y
... 
>>> plus(1,1)
2

``def`` is a keyword that says, get ready Python, we're about to define our function, and it's immediately followed by the name of the function, the arguments and a semicolon.

Here is the last example again, but executed as a script from the file ``script.py`` (notice that we need an explicit ``print`` call since we're no longer in the interpreter)::

    def plus(x,y):
        return x + y
    
    result = plus(1,1)
    print result

Here is the result of running that script from the shell::

    > python script.py
    2

Our first function has the name or label ``plus``.  A function usually has 'arguments' enclosed in parentheses and separated by commas, although it is legal for a function to have no arguments, in which case the parentheses are still needed, but they're empty.  

In the definition, we specify the arguments by the names we'll use 'inside' the function.  These may be different than the names those arguments have outside the function, but they don't have to be.

>>> def f(x,y):
...     print x + y
... 
>>> a = 1
>>> b = 2
>>> f(a,b)
3
>>> x = 1
>>> y = 2
>>> f(x,y)
3

A function may 'return' a value but this is also optional.

>>> def f():
...     return 1
... 
>>> def g():
...     pass
... 
>>> print f()
1
>>> print g()
None

In the original example, ``plus`` adds x and y and returns the result.

The semicolon is a symbol that means we're descending a level in our code, so the part which follows is somehow nested underneath the line above.

**Whitespace**

The whitespace rule demands that all the code within a function is indented at least four spaces (see below).  Although a tab is possible here, I strongly recommend that you use four spaces as your standard.  

The indentation is awkward for the interpreter to handle when pasting in code.  That's one reason why it doesn't work so well for more complex examples.

Having defined the function, we can call it with the arguments (1,1) and get the expected result.

We've already used functions in the previous section on strings and lists, except there we called them 'methods'.  What's up with that?  Eventually, we will learn how to define 'objects', but simply put, an 'object' is an object (duh) with data *and* its own functions.  A function that we define is called like so::

    f(args)

A function that belongs to an object, that is a method of that object, is called like this::

    obj.f(args)

That's the important difference for now.

Notice that with our function ``plus`` Python does not care what the types of the arguments and x and y really are.  Given the definition, this also works::

    def plus(x,y):
        return x + y
    
    result = plus('a','b')
    print result

Output::

    > python script.py
    ab

This is surprising, perhaps even shocking, to someone coming from another language like C or Java.  Arguments are not 'typed'.  As long as we don't ask the function to do anything illegal, there is no problem.

If we replace the relevant line by::

    result = plus('a',1)

Output::

    > python script.py
    Traceback (most recent call last):
      File "script.py", line 4, in <module>
        result = plus('a',1)
      File "script.py", line 2, in plus
        return x + y
    TypeError: cannot concatenate 'str' and 'int' objects

Python lets us know there's a problem with adding a string and an int.

We frequently have nesting within nesting.  If you use four spaces for indentation, then the second level must be indented by eight spaces::

    def plus(x,y):
        if not type(x) == type(y):
            return 'error'
        return x + y
    
    print plus(1,1)
    print plus('1',1)

Output::

    > python script.py
    2
    error

You shouldn't actually write code like this, but I think you can see what's going on.  We use ``if`` to test whether something is ``True``.  ``a == b`` is true if the left-hand side (a) is equal to the right-hand side (b), and ``not a == b`` is the negation of that.  If the final evaluation is ``True`` we return the string 'error'.  A boolean value (``True`` or ``False``) or an expression that can be evaluated to true or false, is used for conditional execution in programs.

However, idiomatic Python code does not ask a variable what type it is.  It just tells it to do whatever you intend to do and then handles any resulting error in the most appropriate way.  In this case probably the best approach is probably to just let the program blow up, but if your program is complicated and has been running for a long time, you will want to handle the error somehow.  We'll talk about that later.

To reiterate, in this comparison between C-style code::

    if (x)
    {
        if (y)
        {
            doOneThing();
            doSomethingElse();
        }
        else
        { 
            doSomethingReallyCool()
        }
    }

and Python code::

    if x:
        if y:
            doOneThing()
            doSomethingElse()
        else:
            doSomethingReallyCool()

In the C example, the whitespace is optional but the brackets are not.  You could even write it all on one line if you want.  In Python the brackets and the semicolon are no longer present, but the whitespace is required.

Here are some more examples of simple functions::

    s = 'Hello, world!'
    def f(s):
        print s
    f(s)

Output::

    > python script.py
    Hello, world

Here is a function with a 'default' argument::

    def f(s='Joan'):
       print 'Hello ' + s

    f()
    f('Sean')

Output::

    > python script.py
    Hello Joan
    Hello Sean

**Scope**

The names we use for variables inside a function only apply there.  For non-mutable objects, they don't refer to a variable that might also exist in the outside world.

I often re-use the same variable names inside a function (rather than make up another name for the same type of thing).  This will be confusing if you don't understand that there is no conflict (with the exception I'll note in a minute).

>>> def f(x):
...     x += 1
...     return x
... 
>>> x = 3
>>> f(x)
4
>>> x
3

However, you have to be careful with mutable data types like a list or dictionary!

>>> def f(L):
...     L.append('x')
... 
>>> L = range(3)
>>> L
[0, 1, 2]
>>> f(L)
>>> L
[0, 1, 2, 'x']

This change did propagate to the outside scope.  And that would happen regardless of whether we used the same name or not:

>>> def f(A):
...     A.append('x')
... 
>>> L = range(3)
>>> L
[0, 1, 2]
>>> f(L)
>>> L
[0, 1, 2, 'x']

To prevent this from happening, make a copy of the list first:

>>> def f(iL):
...     L = iL[:]
...     L.append('x')
...     print L
... 
>>> L = range(3)
>>> L
[0, 1, 2]
>>> f(L)
[0, 1, 2, 'x']
>>> L
[0, 1, 2]

There is more to say about arguments to functions but that's for later.