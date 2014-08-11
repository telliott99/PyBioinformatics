.. _colicrp:

########
Indexing
########

Now it's time to do the real thing.

Here is the overview for the sequenced genome of E. coli MG1655

http://www.ncbi.nlm.nih.gov/sites/genome/?term=115&dopt=Overview

Here is a link to the Genbank record

http://www.ncbi.nlm.nih.gov/nuccore/NC_000913

And here is a link to the FASTA-formatted sequence.

http://www.ncbi.nlm.nih.gov/nuccore/U00096

I grab the sequence as ``EC_genome.txt`` and the record as ``EC_genome.gb``.  But first I do a little massage on the sequence:

.. sourcecode:: python

    fn = 'sequence.fasta'
    import utils
    data = utils.load_data(fn)
    data = data.strip().split('\n',1)[1]
    seq = ''.join(data.split())
    seq = seq.lower()
    FH = open('EC_genome.txt','w')
    FH.write('>EC_genome\n')
    FH.write(seq + '\n')
    FH.close()

Now, it's a simple matter to go back to our ``script.py`` from :ref:`crptest`, and modify it to load the E. coli sequence:

.. sourcecode:: python

    import ctypes, os
    import utils

    pre = os.getcwd()
    mylib = ctypes.CDLL(pre + '/sites.dylib', ctypes.RTLD_GLOBAL)

    data = utils.load_data('EC_genome.txt')                
    dna = data.strip().split('\n',1)[1]
    print dna[:50]

    data = utils.load_data('scores.txt')
    data = data.strip().split()
    L = [float(n) for n in data]
 
    Floats = ctypes.c_double * len(L)
    ff = Floats(*L)
    n = int(len(L)/4)
    N = len(dna) - n + 1

    NFloats = ctypes.c_double * N
    result = [0.0] * N
    result = NFloats(*result)

    mylib.score(dna, ff, n, result)
    #print max(result)
    for i,f in enumerate(result):
        if f > 12:
            print dna[i:i+n], round(f,3)

Here is the the first part of the output::

    22.1246604608
    tattgtgaactatcgcaaagaa 14.331
    ttctgtgattggtatcacattt 19.156
    attggtgatccataaaacaata 12.441
    aagagtgacgtaaatcacactt 13.481
    aagtgtgacgccgtgcaaataa 15.022
    atgtgtgatcgtcatcacaatt 18.949
    tgatgtgaaaatcctcaaagat 12.43
    aattgtgcttattttagcattt 13.674
    ggatgtgaatcacttcacacaa 13.601
    atttctgacgttagtcatattt 12.343
    taatgtgaacatgatcaacgaa 13.398
    atatgtgatccagcttaaattt 18.4

We'll save this in ``EC_crp_results.txt``, minus the first line which lists the winning score.

