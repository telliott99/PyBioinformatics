.. _sampler:

#############
Gibbs Sampler
#############

In this section, we develop what is possibly the world's simplest Gibbs Sampler.

Here is a quote from a source cited in the post:

http://telliott99.blogspot.com/2009/06/motif-discovery.html

    The Gibbs sampler (introduced in the context of image processing by Geman and Geman 1984), is a special case of Metropolis-Hastings sampling wherein the random value is always accepted (that is, alpha = 1). The task remains to specify how to construct a Markov Chain whose values converge to the target distribution. The key to the Gibbs sampler is that one only considers univariate conditional distributions---the distribution when all of the random variables but one are assigned fixed values. Such conditional distributions are far easier to simulate than complex joint distributions...To introduce the Gibbs sampler, consider a bivariate random variable (x, y)...The sampler starts with some initial value y0 for y and obtains x0 by generating a random variable from the conditional distribution p(x | y = y0 ). The sampler then uses x0 to generate a new value of y1 , drawing from the conditional distribution based on the value x0 , p(y | x = x).            

Rather than use technical language to explain the Gibbs sampler, we can visualize how it works with a biological example.  Suppose we have 10 sequences each having a motif embedded at a random position, like this:

.. image:: /figures/gibbs1.png
   :scale: 50 %

What we'd like to do is to slide the sequences back and forth until we end up the motifs aligned with each other:

.. image:: /figures/gibbs2.png
   :scale: 50 %

Start by picking a distribution at random.  Choose a list of 10 integers abd align all of the sequences so the nucleotide at index ``i`` from the list is in the same column.

If we choose at random, it's unlikely that the alignment has much information in it.  The sampler procedure is to fix all of the sequences except one, and then slide that one back and forth to find a better alignment.  The choose another one, and repeat.

If we always choose the best score to assign the index for the new alignment, that's a 'greedy' algorithm, which has the problem of getting trapped on local maxima, so we need to be careful.

Let's work on a simpler problem before doing the sequence alignment..

Construct a 2D distribution, saving the values as a ``csv``-formatted text file::

    1,1,2,2,1,1,1,1,1,1
    1,3,7,5,2,1,1,1,1,1
    1,7,9,6,2,1,1,1,1,1
    1,3,4,3,2,1,1,1,1,1
    1,1,1,1,3,1,1,1,1,1
    1,1,1,1,1,3,1,2,2,1
    1,1,1,1,1,1,2,3,2,1
    1,1,1,1,1,2,3,4,2,1
    1,1,1,1,1,2,2,5,3,1
    1,1,1,1,1,1,4,6,2,1

There's a great R function for plotting this kind of data, so let's not reinvent the wheel but use it.  R code::

    setwd('Desktop')
    library(scatterplot3d)
    fn = 'distr1.txt'
    df = read.csv(fn,head=F)
    m = as.matrix(df)

    z = as.numeric(m)
    x = rep(1:10,each=10)
    y = rep(1:10,10)

    scatterplot3d(x,y,z,
      type='h',pch=16,
      cex.symbol=3,
      cex.axis=2,
      highlight.3d = T,
      xlab='x',ylab='y',
      zlab='z')

And the graphic:

.. image:: /figures/distr1.png
   :scale: 50 %

Actually, the example shows the the advantages of a heatmap for data like this.  I've added a bit more detail to a second version of the distribution::

    1,1,2,2,1,1,1,1,1,1
    1,3,7,5,2,1,1,1,9,1
    1,7,9,6,2,1,1,1,1,1
    1,3,4,3,2,1,1,1,1,1
    1,1,1,1,3,1,1,1,1,1
    1,1,1,1,1,3,1,2,2,1
    0,0,0,0,1,1,2,3,2,1
    1,0,0,0,1,2,3,4,2,1
    2,1,0,0,1,2,2,5,3,1
    3,2,1,0,1,1,4,6,2,1

R code::

    fn = 'distr2.txt'
    df = read.csv(fn,head=F)
    m = as.matrix(df)
    image(m,
      col=topo.colors(10))

And the graphic:

.. image:: /figures/distr2.png
   :scale: 50 %

Our goal is to sample this distribution using a Gibbs Sampler.

While the script (in ``script.py``) *is* 63 lines long, I contend that it's not complicated.  I'll paste the whole thing here first, so you can copy and run it, and then we'll go through its components.

