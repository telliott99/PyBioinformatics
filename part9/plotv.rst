.. _plotv:

#####################
Visualizing variation
#####################

.. sourcecode:: python

    import matplotlib.pyplot as plt
    import utils

    data = utils.load_data('counts.txt')
    X = list()
    Y = list()

    for e in data.strip().split('\n'):
        i, nt, o, info = e.strip().split()
        i = int(i)
        if info == 'gap':
            continue
        if i > 600:
            continue
        X.append(i)
        Y.append(float(info))

    plt.plot(X,Y,lw=2)

    V1 = (60,106)
    plt.plot(V1,(0,0),lw=20,color='r')
    V3 = (368,497)
    plt.plot(V3,(0,0),lw=20,color='r')

    plt.savefig('vbars.png')

.. image:: /figures/vbars.png
   :scale: 50 %
   
.. sourcecode:: python

    import matplotlib.pyplot as plt
    import numpy as np
    import utils

    data = utils.load_data('counts.txt')
    X = list()
    Y = list()

    for e in data.strip().split('\n'):
       i, nt, o, info = e.strip().split()
       i = int(i)
       if info == 'gap':
           continue
       X.append(i)
       Y.append(float(info))

    aL = list()
    w = 20
    T = 1.8
    for i in range(len(Y)):
       j, k = i - w, i + w + 1
       if j < 0:  j = 0
       if k > len(Y):  k = len(Y)
       m = utils.mean(Y[j:k])
       aL.append(m)

    X = np.array(X) + w/2

    plt.plot((1,1451),(T,T),lw=2,color='r',zorder=0)
    plt.scatter(X,aL)
    ax = plt.axes()
    ax.set_xlim(-5,1455)
    ax.set_ylim(0.8,2.05)
    plt.savefig('16Swindow.png')
   
.. image:: /figures/16Swindow.png
   :scale: 50 %
