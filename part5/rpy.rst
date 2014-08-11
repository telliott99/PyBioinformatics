.. _rpy:

##########
Using RPy2
##########


This section describes the basics of controlling R from Python using RPy2.

The first example shows how to process a phylogenetic ``tree$tip.label`` to color the names according to some scheme (say a clustering group).

We'll do a small first example, with six Gram-negative proteobacteria.  We grab the sequences using PyCogent:

.. sourcecode:: python

    L = [ ('Salmonella_typhi', {'id':'16758993',
                               'from':'287479',
                               'to':'289020'}),
          ('Escherichia_coli', {'id':'49175990',
                               'from':'4164682',
                               'to':'4166223'}),
          ('Pseudomonas_aeruginosa', {'id':'110645304',
                                     'from':'722096',
                                     'to':'723631'}),
          ('Haemophilus_influenzae', {'id':'M75081'}),
          ('Stenotrophomonas_maltophilia', {'id':'194363778',
                                           'from':'353034',
                                           'to':'354573'}),
          ('Haemophilus_influenzae', {'id':'L06164'}) ]

    from cogent.db.ncbi import EFetch

    for name,D in L:
        ef = EFetch(**D)
        data = ef.read()
        print '>' + name
        print data.strip().split('\n',1)[1]
        print
    print

.. sourcecode:: python

    python script.py > proteo.seqs.txt
    muscle -in proteo.seqs.txt -out proteo.align.txt

The R package we're using is ``ape``:

.. sourcecode:: python

    import sys
    from rpy2 import robjects
    from rpy2.robjects.packages import importr
    grdevices = importr('grDevices')

    ape = importr('ape')
    fn = 'proteo.align.txt'
    seqs = ape.read_dna(fn,format='fasta')
    dist = ape.dist_dna(seqs)
    tr = ape.nj(dist)

    print tr.names
    tip_labels = list(tr.rx2('tip.label'))
    for item in tip_labels:
        print item

    def get_color(n):
        D = { 'Steno':'maroon',
              'Kingella':'maroon',
              'Haemo':'DodgerBlue',
              'Salmonella':'magenta' }
        for k in D:
            if n.startswith(k):  return D[k]
        return 'darkgreen'

    color_list = [get_color(n) for n in tip_labels]
    color_list = robjects.StrVector(color_list)

    ofn = '/Users/telliott/Desktop/proteo_plot.pdf'
    grdevices.pdf(ofn)
    ape.plot_phylo(tr,tip_color=color_list,
        cex=1.5,x_lim=0.25)
    ape.nodelabels(cex=2)
    ape.axisPhylo()
    grdevices.dev_off()
    
We send instructions to R in the first part to load our aligned sequences, and use ``nj`` (neighbor-joining) to make the tree this time.  We print out the tree's ``$tip.label`` variable (below).  (Knowing how to ask RPy2 for the variable of interest can be a little tricky sometime.  In this example we're using a stand-in for the [[ ]] method of R lists.

Given a list of the tips as R sees them, we can make a corresponding list of colors easily from Python.  Then we pass that list back to R as a ``robjects.StrVector`` and do the plot as we would normally.

.. sourcecode:: python

    > python script.py
    [1] "edge"        "edge.length" "tip.label"   "Nnode"      

    Kingella_oralis
    Stenotrophomonas_maltophilia
    Pseudomonas_aeruginosa
    Haemophilus_influenzae
    Salmonella_typhi
    E_coli

This is pretty complex stuff, at least in terms of knowing what to do when the obvious things don't work.  I have a number of posts about it:

http://telliott99.blogspot.com/search/label/RPy2

Here is the plot:

.. image:: /figures/proteo_plot.png
   :scale: 50 %
   
And we can plot our nice collection of Streptococci using exactly the same method.  We had the group data in ``groups.txt`` and defined a function that we put in ``utils.py`` to extract the information into a dictionary.

We already have the tree file.  Now it's just a question of figuring out what colors we want.
   
.. sourcecode:: python
   

    from rpy2 import robjects
    from rpy2.robjects.packages import importr
    import utils

    D = utils.make_gid_dict('genomes.txt','groups.txt')

    ape = importr('ape')
    fn = '/Users/telliott_admin/Desktop/strep.tree.txt'
    tr = ape.read_tree(fn)
    tip_labels = tr[2]

    def f(s):
        colors = ['maroon','blue','magenta','red', 
                  'dodgerblue','salmon','black']
        g = D[s][0]
        return colors[g]

    color_list = [f(s) for s in tip_labels]
    color_list = robjects.StrVector(color_list)

    grdevices = importr('grDevices')
    ofn = '/Users/telliott/Desktop/strep_plot.pdf'
    grdevices.pdf(ofn)
    ape.plot_phylo(tr,tip_color=color_list)
    ape.axisPhylo()
    grdevices.dev_off()

.. sourcecode:: python

    > python script.py

Here is the plot:

.. image:: /figures/strep_plot.png
  :scale: 50 %