.. sourcecode:: python

    import sys, random
    import matplotlib.pyplot as plt
    import numpy as np
    import utils

    def gibbsMove(L):
        # weight by score
        r = random.random()
        S = sum(L)
        sL = [n + 0.02 for n in L]
        fL = [n*1.0/S for n in sL]
        current = 0
        for i,f in enumerate(fL):
            current += f
            if r < current:
                return i
        raise ValueError('f < r')
    
    if __name__ == '__main__':
        fn = 'distr2.txt'
        data = utils.load_data(fn)
        data = data.strip().split('\n')
        L = list()
        for line in data:
            line = line.strip().split(',')
            line = [int(n) for n in line]
            L.append(line)
        # transpose the data, can select by cols
        T = zip(*L)
    
        R = len(L)
        C = len(T)
        # initial choice
        r = random.choice(range(R))
        c = random.choice(range(C))
        N = int(1E4)
        results = [(r,c)]
    
        for i in range(N):
            move = random.choice('rc')
            if move == 'r':
                r = random.choice(range(R))
                j = gibbsMove(L[r])
                results.append((r,j))
            else:
                c = random.choice(range(C))
                j = gibbsMove(T[c])
                results.append((j,c))
    
        for r in range(R):
            pL = [results.count((r,c)) for c in range(C)]
            pL = [str(n).rjust(6) for n in pL]
            print ''.join(pL)
    
        rL = [results.count((r,c)) for r in \
              range(R) for c in range(C)]
        A = np.array(rL)
        A.shape = (R,C)
        cm=plt.get_cmap('hot')
        plt.pcolor(A,cmap=cm)
        plt.colorbar()
        plt.savefig(fn.split('.')[0] + '.png')


Now let's break it down into pieces.  The only function is ``gibbs_move``:

.. sourcecode:: python

    def gibbsMove(L):
        # weight by score
        r = random.random()
        S = sum(L)
        sL = [n + 0.02 for n in L]
        fL = [n*1.0/S for n in sL]
        current = 0
        for i,f in enumerate(fL):
            current += f
            if r < current:
                return i
        raise ValueError('f < r')

What is going on in this function is that the argument is a list of the values from a particular column or row in the data.  We convert that list (of ints) into a list of floats.  For example, if the input was::

    1, 4, 0, 5, 10
    
The list fL would contain::

    0.05, 0.2, 0, 0.25, 0.5

Next, we generate a random number between 0 and 1.

Then we iterate through the list accumulating the values into ``current``.  When the random number is less than ``current``, we return that index.  This is just a way of sampling the distribution in the list passed into the function.  We make a random choice of the index to return in proportion to the value at the index.

In the first part of ``main``, it is all just setup

.. sourcecode:: python

    fn = 'distr2.txt'
    data = utils.load_data(fn)
    data = data.strip().split('\n')
    L = list()
    for line in data:
        line = line.strip().split(',')
        line = [int(n) for n in line]
        L.append(line)
    # transpose the data, can select by cols
    T = zip(*L)

We loaded the data and turned it into a matrix (a list of rows).  We use the transpose trick from :ref:`here <matrix-columns>`, to generate a second matrix indexed by column, then row.

.. sourcecode:: python

    R = len(L)
    C = len(T)
    # initial choice
    r = random.choice(range(R))
    c = random.choice(range(C))
    N = int(1E4)
    results = [(r,c)]

Then we generate initial values for the current row and column and set up a list ``results`` to hold the results.

The actual scoring is done in the third part of ``main``:

.. sourcecode:: python

    for i in range(N):
        move = random.choice('rc')
        if move == 'r':
            r = random.choice(range(R))
            j = gibbsMove(L[r])
            results.append((r,j))
        else:
            c = random.choice(range(C))
            j = gibbsMove(T[c])
            results.append((j,c))

    for r in range(R):
        pL = [results.count((r,c)) for c in range(C)]
        pL = [str(n).rjust(6) for n in pL]
        print ''.join(pL)

Starting from our current r,c we decide to change either the row or column, and we use the ``gibbsMove`` function to generate a new index.  We can print the results right now::

    > python script.py
    86    67   155   136    70    78    84    55    86    83
    59   128   268   222   107    48    47    32   324    68
    63   278   331   281   102    40    42    35    36    59
    70   189   174   160   115    68    71    55    52    62
    96    65    62    73   217    68    91    65    46    87
    95    52    58    62    59   223    65   115   115    92
     3     5     2     1    91    92   147   224   145    84
    85     1     0     1    79   156   195   223   107    76
   142    54     1     1    61   119   136   223   144    74
   180   100    41     0    39    53   203   261    95    65

But we can also get a little fancier and plot a heatmap with ``matplotlib``

.. sourcecode:: python

    rL = [results.count((r,c)) for r in \
         range(R) for c in range(C)]
    A = np.array(rL)
    A.shape = (R,C)
    cm=plt.get_cmap('hot')
    plt.pcolor(A,cmap=cm)
    plt.colorbar()
    plt.savefig(fn.split('.')[0] + '.png')

That is what we had above.