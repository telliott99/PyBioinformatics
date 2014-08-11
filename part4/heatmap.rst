.. _heatmap:

#########
Heat Maps
#########

The essence of a heat map is to transform an array of data into a picture, with colors or shades of gray to indicate the values.  We've actually seen that already.

The new questions for us are whether we should we bin the data?   And, can we print the values on the plot?  By binning the data I mean to have a fixed set of colors for the boxes, and plot according to some scheme for binning.

It's possible to write a very nice heatmap script in 100 lines or so, using the ``Rectangle`` class to organize things, perhaps after using a ``grid`` function to do the basic layout.

Here's a link:

http://telliott99.blogspot.com/2011/03/dental-project-5.html

The question for this section is, given this:

.. sourcecode:: python

    import matplotlib.pyplot as plt
    import matplotlib.pylab as pylab
    import numpy as np

    A = np.array(range(12))
    A.shape = (3,4)

    cm=plt.get_cmap('gist_rainbow')
    plt.pcolor(A,cmap=cm)
    plt.colorbar()
    plt.savefig('heatmap1.png')

.. image:: /figures/heatmap1.png
  :scale: 50 %

This code is trivial, so it begs the question:  can we let ``matplotlib`` make our heatmap in a line or two, and then get the number printed afterward.

If we're really doing well, can we get borders drawn on the cells?

In this strategy, we need to interrogate the object returned by the call ``plt.pcolor`` to find where it actually plotted things.  It turned out to be a little awkward to extract the coordinates for the center of each box, but it can be done.  Perhaps there is a better way I don't know about.

.. sourcecode:: python

    import matplotlib.pyplot as plt
    import matplotlib.pylab as pylab
    import numpy as np

    A = np.array(range(12))
    A.shape = (3,4)

    cm=plt.get_cmap('gist_rainbow')
    stuff = plt.pcolor(A,cmap=cm)

    pL = stuff.get_paths()
    p = pL[0]
    dx = (p.vertices[2][0] - p.vertices[1][0])/2.0
    dy = (p.vertices[1][1] - p.vertices[0][1])/2.0

    cL = list()
    for i in range(len(pL)):
        v = pL[i].vertices
        cL.append((v[0][0]+dx,v[0][1]+dy))

    for i in range(len(cL)):
        x,y = cL[i]
        plt.text(x,y,str(i+1),
            color='k',fontsize=36,
            fontname='Helvetica',
            ha='center',va='center')
    
    plt.colorbar()
    plt.savefig('heatmap2.png')

.. image:: /figures/heatmap2.png
  :scale: 50 %
