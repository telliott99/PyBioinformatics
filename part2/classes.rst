.. _classes:

#######
Classes
#######

Object-oriented programming is about objects, naturally enough.  Objects are derived from---'instantiated from'---classes.  You can think of a class as a factory that turns out objects of a particular type.  The class definition defines the type, but the objects may also have individual character.

OOP is really about classes.

In Python, a class can be defined with no data or functions at all.  For this example I've added a single member variable:

>>> class A:
...     x = 3
... 
>>> a1 = A()
>>> print a1.__class__
__main__.A
>>> print a1.__dict__
{}
>>> print A.__dict__
{'x': 3, '__module__': '__main__', '__doc__': None}
>>> print a1.x
3

Basically, what having a "class" really means is that there is a Python dictionary somewhere that includes information about the class, and tells if there are class methods.  

If we add this code:

>>> a2 = A()
>>> print a2.__dict__
{}
>>> print a2.x
3
>>> a2.x = 5
>>> print a2.x
5
>>> print a2.__dict__
{'x': 5}
>>> print A.__dict__
{'x': 3, '__module__': '__main__', '__doc__': None}
>>> print a1.x
3

You can see that when we did ``a2.x = 5`` we "shadowed" the ``x`` variable from the class A.  So now the dict for a2 has an entry ``x`` and when Python looks for a2's ``x`` it stops and gives us that value.

But the change in the object ``a2``'s data doesn't propagate to ``a1``.  They don't share 'state'.  

Normally, classes are employed to associate methods with data.  Two methods you nearly always see are ``__init__`` and ``__repr__``.  

``__int__`` is called when the object is constructed, to initialize data at that time, and ``__repr__`` determines how the object will look when it's printed.  When you write your own ``__repr__`` method for a class, you should return a string that will be printed when the object is asked to print itself.

All the 'instance methods' have ``self`` as an unseen first argument (that is, there is no corresponding argument when the method is called, instead the object is secretly added as the first argument by Python).  All the methods that mean something special to Python have flanking double underscores.

.. sourcecode:: python

    class Obj:
        def __init__(self, s='x'):
            self.s = s

        def __repr__(self):
            pL = ["Hi, I'm an", 
                  str(self.__class__).split('.')[1],
                  ', my name is', self.s]
            return ' '.join(pL)

    a = Obj('o')
    print a

.. sourcecode:: python

    > python script.py 
    Hi, I'm an Obj , my name is o

Here is a more practical example from analytical geometry.

**Line class**

.. sourcecode:: python

    import math

    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y
        def __repr__(self):
            return 'point (' + self.chars() + ')'
        def chars(self):
            return str(self.x) + ',' + str(self.y)

    P = Point(0,0)
    Q = Point(3,4)
    print 'P', P
    print 'Q', Q
    
A point class seems reasonable in order to print the data for a point.  (On the other hand, a simple tuple is a lot less fuss).

Now we add another class to the same script file:

.. sourcecode:: python


    class Line:
        def __init__(self, p1, p2):
            self.p1 = p1
            self.p2 = p2

        def __repr__(self):
            p1 = `self.p1`
            p2 = `self.p2`
            return ''.join(['line [', p1, ', ', p2, ']'])

        def length(self):
            dx = self.p1.x - self.p2.x
            dy = self.p1.y - self.p2.y
            h = dx**2 + dy**2
            if h == 0:
                 return 0
            return round(math.sqrt(h), 2)

    L = Line(P,Q)
    print L, 'length ', L.length()

.. sourcecode:: python


    > python script.py 
    line [point (0,0), point (3,4)] length  5.0

Here is another example using FASTA DNA data:

.. sourcecode:: python

    class DNA:
        N = 40
        def __init__(self, data):
            title, seq = data.strip().split('\n',1)
            self.t = title
            self.s = ''.join(seq.split())

        def __repr__(self):
            N = DNA.N
            pL = [self.t]
            if len(self.s) > N:
                pL.append(self.s[:N] + '..')
            else:
                pL.append(self.s)
            return '\n'.join(pL)

    dna = DNA('>my_seq\n' + 'ACGT' * 15)
    print dna

.. sourcecode:: python

    > python script.py 
    >my_seq
    ACGTACGTACGTACGTACGTACGTACGTACGTACGTACGT..

True afficionados will tell you that what is really cool about OOP is (i) overloading and (ii) inheritance.  Overloading means to modify the meaning of familiar methods, operators like + and -, even ( ), [ ], and the like.  

.. sourcecode:: python

    class A:
        def __init__(self, s):
            self.s = s
        def __repr__(self):
            return self.s
        def __add__(self, other):
            return A(self.s + other.s)

    p = A('p')
    q = A('q')
    print p
    print q
    print p + q

.. sourcecode:: python

    > python script.py 
    p
    q
    pq

Now, this doesn't make a lot of sense if the only data is a string, but it's useful in other contexts.

You certainly do see classes in bioinformatics programming, but I mainly rely on what's called procedural programming

http://en.wikipedia.org/wiki/Procedural_programming

Two use cases for classes come to mind.  First, suppose we have sequences coming into our program that may have invalid or unusual characters.  We might define a class for DNA sequences that accounts for this diversity.

Another is inheritance.  What this means is that a 'derived' class 'inherits' from a parental class some or all of its function definitions (or data).  This makes sense if the simple parental class implements functions common to all its descendants, while the descendants have their own specialized code.

An example from PyCogent:

.. sourcecode:: python

    class NucleicAcidSequence(Sequence):

The ``Sequence`` class has some code or data that is useful for all sequences.  The ``NucleicAcidSequence`` class includes those functions and data by inheritance, but will add other stuff on top of it.

