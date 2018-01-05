.. _numpy:

#####
Numpy
#####

In the next section we're going to install ``matplotlib``, but first we also have to install ``numpy`` (on Linux---see :ref:`matplotlib`).  It's already there on OS X.

Here's a simple example with ``numpy`` (from the help for ``numpy.mean``):

>>> import numpy as np
>>> R = range(4)
>>> R
[0, 1, 2, 3]
>>> A = np.array(R)
>>> A.shape=(2,2)
>>> A
array([[0, 1],
       [2, 3]])
>>> np.mean(A)
1.5
>>> np.mean(A,axis=0)
array([ 1.,  2.])
>>> np.mean(A,axis=1)

With no ``axis`` argument, ``mean`` computes the mean of the entire 'flattened' array.  With ``axis=0``, we get the means of the columns, while for ``axis=1`` we get the row means.

``numpy`` is for serious math.  Here is a non-serious example.  We generate a 2 x 2 matrix::

    0  1
    1  1

It turns out that if we multiply this matrix by itself we generate an old friend:

.. sourcecode:: python

    import numpy as np

    L = [0, 1, 1, 1]
    T = np.array(L)
    T.shape = (2,2)
    M = T
    print T, '\n'

    for i in range(4):
        M = np.dot(M,T)
        print M, '\n'

.. sourcecode:: python

    > python script.py
    [[0 1]
     [1 1]] 

    [[1 1]
     [1 2]] 

    [[1 2]
     [2 3]] 

    [[2 3]
     [3 5]] 

    [[3 5]
     [5 8]] 

.. sourcecode:: python
 
     for i in range(10):
         M = np.dot(M,T)
         print M[1,1],
     print

.. sourcecode:: python

    2 3 5 8 13 21 34 55 89 144

**Indexing**

>>> import numpy as np
>>> L = [[[1,2],[3,4]],[[5,6],[7,8]]]
>>> A = np.array(L)
>>> A.shape
(2, 2, 2)
>>> A[0,1,0]
3
>>> A[1,1,1]
8

Let's take a 2D example as easier to visualize:

>>> A = np.array(L[0])
>>> A
array([[1, 2],
       [3, 4]])
>>> A[0]
array([1, 2])
>>> A[0,0]
1
>>> A[:,0]
array([1, 3])
>>> A[:,0].shape
(2,)

Alternatively::

    >>> A = np.array(range(27))
    >>> A.shape = (3,3,3)
    >>> A
    array([[[ 0,  1,  2],
            [ 3,  4,  5],
            [ 6,  7,  8]],

           [[ 9, 10, 11],
            [12, 13, 14],
            [15, 16, 17]],

           [[18, 19, 20],
            [21, 22, 23],
            [24, 25, 26]]])
    >>> A[:,1,]
    array([[ 3,  4,  5],
           [12, 13, 14],
           [21, 22, 23]])

The slice access makes it easy to get columns (or whatever slice you're looking for) from the data.

**PCA**

With ``numpy`` we have the tools to do principal components analysis (PCA).  This example has more code than anything we've seen so far, but if we break it down it should be clear.  

In the first part we do our imports and set the ``seed`` for random.  Then we generate a bunch of numbers.  The variance in the x-direction is ``100.0/15`` times that in the y-direction.  We plot these values as red circles.

.. sourcecode:: python

    import matplotlib.pyplot as plt
    import numpy as np
    import sys
    from math import sqrt
    import random
    random.seed(1357)

    R = range(-100,100)
    X = [random.choice(R) for i in range(30)]
    r = range(-15,15)
    Y = [random.choice(r) for i in range(30)]
    
    plt.scatter(X,Y,s=150,
        color='r',marker='o')
    ax = plt.axes()
    ax.set_ylim(-100,100)

.. image:: /figures/pca0.png
    :scale: 50 %

In the second part, which continues the script above, we rotate the values by 45 degrees, and plot them in purple.  If you look closely you can see that the pattern is the same.  We use the ``numpy`` function ``vstack`` to generate a 2 row x 30 column matrix.

.. sourcecode:: python

    A = np.vstack([X,Y])
    z = 1.0/sqrt(2)
    t = [[z,-z],[z,z]]
    T = np.array(t)
    X2,Y2 = np.dot(T,A)

    plt.scatter(X2,Y2,s=150,
        color='purple',marker='o')
    plt.grid(True)

In the third part comes the magic.  We generate a covariance matrix for the values from part two.  The print statement shows this matrix is nothing more than::

    > python script.py
    [[ 1826.9908046   1785.0045977 ]
     [ 1785.0045977   1883.89425287]]

We use numpy's linear algebra routines to generate the eigenvalues and eigenvectors for this covariance matrix.  When we do matrix multiplication using the eigenvectors and the data from part two, we transform the data so its greatest variance lies along the x-axis.  Since that's the way we set it up, the points plot on top of the original ones.

.. sourcecode:: python

    A2 = np.vstack([X2,Y2])
    cm = np.cov(A2)
    evals,evecs = np.linalg.eig(cm)
    evals.sort()
    X2,Y2 = np.dot(-evecs,A2)

    for e in [cm,evals,evecs]:
        print e

    plt.scatter(X2,Y2,s=75,
        color='k',marker='+')

    plt.savefig('pca.png')

Well actually, they don't.  If you notice, we multiplied by ``-evecs``.  The only guarantee of PCA is that the variance is maximized.  In this case we generated a 180 degree rotation of the original points, but our sly ``-`` sign fixed that.  Here are the eigenvalues and eigenvectors::

    [   70.21119515  3640.67386232]
    [[-0.71271919 -0.70144947]
     [ 0.70144947 -0.71271919]]


.. image:: /figures/pca.png
    :scale: 50 %

Numpy usually operates on arrays (like R's vectors).  It turns out that if we want to define our own functions (designed to take a single value at a time), they need to be 'vectorized' to work with Numpy arrays.

.. sourcecode:: python

    import numpy as np

    A = np.arange(10)

    def f(n):
        if n > 3:
            return n
        return 0
    print f(A)

.. sourcecode:: python

    > python script.py 
    Traceback (most recent call last):
      File "script.py", line 8, in <module>
        print f(A)
      File "script.py", line 5, in f
        if n > 0.3:
    ValueError:. . .

Try again:

.. sourcecode:: python

    import numpy as np

    A = np.arange(10)

    @np.vectorize
    def f(n):
        if n > 3:
            return n
        return 0
    print f(A)

.. sourcecode:: python

    > python script.py 
    [0 0 0 0 4 5 6 7 8 9]

Although this looks good, it is still not correct

http://telliott99.blogspot.com/2010/03/vectorize-in-numpy.html

The problem is a bit obscure.  When we did ``return 0`` above, we fixed the return type for all values returned from the function.  With the ``0``, we got locked into integers as the return type.  

Having done that, if we run this code with all the values floats (divided by 10.0), it does not run without a modification:

.. sourcecode:: python

    import numpy as np

    A = np.arange(0,1,0.1)

    @np.vectorize
    def f(n):
        if n > 0.3:
            return n
        return 0.0
    print f(A)

.. sourcecode:: python

    > python script.py 
    [ 0.   0.   0.   0.3  0.4  0.5  0.6  0.7  0.8  0.9]

Notice the line ``return 0.0``.  The return type is determined by the first value returned.  Thus if we do ``return 0`` at this point, all of the rest of the values are returned as ints.  And that means we'll see zeroes all the way through the output, rather than 0.3, 0.4 and so on as is correct.