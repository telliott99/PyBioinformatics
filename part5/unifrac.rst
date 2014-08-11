.. _unifrac:

#######
Unifrac
#######

I want to briefly cover analysis of the population structure of microbial communities using the Unifrac metric, developed by Rob Knight and colleagues.  I've posted extensively about this

http://telliott99.blogspot.com/search/label/Unifrac

and there is plenty more on their website 

http://bmf2.colorado.edu/unifrac/tutorial.psp
http://bmf2.colorado.edu/fastunifrac/

and in the PyCogent docs

http://pycogent.sourceforge.net/examples/unifrac.html

The idea is that starting from a phylogenetic tree containing sequences from different populations, like this idealized one:

.. image:: /figures/unifrac0.png
   :scale: 50 %

one can determine something about how closely related the two populations are.

A metric for that is to total up the amount of branch length in parts of the tree that is unique to either one of two populations in a pairwise comparison (all leaf nodes below a certain point are from only one population).  The more distinct the two groups, the larger this value will be.  Various statistical analyses can be done including resampling, for significance.  What's especially nice is that a technique related to PCA called PCoA (Principal Coordinate Analysis) can take a distance measure like this and create a plot that maximizes the variation in two dimensions.

The example I'm going to do is bare bones.  In fact, this is not a great example because the sequences are typestrains from individual bacterial phyla or sub-phyla.  But it's easy to set up and it shows the mechanics of what to do.

We'll grab some sequences, align them and make a tree, and then run the analysis.  Finally, we'll make a plot of the results from PCoA.

The sequences we'll use are typestrains (not real environmental sequences)::

    AJ131916.1     Stenotrophomonas_maltophilia
    Z76653.1       Pseudomonas_alcaligenes_16S
    EU009197.1     Shigella_sonnei_FBD023

    L06164.1       Kingella_oralis
    EF522133.1     Comamonas_testosteroni_CU101

    AB053940.1     Tannerella_forsythensis_HA3
    L16469.1       Prevotella_melaninogenica_25845
    AF133536.1     Capnocytophaga_sputigena

    AY005045.1     Streptococcus_mitis_bv2
    AY485606.1     Streptococcus_gordonii_10558
    AY518677.1     Streptococcus_mitis_Sm91

    AJ401017.1     Thermotoga_maritima_SL7

The above listing is in the file ``genbank_ids.txt``.  We put the following into ``script.py`` and do a redirect to file with ``python script.py > seqs.txt`` in the usual way.

.. sourcecode:: python

    from cogent.db.ncbi import EFetch
    import utils

    data = utils.load_data('genbank_ids.txt')
    L = data.strip().split('\n')
    for line in L:
        if not line:
            continue
        gid,name = line.strip().split()
        ef = EFetch(id=gid)
        print ef.read()
    
The sequences have those long Genbank title lines that I don't like, so we'll run another script (again with redirect ``python script.py > seqs.mod.txt``:

.. sourcecode:: python

    from cogent.db.ncbi import EFetch
    import utils

    data = utils.load_data('genbank_ids.txt')
    data = data.strip().split('\n')
    D = dict()
    for line in data:
        if not line:
            continue
        gid,name = line.strip().split()
        D[gid] = name

    data = utils.load_data('seqs.txt')
    L = data.strip().split('\n\n')
    for fasta in L:
        title, seq = fasta.strip().split('\n',1)
        for k in D:
            if k in title:
                title = '>' + D[k]
                break
        print title
        print ''.join(seq.strip().split())
        print

The code to load the dictionary is repeated, and this isn't a good thing, so you could easily factor it out and put it in ``utils.py`` if you wanted to.

We use :ref:`muscle <muscle>` and :ref:`FastTree <FastTree>` in the usual way::

    muscle -in seqs.mod.txt -out seqs.aln.txt
    FastTree -nt seqs.aln.txt > tree.txt

Now, here's something important:  the tree must be rooted.  The best way to do that without a complex approach is to use an outgroup (that's why we have the *Thermotoga* strain in the sequence set).  We need to explicitly root the tree, and I'm going to use R for that::

    > library('ape')
    > setwd('Desktop')
    > tree = read.tree('tree.txt')
    > plot(tree)
    > tree$tip.label
     [1] "Stenotrophomonas_maltophilia"    "Kingella_oralis"                
     [3] "Comamonas_testosteroni_CU101"    "Streptococcus_gordonii_10558"   
     [5] "Streptococcus_mitis_bv2"         "Streptococcus_mitis_Sm91"       
     [7] "Thermotoga_maritima_SL7"         "Capnocytophaga_sputigena"       
     [9] "Tannerella_forsythensis_HA3"     "Prevotella_melaninogenica_25845"
    [11] "Shigella_sonnei_FBD023"          "Pseudomonas_alcaligenes_16S"    
    > tree2 = root(tree,7)
    > plot(tree2)
    > write.tree(tree2,'tree2.txt')

