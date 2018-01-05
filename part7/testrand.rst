.. _testrand:

############
Significance
############

Before we leave this example, I'd like to try to test the significance of the results.  One way to do this is to shuffle the DNA sequence (so that it has the same composition), and then re-run the search for sites.

I also modified the code slightly to transform the site scores to integers (multiplied by 10):

.. sourcecode:: python

    for f in result:
        if f > 12:
            print int(10*f)
        
The shuffle code is just:

.. sourcecode:: python

    if 1:
        dna = list(dna)
        random.shuffle(dna)
        dna = ''.join(dna)
    
All of that goes into ``script.py`` from ____

Just run with a redirect::

    > python script.py > EC_high.txt
    > python script.py > rand_high.txt
    
The first run is with ``if 0`` above, the second with ``if 1``.  Code to plot this is:

.. sourcecode:: python

    import os
    import matplotlib.pyplot as plt
    import numpy as np
    import Counter

    path = os.getcwd()
    ECfn = 'EC_high.txt'
    rfn = 'rand_high.txt'

    L = list()
    t = 10

    for fn in [ECfn,rfn]:
        FH = open(path + '/' + fn,'r')
        data = FH.read().strip()
        FH.close()
        data = [float(n) for n in data.split('\n')]
        data = [n for n in data if n > t]
        L.append(Counter.Counter(data))

    C0 = L[0]
    X0 = np.array(sorted(C0.keys()))
    Y0 = [C0[i] for i in X0]
    C1 = L[1]
    X1 = np.array(sorted(C1.keys()))
    Y1 = [C1[i] for i in X1]
    plt.bar(X0,Y0,color='red')
    plt.bar(X1,Y1,color='yellow')
    plt.savefig(path + '/test_random.png')
    
    
.. image:: /figures/test_random.png
   :scale: 50 %

The point is that although the extreme high values are clearly higher in the real sequence, for a scoring range like 110 - 120 (that is 11.0 - 12.0 in the original scheme), the ratio of the likelihoods for the two models (*E. coli* v. random) is not even greater than 2. So, upon observing a site with a value of 11.5, say, its significance isn't clear.

One idea that would improve the significance is to note that the genome is (obviously) subject to selection. For the Crp system to work properly, there has likely been selection against randomly placed sites, so the random model is not really the appropriate one to test against.
   