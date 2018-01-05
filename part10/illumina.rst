.. _illumina:

########
Illumina
########

**A next-gen project**

This project is a recapitulation of a very nice PNAS paper by Gawronski et al

PMID `19805314 <http://www.ncbi.nlm.nih.gov/pubmed/19805314>`_

http://telliott99.blogspot.com/2011/03/handling-large-sequence-sets.html

We are looking for mariner transposon hits (at 'TA') sequences.

The first thing we need is the sequence of the *Haemophilus influenzae* genome.  ``script.py``:

.. sourcecode:: python

    from cogent.db.ncbi import EFetch
    ef = EFetch(id='L42023')
    seq = ef.read().split('\n',1)[1].strip()
    seq = seq.replace('\n','')
    print '>Hinf'
    print seq

Run it as usual::

   python script.py > Hinf.txt

Now take a look:

>>> from utils import load_data
>>> data = load_data('Hinf.txt')
>>> seq = data.strip().split('\n',1)[1]
>>> len(seq)
1830138
>>> symbols = ''.join(set(seq))
>>> symbols
'ACGKMNSRTWY'
>>> for c in symbols:
...     if c in 'ACGT':
...         continue
...     print c, seq.count(c)
... 
K 14
M 11
N 46
S 12
R 10
W 11
Y 11

Kind of ugly, but this was the very first bacterial genome to be sequenced.

I got the data from the Supporting Information page at PNAS:

http://www.pnas.org/content/106/38/16422/suppl/DCSupplemental

Datasets 1, 2 and 3 saved as SD1.txt etc.  Big files!::

    > ls -al SD*
    -rwxrwxrwx@ 1 telliott  staff  44581229 Mar  1  2011 SD1.txt
    -rwxrwxrwx@ 1 telliott  staff  46351855 Mar  3  2011 SD2.txt
    -rwxrwxrwx@ 1 telliott  staff  28145163 Mar  3  2011 SD3.txt
    
SD1 and SD2 are independent reads of the library before selection.  SD3 is after selection in the murine lung.

I decided to take a look at Bowtie for doing alignments of short reads to a genome.

http://bowtie-bio.sourceforge.net/

I downloaded the source and it was the easiest build ever. Just ``cd`` into the project directory and do ``make``::

    > file ~/Software/bowtie-0.12.7/bowtie
    /Users/telliott/Software/bowtie-0.12.7/bowtie: Mach-O 64-bit executable x86_64

Remember to make ``sym`` links, as described in the section on Unix.

Before using it it's necessary to build an index for the reference genome::

    bowtie-build ~/Desktop/Hinf.txt ~/Desktop/Hinf-ref/Hinf

A quick test with a file containing the first 10,000 of the data entries::

    bowtie Hinf-ref/Hinf -f test.txt

The output looks like this::

    5859	+	Hinf	706009	\
    TAGTAATCCTTGTTTATGAGATAATCTCTCGCATCTTTTGTATTATAAATTAA\
    	IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII\
    		0	41:T>A,52:C>A
    5871	+	Hinf	844099	\
    TATTGATACATGATCTTCCTTATCAAGAAGAGGAGATTGGCATCACAGAGATT\
    	IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII\
    		0	50:T>A
    6135	-	Hinf	110649	\
    TTCTTTATCCGCTAAATCGCCTAAATCCAAATCTGCTTTTGTAATACTTTGTA\
    	IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII\
    		0	
    6407	+	Hinf	484018	\
    TATTAGATCCCGAGCAAAACACCACATTTAACGATCACTATTTAGAAGGGGAT\
    	IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII\
    		0	48:T>G

    # reads processed: 13783
    # reads with at least one reported alignment: 9545 (69.25%)
    # reads that failed to align: 4238 (30.75%)
    Reported 9545 alignments to 1 output stream(s)
    