The plot from R is here:

.. image:: /figures/unifrac1.png
   :scale: 50 %

The next step is to make a file (``environ.txt``) that tells which 'environment' each sample comes from::

    Stenotrophomonas_maltophilia  A
    Pseudomonas_alcaligenes_16S  A
    Shigella_sonnei_FBD023  A
    Kingella_oralis  B
    Comamonas_testosteroni_CU101  B
    Eikenella_corrodens  B
    Achromobacter_xylosoxidans_AU1011  B
    Tannerella_forsythensis_HA3  C
    Prevotella_melaninogenica_25845  C
    Capnocytophaga_sputigena  C
    Streptococcus_mitis_bv2  D
    Streptococcus_gordonii_10558  D
    Streptococcus_mitis_Sm91  D

Notice that we just leave the outgroup out of that file.

The code to actually do the analysis is one or two lines.  We'll do the plot with ``matplotlib``.

.. sourcecode:: python

    from cogent import LoadTree
    from cogent.maths.unifrac.fast_unifrac import fast_unifrac
    import matplotlib.pyplot as plt

    # convert our environment file repr into a dict
    FH = open('environ.txt','r')
    data = FH.read().strip()
    FH.close()
    L = data.split('\n')
    env_dict = dict()
    for e in L:
        seq_name, sample = e.strip().split()
        env_dict[seq_name] = {sample:1}

    tr = LoadTree('tree2.txt')
    result = fast_unifrac(tr, env_dict)
    print result['distance_matrix']
    pca = result['pcoa']
    print pca

    X = pca.getRawData('vec_num-0')[:4]
    Y = pca.getRawData('vec_num-1')[:4]
    for x,y,name in zip(X,Y,'ABCD'):
        plt.scatter(x,y,s=150,color='blue')
        plt.text(x+0.03,y+0.03,name,va='center',
            fontsize=16)
        
    ax = plt.axes()
    ax.set_xlim(-0.7,0.7)
    ax.set_ylim(-0.7,0.7)
    plt.grid()
    plt.savefig('unifrac2.png')

Here is the output::

    > python unifrac.py 
    /Library/Python/2.6/site-packages/cogent/util/progress_display.py:28: UserWarning: Not using MPI as mpi4py not found
      from cogent.util import parallel, terminal
    (array([[ 0.        ,  0.83249614,  1.        ,  0.94210318],
           [ 0.83249614,  0.        ,  1.        ,  0.93071831],
           [ 1.        ,  1.        ,  0.        ,  1.        ],
           [ 0.94210318,  0.93071831,  1.        ,  0.        ]]), ['A', 'B', 'C', 'D'])
    ===========================================================================
            Type              Label  vec_num-0  vec_num-1  vec_num-2  vec_num-3
    ---------------------------------------------------------------------------
    Eigenvectors                  A      -0.28       0.25      -0.41       0.00
    Eigenvectors                  B      -0.29       0.19       0.43       0.00
    Eigenvectors                  C       0.62       0.15       0.01       0.00
    Eigenvectors                  D      -0.05      -0.59      -0.03       0.00
     Eigenvalues        eigenvalues       0.55       0.46       0.35      -0.00
     Eigenvalues  var explained (%)      40.52      34.06      25.42      -0.00
    ---------------------------------------------------------------------------

And the plot:

.. image:: /figures/unifrac2.png
   :scale: 50 %
   
As expected, the sequences from the gamma- and beta-*Proteobacteria* (A and B) are more closely related than those from *Bacteroidetes* (C) or the *Streptococci* (D).