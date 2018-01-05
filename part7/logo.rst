.. _logo:

####
Logo
####

As long as we're doing site classification we should have a Logo.  

http://www.ccrnp.ncifcrf.gov/~toms/glossary.html#sequence_logo

I have to start over again from the file ``crp.data.txt`` because we calculate a little differently for this.

.. image:: /figures/Crp_sites.png
   :scale: 50 %

Here goes:

.. sourcecode:: python

    import sys
    import matplotlib.pyplot as plt
    import utils

    fn = 'crp.dat.txt'
    cL = utils.get_crp_site_counts(fn)

    N = len(cL)
    ax = plt.axes()
    colors = ['MediumSeaGreen','SteelBlue','Coral','Crimson']
    correction = 0.018

    for i,D in enumerate(cL):  
        L = list()
        for nt in 'acgt':
            c = D[nt]
            if c == 0:
                L.append(1)
            else:  
                L.append(c)
        S = sum(L)
        fL = [n*1.0/S for n in L]
        hL = [utils.log2(f)*f for f in fL]
        H = -sum(hL)
        info = 2 - H - correction
        y0 = 0
        for f,nt in sorted(zip(fL,'acgt')):
            h = info*f
            if h < 0:  h = 0
            c = colors['acgt'.index(nt)]
            r = plt.Rectangle((i,y0),width=1,
                   height=h,facecolor=c)
            ax.add_patch(r)
            y0 += info*f

    for i,nt in enumerate('ACGT'):
        plt.text(15+(N/15)*i,1.8,nt,
            color =colors[i],fontsize=30)

    ax.set_xlim(0,N)
    ax.set_ylim(-0.05,2.05)
    ax.set_title('Crp sites')
    ax.set_ylabel('bits')
    plt.savefig('Crp_sites.png')


