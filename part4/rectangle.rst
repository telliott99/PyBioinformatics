.. _rectangles:

##########
Rectangles
##########

.. sourcecode:: python

    import matplotlib.pyplot as plt

    ax = plt.axes()

    x = y = 0.3
    dx = 0.4
    dy = 0.2

    p = Rectangle((x,y),
            width=dx,height=dy,
            facecolor='purple',
            edgecolor='w')
              
    ax.add_patch(p) 
    t = ax.text(x+dx/2,y+dy/2,str(n),
                color=label_color,fontsize=12,
                fontname='Helvetica',
                ha='center',va='center')

.. image:: /figures/rectangle.png
   :scale: 50 %

Here is a biological example:

.. sourcecode:: python

    import random
    import matplotlib.pyplot as plt
    from pylab import get_cmap
    import numpy as np

    def make_random_DNA(N,GC=50.0):
        nt =  'GC' * int(GC * 10)
        nt += 'AT' * int((100.0-GC) * 10)
        n = N /len(nt) + 1
        rL = list(nt) * n
        random.shuffle(rL)
        return rL[:N]

    seq = make_random_DNA(10000,GC=50)
    print len(seq)

    N = 400  # length of insert
    n = 5    # no. of inserts
    inserts = make_random_DNA(N*n,GC=30)
    print len(inserts)

    for i in range(n):
        j = random.choice(range(len(seq)))
        if j + N > len(seq):
            d = len(seq) - j
            seq = seq[:j] + inserts[i*N:i*N + d]
        else:
            seq[j:j+N] = inserts[i*N:i*N+N]


    delta = 100
    R = range(0,len(seq),delta)
    L = list()
    for i in R:
        G = seq[i:i+delta].count('G')
        C = seq[i:i+delta].count('C')
        L.append(float(G+C))

    A = np.array(L)
    A /= delta
    A.shape=(10,len(A)/10)
    print A

    cm=get_cmap('Oranges')
    plt.pcolor(A,cmap=cm)
    plt.colorbar()
    plt.savefig('GC.png')

Here is the image.  We are looking for 5 sets of 4 blocks in a row that are low 'GC'.  I think I can see them.

.. image:: /figures/GC.png
   :scale: 50 %

And here is the data::

    [[ 0.41  0.47  0.43  0.48  0.53  0.53  0.51  0.62  0.4   0.46]
     [ 0.53  0.48  0.52  0.5   0.44  0.51  0.51  0.53  0.5   0.46]
     [ 0.51  0.5   0.52  0.49  0.47  0.46  0.48  0.31  0.29  0.31]
     [ 0.29  0.42  0.24  0.32  0.27  0.31  0.45  0.54  0.51  0.39]
     [ 0.51  0.55  0.53  0.5   0.46  0.43  0.44  0.56  0.46  0.5 ]
     [ 0.56  0.51  0.47  0.47  0.59  0.35  0.24  0.32  0.33  0.49]
     [ 0.46  0.53  0.51  0.57  0.56  0.52  0.36  0.31  0.38  0.37]
     [ 0.46  0.55  0.46  0.5   0.5   0.54  0.48  0.24  0.31  0.28]
     [ 0.24  0.45  0.59  0.54  0.46  0.48  0.42  0.53  0.56  0.45]
     [ 0.56  0.47  0.52  0.54  0.45  0.51  0.47  0.48  0.5   0.47]]

The default plot is from the lower right-hand corner.