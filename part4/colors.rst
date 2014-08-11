.. _colors:

######
Colors
######

Here is a blog post about colors:

http://telliott99.blogspot.com/2008/08/colors-for-heat-maps.html

I wanted to get the right colors for heat maps, and of course, the red <=> black <=> green standard is a spectacularly bad idea (though I have to say that, having talked to affected individuals, it's not clear what would be better).

I like the topo.colors from R.

.. image:: /figures/topo_R.png
    :scale: 50 %

In R::

    setwd('Desktop')
    v = topo.colors(1000)
    write.table(v,'topo.colors.txt')

Looks a little weird, but OK::

    "x"
    "1" "#4C00FFFF"
    "2" "#4C00FFFF"

Here is the code to analyze and plot

.. sourcecode:: python

    import matplotlib.pyplot as plt
    import utils

    data = utils.load_data('topo.colors.txt')
    L = data.strip().split('\n')[1:]
    r = list()
    g = list()
    b = list()
    for e in L:
        s = e.strip().split()[1][2:]
        r.append(s[:2])
        g.append(s[2:4])
        b.append(s[4:6])

    R = range(1000)
    for hL,c in zip((r,g,b),list('rgb')):
        iL = [int(h,16) for h in hL]
        plt.scatter(R,iL,color=c,s=5)

    for i in R:
        c = L[i].split()[1][1:8]
        plt.scatter(i,-25,color=c,s=50)

    plt.savefig('colors.png')
    
And the plot:

.. image:: /figures/topo_colors.png
    :scale: 50 %

matplotlib has something called ``colormaps``.

there are a bunch of them built-in 

http://matplotlib.sourceforge.net/examples/pylab_examples/show_colormaps.html

.. sourcecode:: python

    import matplotlib.pyplot as plt
    import matplotlib.pylab as pylab
    import numpy as np

    A = np.array(range(200))
    A.shape = (20,10)

    cm=plt.get_cmap('gist_rainbow')
    plt.pcolor(A,cmap=cm)
    plt.colorbar()
    plt.savefig('rainbow_cm.png')

.. image:: /figures/rainbow_cm.png
    :scale: 50 %


Do we want to try to build our own

http://telliott99.blogspot.com/2009/12/matplotlib-topocolors.html
 
.. sourcecode:: python
   
    import matplotlib.pyplot as plt
    import matplotlib
    import numpy as np

    # topo colors
    r = ((0.000, 0.000, 0.297),
         (0.084, 0.000, 0.000),
         (0.418, 0.000, 0.000),
         (0.667, 0.895, 0.895),
         (0.668, 1.000, 1.000),
         (1.000, 1.000, 1.000))

    g = ((0.000, 0.000, 0.000),
         (0.084, 0.000, 0.000),
         (0.334, 0.895, 0.895),
         (0.335, 1.000, 1.000),
         (0.667, 1.000, 1.000),
         (0.850, 0.863, 0.863),
         (1.000, 0.875, 1.000))

    b = ((0.000, 0.000, 1.000),
         (0.334, 1.000, 1.000),
         (0.335, 0.297, 0.297),
         (0.418, 0.000, 0.000),
         (0.667, 0.000, 0.000),
         (1.000, 0.700, 1.000))

    colors = {'red':r, 'green':g, 'blue':b}

    f = matplotlib.colors.LinearSegmentedColormap
    m = f('my_color_map', colors, 256)
    A = np.array(range(100))
    A.shape = (10,10)
    plt.pcolor(A,cmap=m)
    plt.colorbar()
    plt.savefig('topo_cm.png')
 
.. image:: /figures/topo_cm.png
    :scale: 50 %

What's going on here?  First of all, I generated the color map above by hand, eyeballing the values from the figure above.

Second, the rgb values can vary independently over different ranges.  Suppose we just look just at red::

    r = ((0.000, 0.000, 0.297),
         (0.084, 0.000, 0.000),
         (0.418, 0.000, 0.000),
         (0.667, 0.895, 0.895),
         (0.668, 1.000, 1.000),
         (1.000, 1.000, 1.000))
     
These 3-tuples are mark, start, finish.

What this means is that during the interval from the beginning up to the mark at ``0.000``, that is, immediately, the r-value went from ``0.0`` to ``0.297`` (``76/256``).  That's where we start.  

At the next mark, ``0.084``, the r-value is ``0.0`` (``r[1,1]`` and stays at ``0.0`` until ``0.418``.  Then during the interval from ``0.418`` to ``0.667``, it changes from ``0.0`` to ``0.895``.  At the ``0.667`` mark, the r-value changes immediately to ``1.0`` and stays there.

To put this another way, at each mark, the color map records the value the color had at the entry and the exit of that mark.  

This allows for jumps.  

The transition from the first mark at ``0.0`` to ``0.084`` is figured from the last value of the starting interval up to the first mark (column 1) of the ending interval.  So the interval from ``0.0`` to ``0.084`` changes the r-value from ``0.297`` to ``0.000``.  Similarly, the interval from ``0.418`` to ``0.667`` changes the r-value from ``0.0`` to ``0.895``.

A colormap is fine if we're doing ``plt.pcolor(A,cmap=cm)`` with some array, and making a heatmap.  What if we want to recover the colors evenly spaced over some particular range?

http://http://stackoverflow.com/questions/3016283/create-a-color-generator-in-matplotlib

>>> import matplotlib.pyplot as plt 
>>> cm=plt.get_cmap('gist_rainbow')
>>> for i in range(11):
...     j = i/10.0
...     print cm(j)
... 
(1.0, 0.0, 0.16470588743686676, 1.0)
(1.0, 0.36470588141796634, 0.0, 1.0)
(1.0, 0.89803920785586044, 0.0, 1.0)
(0.56235303467395259, 1.0, 0.0, 1.0)
(0.030588270016018541, 1.0, 0.0, 1.0)
(0.0, 1.0, 0.51895421268159725, 1.0)
(0.0, 0.94588235616683958, 1.0, 1.0)
(0.0, 0.41019602749901846, 1.0, 1.0)
(0.12156863063573838, 0.0, 1.0, 1.0)
(0.65490205989220174, 0.0, 1.0, 1.0)
(1.0, 0.0, 0.80784314870834351, 1.0)

The last value is the transparency, which we can ignore.  Otherwise, we just get a tuple of rgb values.  So it's as simple as ``calling`` cm with the fractional value we seek.
