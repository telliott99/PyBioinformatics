.. _phylo:

###########
Simple tree
###########

In this section, we're going to start with a list of half a dozen sequences in Genbank (16S rRNA gene sequences from bacteria).  We'll grab the sequences, align them, construct a phylogenetic tree, and plot the results.

Let's start with a file (``achromo.species.txt``) containing in columns the Genbank ids, a 'short name', a more complete name for each::

.. sourcecode:: bash

    AF411020  Ax1  Achromobacter xylosoxidans AU1011
    EU373389  Ax2  Achromobacter xylosoxidans TPL14
    AJ278451  Ax3  Achromobacter xylosoxidans denitrificans
    AF411019  Ax4  Achromobacter xylosoxidans AU0665
    DQ450530  Aa1  Alcaligenaceae bacterium LBM
    AJ002809  Aa2  Alcaligenes sp.

In this data, I've separated the fields with 2 spaces for readability.  It might make more sense in many cases to use a comma or a tab ('\t') or some other symbol, as long as it doesn't occur in any of the items.  

It could get tricky with the spaces here since the entries in the third column also contain spaces.  But the first and second columns don't have any, so we can do something like this in ``script.py``

.. sourcecode:: python

    import utils
    fn = 'achromo.species.txt'
    data = utils.load_data(fn)
    data = data.strip().split('\n')
    iL = [t.split()[0] for t in data]
    nL = [t.split()[1] for t in data]
    
    print iL[:3]

.. sourcecode:: python

    > python script.py
    ['AF411020', 'EU373389', 'AJ278451']
    
    
Now we add to that listing the code to fetch the data from Genbank

.. sourcecode:: python

    import urllib2
    eutils = 'http://www.ncbi.nlm.nih.gov/entrez/eutils/'
    efetch = 'efetch.fcgi?'

    s = 'id=' + ','.join(iL)
    url = eutils + efetch + s
    url += '&db=nucleotide&rettype=fasta'
    f = urllib2.urlopen(url)
    data = f.read().strip()

    fn = 'achromo.seqs.txt'
    FH = open(fn,'w')
    FH.write(data)
    FH.close()

We don't want to ask the Genbank servers again, so save the sequences to disk.  Now let's take a look.  Make a new version of ``script.py``

.. sourcecode:: python

    from utils import load_data
    fn = 'achromo.seqs.txt'
    data = load_data(fn)
    entries = data.split('\n\n')
    for e in entries:
        title, seq = e.split('\n',1)
        print title.split()[0]
        print seq[:40]
        print

Output::

    > python script.py 
    >gi|15384334|gb|AF411020.1|
    AGTTTGATCCTGGCTCAGATTGAACGCTAGCGGGATGCCT

    >gi|171191189|gb|EU373389.1|
    TCGGAGAGTTTGATCCTGGCTCAGATTGAACGCTAGCGGG

    >gi|92919431|gb|DQ450530.1|
    ATTAGAGTTTGATCCTGGCTCAGATTGAACGCTAGCGGGA

    >gi|21436540|emb|AJ278451.1|
    AGAGTTTGATCATGGCTCAGATTGAACGCTAGCGGGATGC

    >gi|15384333|gb|AF411019.1|
    AGTTTGATCCTGGCTCAGATTGAACGCTAGCGGGATGCCT

    >gi|2832590|emb|AJ002809.1|
    ATTGAACGCTAGCGGGATGCCTTACACATGCAAGTCGAAC

Those title lines are awkward (I've truncated them).  Here 

http://www.ncbi.nlm.nih.gov/nuccore/15384334?report=fasta 

is a link to the first record at NCBI.

Let's replace the long titles with the short names from ``achromo.species.txt``.  Make a new version of ``script.py`` with the very first block of code at the top above (leaving out the last line with the ``print`` statement), then supplement with this

.. sourcecode:: python

    data = utils.load_data('achromo.seqs.txt')
    for line in data.strip().split('\n'):
        for genbankid, name in zip(iL,nL):
            if genbankid in line:
                line = '>' + name
                continue
        print line
    
If you run ``python script.py`` it will print all of the sequences with their new title lines.  An easy way to save the modified data is to do a 'redirect'

http://en.wikipedia.org/wiki/Redirection_(computing) 

from the command line:

.. sourcecode:: python

    python script.py > achromo.mod.txt

Inspect the contents of ``achromo.mod.txt`` to see that it seems correct.

.. _muscle:

**muscle**

The next step is to align the sequences.  We could use ``clustal`` but I also like muscle *a lot*:

http://www.drive5.com/muscle

Output::

    > muscle -in achromo.mod.txt -out achromo.align.txt

    MUSCLE v3.6 by Robert C. Edgar

    http://www.drive5.com/muscle
    This software is donated to the public domain.
    Please cite: Edgar, R.C. Nucleic Acids Res 32(5), 1792-97.

    seqs.mod 6 seqs, max length 1523, avg  length 1498
    00:00:00     10 MB(2%)  Iter   1  100.00%  K-mer dist pass 1
    00:00:00     10 MB(2%)  Iter   1  100.00%  K-mer dist pass 2
    00:00:01     10 MB(2%)  Iter   1  100.00%  Align node       
    00:00:01     10 MB(2%)  Iter   1  100.00%  Root alignment
    00:00:01     10 MB(2%)  Iter   2  100.00%  Root alignment
    00:00:03     10 MB(2%)  Iter   3  100.00%  Refine biparts


Actually, these sequences are so closely related, there aren't any gaps.  Now, to make a phylogenetic tree with :ref:`FastTree <FastTree>`::

    > FastTree -nt achromo.align.txt > achromo.tree.txt
    
It looks like this::

    (Ax1:0.00068,Ax4:0.00014,
    ((Aa2:0.00611,Ax2:0.00014)0.935:0.00259,
    (Ax3:0.00401,Aa1:0.00260)0.949:0.00345)0.767:0.00068);
    
I've broken up the output so it'll fit.  

Finally, I'm going to plot it using the ``ape`` package in R::

    > library(ape)
    > setwd('Desktop')
    > tr = read.tree('achromo.tree.txt')
    > plot(tr,edge.width=3,cex=2,type='unrooted')
    
.. image:: /figures/tree1.png
   :scale: 50 %

That's a little ugly.  For now, let's fix it by plotting it as a rooted tree (though we know better) using the root chosen by ``ape``::

    > plot(tr,edge.width=3,cex=2)

.. image:: /figures/tree2.png
   :scale: 50 %

* Find out more about R

http://www.r-project.org/

* Selection of blog posts

http://telliott99.blogspot.com/search/label/R


