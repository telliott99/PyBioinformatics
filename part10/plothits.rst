.. _plothits:

########
Plotting
########

**Our next-gen project**

.. image:: /figures/hemX.png
   :scale: 50 %
   
.. image:: /figures/rfaF.png
  :scale: 50 %


.. sourcecode:: python

    import matplotlib.pyplot as plt
    import utils

    def make_dict(L):
        D = dict()
        for k,v in L:
            D[int(k)] = int(v)
        return D
        
    def doit(fn):
        data = utils.load_data(fn)
        data = data.strip().split('\n')
        L = [e.split() for e in data]
        return make_dict(L)

    cD1 = doit('FD1.txt')
    cD2 = doit('FD2.txt')
    for k in cD2:
        if k in cD1:
            v = cD1[k] + cD2[k]
            cD1[k] = v
        else:
            cD1[k] = cD2[k]
            
    eD = doit('FD3.txt')

    data = utils.load_data('HI_genes.txt')
    data = data.strip().split('\n')
    gD = dict()
    for line in data:
        g,i,j,d = line.strip().split()
        gD[g] = (int(i),int(j))
    
    t = 'hemX'
    t = 'rfaF'
    i,j = gD[t]

    for k,D in enumerate([cD1,eD]):
        cL = [['blue','steelblue'],['red','salmon']][k]
        for x in sorted(D.keys()):
            if x < i-1000:  continue
            if x > j+1000:  continue
            y = D[x]
            if k == 1:
                y *= -1
            if x < i or x > j:
                plt.plot((x,x),(0,y),color='k',zorder=1)
                plt.scatter(x,y,s=25,color=cL[1],zorder=2)
            else:
                plt.plot((x,x),(0,y),color='k',zorder=1)
                plt.scatter(x,y,s=25,color=cL[0],zorder=2)

    ax = plt.axes()
    p = plt.Rectangle((i,-10),
            width=j-i,height=20,
            facecolor='0.8',edgecolor='w')

    ax.text(i + (j-i)/2,40,t,
            color='red',fontsize=24,
            fontname='Helvetica',
            ha='center',va='center')

    ax.add_patch(p)
    plt.savefig(t + '.png')