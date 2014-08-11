.. _hiselection:

#########
Selection
#########

For each gene, we want to calculate the selection index (the ratio of total HITS in the lung compared to the library).  Ultimately we will be interested in those genes with a low selection index, indicating that strains bearing insertions in those genes did not survive well in the model infection.

In this plot, the y-axis is the selection index and the x-axis is saturation (fraction of TA sites in that gene which were hit by the transposon in the library).  Some genes just aren't sampled well by the transposon, and we exclude those from consideration.

.. image:: /figures/selection.png
   :scale: 50 %


The first part of this code is identical to that from the last section with the addition of two lines to load the sequence.

.. sourcecode:: python

    import matplotlib.pyplot as plt
    import utils

    data = utils.load_data('Hinf.txt')
    seq = data.strip().split('\n',1)[1]

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
    
    #----------------------------------------

    for g in sorted(gD.keys()):
        i,j = gD[g]
        L = [(x,cD1[x]) for x in cD1 if i <= x <= j]
        rL = list()
        count = 0
        for x,n in L:
            if seq[x:x+2] != 'TA':
                # print x
                continue
            count += n
            rL.append((x,n))
        sites_found = len(rL)

        total_sites = seq[i:j+1].count('TA')
        saturation = sites_found*1.0/total_sites
        if count == 0 or saturation < 0.2:
            continue
        print g, saturation,
    
        eL = [eD[x] for x in eD if i <= x <= j]
        selection_index = sum(eL)*1.0/count
        print selection_index

Before continuing, we make sure that nearly all of the sites are 'TA' sites with the ``print`` call above.

R code::

    setwd('Desktop')
    data = read.table('results.txt',head=F)
    color.list = rep('steelblue',length(data[,1]))
    sel = data[,3] < 0.15
    color.list[sel] = 'red'
    sel = data[,2] < 0.4
    color.list[sel] = 'lightgray'

    #sel = data[,2] < 0.4 & data[,3] < 0.15


    plot(data[,2],data[,3],
      col=color.list,log='y',pch=16,
    xlab='saturation',ylab='selection index')