.. _histogram:

##########
Histograms
##########

We have a collection of values drawn from a continuous distribution.  We'd like to visualize the collection, but first we have to bin them.

We can do it by hand, knowing the desired number of bins (N).  Suppose the limits are 0 and 1 (inclusive), and N = 8.

>>> import random, bisect
>>> import numpy as np
>>> 
>>> N = 8
>>> bL = np.linspace(0,1,N+1)
>>> print bL
[ 0.     0.125  0.25   0.375  0.5    0.625  0.75   0.875  1.   ]

There are 9 values in bL including the limits, which makes a total of 8 bins.

We could examine each value and increment the count of the appropriate bin, but there is another way.  The ``bisect`` module has functions that can help, as long as we first sort our list of values

>>> f = random.normalvariate
>>> L = [f(mu=0.5,sigma=0.1) for i in range(1000)]
>>> L.sort()
>>> 
>>> def show():
...     prev = 0
...     for b in bL[1:]:
...         i = bisect.bisect_left(L,b)
...         print b, i - prev
...         prev = i
... 
>>> show()
0.125 0
0.25 6
0.375 81
0.5 399
0.625 409
0.75 98
0.875 6
1.0 1

The problem, as I hope you can see, is that the bins are not spaced properly with respect to the mean (mu = 0.5) of the distribution.  We need an odd number of bins, which would put 0.5 in the center of the middle bin.

>>> N = 9
>>> bL = np.linspace(0,1,N+1)
>>> show()
0.111111111111 0
0.222222222222 2
0.333333333333 30
0.444444444444 249
0.555555555556 420
0.666666666667 256
0.777777777778 38
0.888888888889 5
1.0 0

You may say there is no reason to do this by hand!  And you'd be right.  

**numpy**

>>> h = np.histogram(L,bins=9,range=(0,1))
>>> h[0]
array([  0,   2,  30, 249, 420, 256,  38,   5,   0])

**matplotlib**

.. sourcecode:: python

    import pylab
    import matplotlib.pyplot as plt
    import random
    import numpy as np

    N = 8
    bL = np.linspace(0,1,N+1)
    f = random.normalvariate
    L = [f(mu=0.5,sigma=0.1) for i in range(1000)]

    n,bins,patches = pylab.hist(L,N,normed=1,
                                histtype='stepfilled')
                            
    ax = plt.axes()
    ax.set_xlim(0,1)
    plt.savefig('hist.png')

.. image:: /figures/hist.png
    :scale: 50 %


