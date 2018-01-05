.. _coligenes:

###
Map
###

In the last section we obtained the positions of all the high-scoring Crp binding sites in the DNA sequence of the *E. coli* MG1655 genome.  The next step is obviously to map those positions with respect to the genes.  For last time, I used a file with only the DNA sequence, so now we have to go back to Genbank and get the whole record.  I followed exactly the same approach as in the :ref:`cogent` section.

For this write-up, I wanted to be sure that I had actually used the same script.  One way to make sure of that is to test the old and the new files for differences using the Unix ``diff`` tool.  From the command line::

    > diff fetchEC.py fetchST.py
    29,30c29,30
    <     gid = 'U00096.2'
    <     gb_fn = 'EC_genome.gb'
    ---
    >     gid = 'AE006468'
    >     gb_fn = 'seq.gb'

Even better, TextMate knows how to syntax color such a file:

.. image:: /figures/diff.png
   :scale: 50 %
   
Similar to last time we do ``python fetchEC.py > EC_genes.txt``

But then, I remember that there is a problem.  We need to modify the ``location`` for each gene so that we're using Python-style indexing internally.  We should subtract 1 from each index.  The output is::

    thrL   189 254 cw
    thrA   336 2798 cw
    thrB   2800 3732 cw
    thrC   3733 5019 cw
    yaaX   5233 5529 cw

Now, let's see what we've got.  Here is ``script.py``:

.. sourcecode:: python

    import utils
    data = utils.load_data('EC_genome.txt')
    seq = data.strip().split('\n')[1]

    data = utils.load_data('EC_crp_results.txt')
    sites = list()
    for line in data.strip().split('\n'):
        s,score = line.strip().split()
        score = float(score)
        sites.append([score,s])
    sites.sort(reverse=True)

    # this always works, and shouldn't
    for i,site in enumerate(sites):
        s = site[1]
        j = seq.index(s)
        site.append(j)
        sites[i] = site
    
    data = utils.load_data('EC_genes.txt')
    genes = list()
    for line in data.strip().split('\n'):
        g,i,j,d = line.strip().split()
        genes.append((g,int(i),int(j),d))

    for site in sites:
        print round(site[0],3)
        print site[1:]
        n = site[-1]
        for g in genes:
            i,j = g[1:3]
            if (i-22) <= n < j:
                print 'in'
                print g
            if abs(i-n) < 500:
                print 'near', abs(i-n),
                print g
        print

We do::
  
    > python script.py > final.txt
    
Here are the first three entries in ``final.txt``::

    22.125
    ['atatgtgattcatatcacatat', 4589511]
    near 168 ('tsr', 4589679, 4591334, 'cw')

    21.073
    ['ttatgtgatctaaatcactttt', 3387504]
    near 349 ('aaeX', 3387155, 3387358, 'ccw')
    near 37 ('aaeR', 3387541, 3388470, 'cw')

    20.779
    ['gattgtgattcgattcacattt', 3886363]
    near 94 ('tnaC', 3886457, 3886531, 'cw')
    near 389 ('tnaA', 3886752, 3888167, 'cw')

Rather than use a word processor, I check for sites with ``grep``.  I read the manual (``man grep``) to learn the correct switches for showing extra lines and also line numbers)::

    > grep lac final.txt -A 2 -B 3 -n
    731-
    732-13.645
    733-['atgagtgagctaactcacatta', 365617]
    734:near 34 ('lacI', 365651, 366733, 'ccw')
    735-
    736-13.603
    --
    1023-12.903
    1024-['taacgttactggtttcacattc', 366716]
    1025-in
    1026:('lacI', 365651, 366733, 'ccw')
    1027-near 94 ('mhpR', 366810, 367643, 'ccw')
    1028-

If we compare with the original definitions file ``crp.dat.txt``::

    >lac 1 (lacZ) 88->110
    taatgtgagttagctcactcat
    >lac 2 (lacZ) 16->38 
    aattgtgagcggataacaattt
    
These sequences don't seem to match very well.  What's going on?  The fundamental problem is that we searched for the pattern without worrying about the opposite strand.  In Schneider's work, they use both the forward and reverse complement versions of each site to build the matrix.

PMID `9396807 <http://www.ncbi.nlm.nih.gov/pubmed/9396807>`_

The first sequence that we found is the *reverse* of the first sequence in ``crp.dat.txt``.

The relevant entries in ``EC_genes.txt`` are::

    lacY   361149 362402 ccw
    lacZ   362454 365528 ccw
    lacI   365651 366733 ccw

The genes run ccw on the chromosome sequence.  So the last nt of *lacI* is 365651.  The index of the site is 365617, so it would run from 365617-365638.  This is the upstream site that controls *lacZ*.  The notation 88->110 indicates that it lies that distance upstream of *lacZ*, and this matches what we have exactly.  365528 + 110 = 365638.

The second site we found is not the site close to *lacZ*.

If we go back to ``script.py`` from the section ``Test run:  Crp``, we can paste in the forward and reverse sequences to check the scores.  The output for the sequence from ``crp.dat.txt`` is::

    aattgtgagcggataacaattt 8.945

The output for its reverse complement is::

    aaattgttatccgctcacaatt 0.995

Naturally, since we looked for the reverse complement it's lost in the noise.  And we filtered for ``f > 12``, so we wouldn't have found the site either way.



