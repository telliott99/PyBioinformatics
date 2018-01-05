.. _circles:

#######
Circles
#######

Plotting circles is easy, that's what ``plt.scatter`` does.

In this example we define a new function ``grid`` that computes coordinates for an xy-grid.  It takes as input the number of rows and columns.  The ``docstring`` tells the overall story.

The heavy lifting is done by ``np.linspace``

>>> import numpy as np
>>> np.linspace(0,1,5)
array([ 0.  ,  0.25,  0.5 ,  0.75,  1.  ])
>>>


.. sourcecode:: python

    def grid(nrow,ncol):
        '''
        Return a dictionary with (0..nrow, 0..col) as keys, 
        and multipliers for x,y values to make a grid as values
        e.g. with nrow = 5, multipliers are 0, 0.25, 0.5, 0.75, 1.0
        '''
        rL = np.linspace(0,1,nrow)
        cL = np.linspace(0,1,ncol)
        D = dict()
        for i in range(nrow):
            for j in range(ncol):
                D[i,j] = (rL[i],cL[j])
        return D
    
We put the code for the ``grid`` function into ``utils.py``.  We can test it by running the following script

.. sourcecode:: python

    import matplotlib.pyplot as plt
    import utils

    def show(D):
        for k in D:
            x,y = D[k]
            plt.scatter(x,y,s=500,
                c=str(x*0.5 + y*0.5))
                
    D = utils.grid(5,8)
    show(D)
    ax = plt.axes()
    ax.set_xlim(-0.1,1.1)
    ax.set_ylim(-0.1,1.1)
    plt.savefig('grid.png')

.. sourcecode:: python

    python script.py


.. image:: /figures/grid.png
    :scale: 50 %

Now we'd like to do something a little fancier.  A while back, we obtained the text for *Ulysses* on the web.  Let's count the frequency of two-letter combinations within words of the book.  We define a function that makes a dictionary of word counts:

.. sourcecode:: python

    def make_word_count_dict(wL):
        wD = dict()
        for w in wL:
            w = w.lower()
            for m,n in zip(w[:-1],w[1:]):
                k = m+n
                if k in wD:
                    wD[k] += 1
                else:
                    wD[k] = 1
        return wD
    
The only unusual thing is this ``zip(w[:-1],w[1:])``.  You can see what it does:

>>> L = list('abcde')
>>> zip(L[:-1],L[1:])
[('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e')]
>>>

The other function does the plotting.  We find the index of each letter within ``lc``, the lowercase letters, to find the xy-coordinates for the two-letter combination.

D is the dictionary we're getting from ``grid()``.  We get the actual count from the word count dictionary wD, then appropriately scale and color the dot we're going to plot.

.. sourcecode:: python

    def plot_word_count_dict(D,wD,lc,scale):
        import matplotlib.pyplot as plt
        for i,u in enumerate(lc):
            for j,v in enumerate(lc):
                x,y = D[(i,j)]
                try:
                    n = wD[u+v]
                except KeyError:
                    n = 1
                n = 10* scale(n)
                if n < 10:
                    n = 25
                    c = '0.7'
                    e = 'w'
                elif u in 'aeiou' or v in 'aeiou':
                    c = 'maroon'
                    e = 'k'
                else:
                    c = 'salmon'
                    e = 'k'
                plt.scatter(x,y,
                    edgecolor=e,s=n,c=c)

We put both of these functions into ``utils.py`` as well.  Now we just write a little script to run the show:

.. sourcecode:: python

    import math
    from string import lowercase as lc
    import matplotlib.pyplot as plt
    import numpy as np
    import utils
                
    fn = 'ulysses.txt'
    data = utils.load_data(fn)
    words = data.strip().split()[:100000]
    wD = utils.make_word_count_dict(words)
    D = utils.grid(26,26)
    utils.plot_word_count_dict(
        D,wD,lc,scale=math.log)

    ax = plt.axes()
    ax.set_xlim(-0.1,1.1)
    ax.set_ylim(-0.1,1.1)
    plt.savefig('letter_counts.png')


.. sourcecode:: python

    > python script.py

Nothing new here.  

Here is the result:

.. image:: /figures/letter_counts.png
    :scale: 50 %

In order to avoid doing the layout for the letters, I colored the vowels differently.

