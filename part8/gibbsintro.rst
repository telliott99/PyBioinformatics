.. _gibbsintro:

#####
Setup
#####

(Note:  this chapter is not finished yet.)

In :ref:`sitesintro`, we had a set of sequences known to be bound by the Crp protein, and the problem was to find new examples of the motif in a bacterial genome.  These would be targets for further biochemical or bioinformatic investigation.

Here, we consider a related problem.  We have a set of genes that is co-regulated under certain conditions, so we suspect that they all contain binding sites for the same regulatory DNA-binding protein nearby.  We wish to search regions for a common, but unknown, motif.

I discussed this problem in blog posts starting with

http://telliott99.blogspot.com/2009/06/motif-discovery.html

and I want to cover the same ground again here, but more briefly.  The general approach we will take is called the Gibbs sampler.

Here is the first bit of code.  It constructs a set of random sequences, then embeds a particular invariant site in each one.  (We'll advance to the more realistic case later).

One nice thing is that the background sequence is in lowercase.  This allows us to see quickly where the motif has been placed.  When we score alignments, we will treat 'A' and 'a', etc., the same.

All the code from this first part is saved in ``gibbs.py``.  We will import these functions later on.  The code is straightforward:

.. sourcecode:: python

    import random
    import utils
    nt = 'acgt'

    def init_gibbs(nseq,N,site,seed=None):
        kL = list()
        if seed:
            random.seed(seed)
        n = len(site)
        L = list()
        for i in range(nseq):
            seq = [random.choice(nt) for j in range(N)]
            k = random.randint(0,N-n)
            seq[k:k+n] = site
            kL.append(k)
            L.append(seq)
        return L, kL

    if __name__ == '__main__':
        N = 50
        nseq = 10
        site = 'GAATTC'
        npos = len(site)
        seed = 153
        seqL, kL = init_gibbs(nseq,N,site=site,seed=seed)
        for seq in seqL:
            print ''.join(seq)

The output consists of 10 random sequences, each 50 nt in length with an *EcoRI* site embedded within them.  The only thing tricky about the code is to remember that ``randint`` can return the upper sentinel of what looks like a range.  Hence, we use N-n, so that the largest possible value is 50 - 6 = 44.  Then we would set ``seq[44:50] = site``, which is at the very end of ``seq``::

    > python gibbs.py
    tacttggttttgcgttttcgggcactcctcggagggcgatGAATTCgccc
    accatgcggacgtGAATTCtacacgaggagagacgtatttagagaagaaa
    gaggcagctacggGAATTCcatcatggaggaagactccccaagggtaggg
    ttaacaacttttgtggtGAATTCagggctaagtctcttgaattaatttct
    cgcgaacgtcaccaataGAATTCttgtgtcaccgggctctcgaagagatt
    gcGAATTCgtagagctgctgggtcaaaggtcaggcttgagtaaagcaatg
    tttagatttaacctcaagGAATTCactttgggccactggaccagctatcc
    tgccaGAATTCgtcgccaagtaggcatccgagtgttaggtctcgtagcac
    gtgaagcaaagggctgaatggGAATTCatcttacttgttttatgccaaga
    gGAATTCgtcaatcgcgatgcgtattttcttaacccgagcatagggacta

In our code, we will align the sequences by sliding them with respect to each other, and then evaluating a short part of the alignment.  The data structure that holds the alignment is just a list of ints (``iL``, returned here from ``random_iList()``).

Suppose the first two values in ``iL`` are 10 and 25 and the length of the site is 6 (as it is here).  Then the part of the alignment for which we will evaluate a score includes seq1[10:16] and seq2[25:31].

Here is a print function as well as a function to return random ints in the proper range for a new ``iL``.

.. sourcecode:: python

    def print_alignment(seqL,iL,npos):
        for seq,i in zip(seqL,iL):
            print ''.join(seq[i:i+npos]), str(i).rjust(2), 
            print ''.join(seq)

    def random_iList(N,npos,nseq):
        # randint is inclusive of end of range
        f = random.randint
        return [f(0,N-npos) for i in range(nseq)]
        
We add these two lines to ``main()``:

.. sourcecode:: python

    iL = random_iList(N,npos,nseq)
    print_alignment(seqL,iL,npos)

Output::

    > python gibbs.py
    tttcgg 15 tacttggttttgcgttttcgggcactcctcggagggcgatGAATTCgccc
    atttag 36 accatgcggacgtGAATTCtacacgaggagagacgtatttagagaagaaa
    ccccaa 36 gaggcagctacggGAATTCcatcatggaggaagactccccaagggtaggg
    caactt  4 ttaacaacttttgtggtGAATTCagggctaagtctcttgaattaatttct
    ccgggc 31 cgcgaacgtcaccaataGAATTCttgtgtcaccgggctctcgaagagatt
    agcaat 43 gcGAATTCgtagagctgctgggtcaaaggtcaggcttgagtaaagcaatg
    aagGAA 15 tttagatttaacctcaagGAATTCactttgggccactggaccagctatcc
    ccaGAA  2 tgccaGAATTCgtcgccaagtaggcatccgagtgttaggtctcgtagcac
    ggctga 11 gtgaagcaaagggctgaatggGAATTCatcttacttgttttatgccaaga
    taaccc 30 gGAATTCgtcaatcgcgatgcgtattttcttaacccgagcatagggacta

The next step is to introduce a scoring method.

This is not the scoring method in the Lawrence *et al.* paper, but it's fine for a start.  A small dictionary is used to look up both 'A' and 'a', G' and 'g' and so on.

.. sourcecode:: python

    def score_column(L):
        D={'a':'A','c':'C','g':'G','t':'T'}
        cL = [L.count(x) + L.count(D[x]) for x in nt]
        S = sum(cL)
        fL = list()
        for n in cL:
            if n == 0:
                fL.append(0.05/S)
            else:
                fL.append(n*1.0/S)
        hL = [utils.log2(f)*f for f in fL]
        return 2 + sum(hL)

    def score_alignment(seqL,iL,npos):
        L = [list() for i in range(npos)]
        for seq,i in zip(seqL,iL):
            for j in range(npos):
                x = seq[i+j]
                L[j].append(x)
        return sum([score_column(cL) for cL in L])

    if __name__ == '__main__':
        N = 50
        nseq = 10
        site = 'GAATTC'
        npos = len(site)
        seed = 153
        seqL, kL = init_gibbs(nseq,N,site=site,seed=seed)

        print
        iL = random_iList(N,npos,nseq)
        current = score_alignment(seqL,iL,npos)
        print round(current,3)
        print_alignment(seqL,iL,npos)

Output::

    > python gibbs.py

    0.758
    tttcgg 15 tacttggttttgcgttttcgggcactcctcggagggcgatGAATTCgccc
    atttag 36 accatgcggacgtGAATTCtacacgaggagagacgtatttagagaagaaa
    ccccaa 36 gaggcagctacggGAATTCcatcatggaggaagactccccaagggtaggg
    caactt  4 ttaacaacttttgtggtGAATTCagggctaagtctcttgaattaatttct
    ccgggc 31 cgcgaacgtcaccaataGAATTCttgtgtcaccgggctctcgaagagatt
    agcaat 43 gcGAATTCgtagagctgctgggtcaaaggtcaggcttgagtaaagcaatg
    aagGAA 15 tttagatttaacctcaagGAATTCactttgggccactggaccagctatcc
    ccaGAA  2 tgccaGAATTCgtcgccaagtaggcatccgagtgttaggtctcgtagcac
    ggctga 11 gtgaagcaaagggctgaatggGAATTCatcttacttgttttatgccaaga
    taaccc 30 gGAATTCgtcaatcgcgatgcgtattttcttaacccgagcatagggacta
    
Our list of random indexes happened to include part of two motifs.  As we'll see the resulting score is not large.

The search space for our problem, the possible number of alignments, is the number of indexes (N - n = 44) raised to the power nseq (10).  That's a big number.  In this next section of code, we implement a brute-force method to search that space and find, to no surprise, that it works poorly.

This part imports the previous functions and is in a separate file ``script.py``.  Because we set the ``seed``, we'll get the same sequences as before.

.. sourcecode:: python

    import random, sys, time
    import gibbs as G

    N = 50
    nseq = 10
    site = 'GAATTC'
    npos = len(site)

    seed = 153
    #seed = None
    seqL,kL = G.init_gibbs(nseq,N,site=site,seed=seed)

    def get_best_of_N(seqL,iL,npos,nrounds):
        t = time.time()
        print nrounds, 'rounds'
        best = G.score_alignment(seqL,iL,npos)
        tL = iL
        for k in range(nrounds):
            iL = G.random_iList(N,npos,nseq)
            current = G.score_alignment(seqL,iL,npos)
            if current > best:
                best = current
                tL = iL
        print round(best,3)
        G.print_alignment(seqL,tL,npos)
        print round(time.time() - t,2), 'sec'
        print
        return tL

    tL = G.random_iList(N,npos,nseq)
    for nrounds in [1,1000,10000,100000]:
        tL = get_best_of_N(seqL,tL,npos,nrounds=nrounds)

    if seed == 153:
        best = G.score_alignment(seqL,kL,npos)
        print round(best,3)
        G.print_alignment(seqL,kL,npos)
        print

    print '%e' % ((N - npos)**nseq)
    
Output::

    > python script.py
    1 rounds
    1.292
    cgtttt 12 tacttggttttgcgttttcgggcactcctcggagggcgatGAATTCgccc
    agagaa 40 accatgcggacgtGAATTCtacacgaggagagacgtatttagagaagaaa
    gctacg  6 gaggcagctacggGAATTCcatcatggaggaagactccccaagggtaggg
    taacaa  1 ttaacaacttttgtggtGAATTCagggctaagtctcttgaattaatttct
    gtcacc 27 cgcgaacgtcaccaataGAATTCttgtgtcaccgggctctcgaagagatt
    gctgct 13 gcGAATTCgtagagctgctgggtcaaaggtcaggcttgagtaaagcaatg
    tcaagG 13 tttagatttaacctcaagGAATTCactttgggccactggaccagctatcc
    tctcgt 39 tgccaGAATTCgtcgccaagtaggcatccgagtgttaggtctcgtagcac
    ggGAAT 19 gtgaagcaaagggctgaatggGAATTCatcttacttgttttatgccaaga
    tcttaa 27 gGAATTCgtcaatcgcgatgcgtattttcttaacccgagcatagggacta
    0.0 sec

    1000 rounds
    3.142
    tggttt  4 tacttggttttgcgttttcgggcactcctcggagggcgatGAATTCgccc
    tGAATT 12 accatgcggacgtGAATTCtacacgaggagagacgtatttagagaagaaa
    ggtagg 43 gaggcagctacggGAATTCcatcatggaggaagactccccaagggtaggg
    gggcta 24 ttaacaacttttgtggtGAATTCagggctaagtctcttgaattaatttct
    gaacgt  3 cgcgaacgtcaccaataGAATTCttgtgtcaccgggctctcgaagagatt
    tgagta 36 gcGAATTCgtagagctgctgggtcaaaggtcaggcttgagtaaagcaatg
    taacct  8 tttagatttaacctcaagGAATTCactttgggccactggaccagctatcc
    TCgtcg  9 tgccaGAATTCgtcgccaagtaggcatccgagtgttaggtctcgtagcac
    tgaagc  1 gtgaagcaaagggctgaatggGAATTCatcttacttgttttatgccaaga
    gggact 43 gGAATTCgtcaatcgcgatgcgtattttcttaacccgagcatagggacta
    0.2 sec

    10000 rounds
    4.459
    gcactc 21 tacttggttttgcgttttcgggcactcctcggagggcgatGAATTCgccc
    ggacgt  7 accatgcggacgtGAATTCtacacgaggagagacgtatttagagaagaaa
    agactc 31 gaggcagctacggGAATTCcatcatggaggaagactccccaagggtaggg
    aatttc 43 ttaacaacttttgtggtGAATTCagggctaagtctcttgaattaatttct
    GAATTC 17 cgcgaacgtcaccaataGAATTCttgtgtcaccgggctctcgaagagatt
    aaaggt 24 gcGAATTCgtagagctgctgggtcaaaggtcaggcttgagtaaagcaatg
    tcaagG 13 tttagatttaacctcaagGAATTCactttgggccactggaccagctatcc
    GAATTC  5 tgccaGAATTCgtcgccaagtaggcatccgagtgttaggtctcgtagcac
    gGAATT 20 gtgaagcaaagggctgaatggGAATTCatcttacttgttttatgccaaga
    GAATTC  1 gGAATTCgtcaatcgcgatgcgtattttcttaacccgagcatagggacta
    2.03 sec

    100000 rounds
    4.571
    ATTCgc 42 tacttggttttgcgttttcgggcactcctcggagggcgatGAATTCgccc
    ATTCta 15 accatgcggacgtGAATTCtacacgaggagagacgtatttagagaagaaa
    ATTCca 15 gaggcagctacggGAATTCcatcatggaggaagactccccaagggtaggg
    AATTCa 18 ttaacaacttttgtggtGAATTCagggctaagtctcttgaattaatttct
    ataGAA 14 cgcgaacgtcaccaataGAATTCttgtgtcaccgggctctcgaagagatt
    ATTCgt  4 gcGAATTCgtagagctgctgggtcaaaggtcaggcttgagtaaagcaatg
    AATTCa 19 tttagatttaacctcaagGAATTCactttgggccactggaccagctatcc
    ggtctc 37 tgccaGAATTCgtcgccaagtaggcatccgagtgttaggtctcgtagcac
    AATTCa 22 gtgaagcaaagggctgaatggGAATTCatcttacttgttttatgccaaga
    tttctt 25 gGAATTCgtcaatcgcgatgcgtattttcttaacccgagcatagggacta
    20.19 sec

    11.312
    GAATTC 40 tacttggttttgcgttttcgggcactcctcggagggcgatGAATTCgccc
    GAATTC 13 accatgcggacgtGAATTCtacacgaggagagacgtatttagagaagaaa
    GAATTC 13 gaggcagctacggGAATTCcatcatggaggaagactccccaagggtaggg
    GAATTC 17 ttaacaacttttgtggtGAATTCagggctaagtctcttgaattaatttct
    GAATTC 17 cgcgaacgtcaccaataGAATTCttgtgtcaccgggctctcgaagagatt
    GAATTC  2 gcGAATTCgtagagctgctgggtcaaaggtcaggcttgagtaaagcaatg
    GAATTC 18 tttagatttaacctcaagGAATTCactttgggccactggaccagctatcc
    GAATTC  5 tgccaGAATTCgtcgccaagtaggcatccgagtgttaggtctcgtagcac
    GAATTC 21 gtgaagcaaagggctgaatggGAATTCatcttacttgttttatgccaaga
    GAATTC  1 gGAATTCgtcaatcgcgatgcgtattttcttaacccgagcatagggacta

    2.719736e+16

If you look carefully at the results, the problem is clear.  With 10,000 rounds of guessing, we happened to find 3 examples of the motif in the right 'frame'.  But because we don't use that knowledge, we haven't done much better with 100,000 rounds.  

The very last section of output used the known positions of the motifs (returned from ``init_gibbs()``, so we can calculate what the best possible score is.

The number of possible alignments is *much* larger than the space we've searched.  A brute-force approach has no hope of success.