(The ``\`` is to indicate that I've wrapped the line).

These sequences are all 53 nt in length.  The third hit shown is on the - strand.  The output reports hits in the Hinf sequence by index..

Let's just check the first one quickly:

>>> from utils import load_data
>>> from utils import rev_complement
>>> data = load_data('Hinf.txt')
>>> seq = data.strip().split('\n',1)[1]
>>> len(seq)
1830138
>>> seq.find('TAGTAATCCTTGTTTATGAGATAATCTCTCGCATCTTTT')
706009
>>> seq[706009:706020]
'TAGTAATCCTT'

If we use the index specified in the bowtie output for this + strand hit, Python gives us the correct output.  This is surprising to me, because of 0-based indexing.

For the - strand match it's more complicated. . .  What is given in the output is the + strand.  We try the sequence that bowtie gave us and hold our breath (hoping for no mismatches):

>>> seq.find('TTCTTTATCCGCTAAATCGCCTAAATCCAAATCTGCTTTTGTAATACTTTGTA')
110649

using numbering based on that index::

    TTCTTTATCCGCTAAATCGCCTAAATCCAAATCTGCTTTTGTAATACTTTGTA
     +    .    +    .    +    .    +    .    +    .    +
 
Since the nt reported for the match is xxxx49, we will try adding 52 to that value to get to the nucleotide *we* will report as the match:  xxx101

>>> i = 110649 + 52

Take a look:

>>> i = 110649 + 52
>>> i
110701
>>> seq[i-20:i]
'CTGCTTTTGTAATACTTTGT'
>>> seq[i]
'A'

Adding 52 has got us to just past where we need to be.  The reason is subtle.

We're looking for mariner transposon hits (at 'TA') sequences.  

The sequences that originate on the + strand will be reported on the + strand as aligned at the 'T' of the 'TA' dinucleotide

The sequences that originate on the - strand will be reported in terms of the + strand as aligned with the 'A' of the 'TA' dinucleotide.  But we want to call these the *same*.  Suppose we had 

AAAATAGGGG
TTTTATCCCC

If mariner inserts in one orientation, would expect TAGGGG;  at the same site in the other orientation we would get TATTTT.  Therefore, we will add 51 rather than 52 to the index for our - strand hits.

Run ``bowtie`` for real::

    > bowtie Hinf-ref/Hinf -f SD1.txt > BT1.txt
    Warning: Skipping read (6532258) because it is less than 4 characters long
    # reads processed: 708731
    # reads with at least one reported alignment: 563880 (79.56%)
    # reads that failed to align: 144851 (20.44%)
    Reported 563880 alignments to 1 output stream(s)
    > bowtie Hinf-ref/Hinf -f SD2.txt > BT2.txt
    Warning: Skipping read (5972319) because it is less than 4 characters long
    # reads processed: 736631
    # reads with at least one reported alignment: 558995 (75.89%)
    # reads that failed to align: 177636 (24.11%)
    Reported 558995 alignments to 1 output stream(s)
    > bowtie Hinf-ref/Hinf -f SD3.txt > BT3.txt
    # reads processed: 447370
    # reads with at least one reported alignment: 263170 (58.83%)
    # reads that failed to align: 184200 (41.17%)
    Reported 263170 alignments to 1 output stream(s)

Write a Python script to filter the data the way we like it (and remember to change to Python's 0-based indexing):

.. sourcecode:: python

    import sys
    import utils

    fn = sys.argv[1]
    data = utils.load_data(fn)
    data = data.strip().split('\n')

    pL = list()
    for line in data:
        L = line.split()
        i = int(L[3])
        if L[1] == '-':
            i += 51
        pL.append(i)

    pL.sort()
    count = 1
    current = pL[0]
    for i in range(1,len(pL)):
        next = pL[i]
        if current == next:
            count += 1
        else:
            print current, count
            count = 1
            current = next
    print current, count

Run it::

    > python script.py Hinf-ref/BT1.txt > FD1.txt
    > python script.py Hinf-ref/BT2.txt > FD2.txt
    > python script.py Hinf-ref/BT3.txt > FD3.txt
    
``FD`` is for 'filtered data'.
           
>>> from utils import load_data
>>> data = load_data('FD1.txt')
>>> L = data.strip().split('\n')
>>> len(L)
62574
>>> L = [int(e.split()[1]) for e in L]
>>> sum(L)
563880

That's a lot of insertions.  While we're doing the setup, I went and grabbed the genome record ``NC_000907``.  The genes were extracted as before (with the modification to ``location``), and they are in ``HI_genes.txt``.  We'll work through that in the next section.