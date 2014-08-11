.. _vregions:

################
Counting changes
################

In this section, I'd like to try to visualize the sequence diversity in 16S rRNA genes. To see the "V" regions clearly, it will be helpful to have an alignment in which these regions *can* align, that is, the sequences need to be closely enough related. The figure above shows the information content of the sequence set computed for a window sliding across the length of the gene. The troughs are V regions.

This project was originally described here

http://telliott99.blogspot.com/2011/03/16s-rrna-v-regions-continued.html

To get such a set of genes, I went to RDP (Browsers)

http://rdp.cme.msu.edu/

I browsed the taxonomic hierarchy to the order Enterobacteriales, then pressed the '+' button on the left of that row, suppressing my confusion at the fact that the sequences I've selected are now suddenly marked with a '-' symbol.  I go to download and select FASTA format and remove common gaps.  

I renamed the file to ``16S_align.txt``.  The E. coli strain they have in there is a weird one, so I checked it against the MG1655 *rrnB* gene with :ref:`muscle <muscle>`, and found no indels.

Most of the sequences start internally in the 16S gene, so that's where our counting will have to start as well.  The first nucleotide that's present is numbered __ by the standard nomenclature.  Here is the aligned version of *E. coli* X80725::

    >S000004313 Escherichia coli (T); ATCC 11775T; X80725
    ------------AGTTTGATCA-TGGCTCAGATTGAACGCTGGCGGCAGGCCT
        .    +    .    +    .
    
As we'll see in a minute, the first part that aligns well (not mostly opposite gaps) is the TGGCT which starts at bp 24 of the given alignment.  The first T in TGGCT corresponds to position 20 of MG1655 *rrnB*, so that is the numbering I've adopted.

Here is the first half of ``script.py``:

.. sourcecode:: python

    import utils
    data = utils.load_data('16S_align.txt')

    L = list()
    for e in data.strip().split('>')[1:]:
        title,seq = e.strip().split('\n',1)
        seq = seq.upper()
        seq = ''.join(seq.split())
        if 'X80725' in title:
            coli = seq
        L.append(seq)
    
    cL = list()
    for c in range(len(L[0])):
        if not coli[c] in 'ACGT':
            continue
        symbols = 'ACGT-o'
        D = dict(zip(symbols,[0]*6))
        for r in range(len(L)):
            nt = L[r][c]
            if not nt in D:
                D['o'] += 1
            else:
                D[nt] += 1
        cL.append(D)

.. sourcecode:: python

    def ordered(L):
        def f(t):  return int(t[1])
        L.sort(key=f,reverse=True)
        return ''.join([t[0] for t in L])

    def shannon(D):
        L = [D[k] for k in 'ACGT']
        S = sum(L)
        if S*1.0/sum(D.values()) < 0.6:
            return 'gap'
        for i in range(len(L)):
            if L[i] == 0:
                L[i] = 0.1
        fL = [n*1.0/S for n in L]
        hL = [utils.log2(f)*f for f in fL]
        H = -sum(hL)
        info = 2 - H
        return str(round(info,2))
    
    for i,D in enumerate(cL):
        print str(i+10).rjust(4), seq[i+13], '  ',
        print ordered(D.items()),
        print shannon(D)
    
And here is the output for the first 30::

    10 -    -AGTCo gap
    11 -    -GACoT gap
    12 -    -TGACo gap
    13 -    -TACGo gap
    14 -    -TACGo gap
    15 A    -GACoT gap
    16 T    -ACGoT gap
    17 C    -TACGo gap
    18 C    -CoAGT gap
    19 -    -CAoGT gap
    20 T    -TACGo gap
    21 G    -GACoT gap
    22 G    -GCAoT gap
    23 C    -CGAoT gap
    24 T    -TACGo gap
    25 C    -CAGoT gap
    26 A    -ACGoT gap
    27 G    -GACoT gap
    28 A    A-CGoT 1.97
    29 T    T-AoCG 1.91
    30 T    T-ACGo 1.97
    31 G    G-TACo 1.87
    32 A    A-GTCo 1.81
    33 A    A-CGoT 1.98
    34 C    C-AGoT 1.92
    35 G    G-oACT 1.98
    36 C    C-GAoT 1.93
    37 T    T-GACo 1.93
    38 G    G-ACoT 1.98
    39 G    G-ACoT 1.98

We save the whole thing to disk with a redirect::

    python script.py > counts.txt

