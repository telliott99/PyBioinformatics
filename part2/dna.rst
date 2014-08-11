.. _dna:

###
DNA
###

We covered a lot in the first chapter.  I think we can actually get some work done.

Let's grab a copy of the sequence of my favorite gene (*mfg*).

http://www.ncbi.nlm.nih.gov/nuccore/154102?report=fasta

Save it into a text file (``mfg.txt``) and then load it into memory

.. sourcecode:: python

    fn = 'mfg.txt'
    FH = open(fn, 'r')
    data = FH.read()
    FH.close()
    title, seq = data.strip().split('\n',1)
    i = title.find('hemA')
    print title[:i+4]

.. sourcecode:: python

    > python script.py 
    >gi|154102|gb|J04243.1|STYHEMAPRF S.typhimurium hemA gene, 

That's a long title line.  Too long for programs like ``clustal``.  We could think about modifying it by hand.  What do you think this would print?::

    print title.strip().split()[0].split('|')[1]

However, the DNA sequence is more interesting than the title.  Let's grab a chunk of it to play with.  (The sequence we received has newlines in it that will need to be removed for any serious work.  I'll show that after we do some simple things).

Add this to the previous code:

.. sourcecode:: python

    seq = seq[:40]
    print seq
    rseq = seq[::-1]
    print rseq

And we do:

.. sourcecode:: python

    > python script.py 
    GGATCCACTGCCGCAGGCTGTTTAACGGAATCGGCATCCC
    CCCTACGGCTAAGGCAATTTGTCGGACGCCGTCACCTAGG

We used the ``[::-1]`` trick for strings, though we might have turned the sequence into a list of characters instead and then used ``reverse``.

This is not really what we want.  We reversed the sequence, but we would normally want to work with its reverse complement.  One way to get that is to use the third fundamental Python data type, called a dictionary, but I'm putting that topic off for a moment.  Another way is to use a ``translation table``.  

.. sourcecode:: python

    import string

    fn = 'mfg.txt'
    FH = open(fn, 'r')
    data = FH.read()
    FH.close()
    title, seq = data.strip().split('\n',1)
    seq = seq[:40]

    def rev_complement(s):
        tt = string.maketrans('ACGT','TGCA')
        c = string.translate(s,tt)
        return c, c[::-1]

    c , rc = rev_complement(seq)
    print seq
    print c + '\n'
    print rc

At the command line:

.. sourcecode:: python

    > python script.py 
    GGATCCACTGCCGCAGGCTGTTTAACGGAATCGGCATCCC
    CCTAGGTGACGGCGTCCGACAAATTGCCTTAGCCGTAGGG

    GGGATGCCGATTCCGTTAAACAGCCTGCGGCAGTGGATCC

Here, we see a new Python keyword: ``import``.  The new methods that we've used, ``maketrans`` and ``translate``, are *defined* in the ``string`` module.  In order to get access to stuff defined there we have to do ``import string``.

A simple rationale for why we'd use ``import`` is that loading data is something we do all the time.  It's tiresome to type those three lines

.. sourcecode:: python

    FH = open(fn, 'r')
    data = FH.read()
    FH.close()

in every script.  So, let's turn it into a function.

.. sourcecode:: python

    def load_data(fn):
        FH = open(fn, 'r')
        data = FH.read()
        FH.close()
        return data

Save the function in a file called ``utils.py`` and leave it on the Desktop (or wherever you are running scripts from).  Then we can just do this in ``script.py``:

.. sourcecode:: python

    import utils
    data = utils.load_data('mfg.txt')
    print data [:54]

.. sourcecode:: python

    > python script.py 
    >gi|154102|gb|J04243.1|STYHEMAPRF S.typhimurium hemA gene,
    
It's not about saving lines, but clarity.

Don't be confused by the two appearances of ``>`` in this listing.  The one in the top line is the shell prompt, while the one in the second line is the symbol that marks a title line in FASTA format.

We might want to search the sequence for the presence of particular restriction sites.  Later, we'll see how to do this in a comprehensive way.  But let's just give the names of a few enzymes and the sites they recognize as a list of tuples:

.. sourcecode:: python

    import utils

    def map_one(seq,site):
        rL = list()
        i = -1
        while True:
            i = seq.find(site, i+1)
            if i == -1:
                break
            rL.append(i)
        return rL

    def map_all(seq,eL):
        rL = list()
        for enz,site in eL:
            L = map_one(seq,site)
            rL.append((enz,L))
        return rL

    data = utils.load_data('mfg.txt')
    seq = data.strip().split('\n', 1)[1]
    seq = ''.join(seq.split())

    enz_list = [ ('BamHI', 'GGATCC'),
                 ('EcoRI', 'GAATTC'),
                 ('HindIII', 'AAGCTT'),
                 ('MluI',  'ACGCGT'),
                 ('PstI',  'CTGCAG') ]

    result = map_all(seq, enz_list)
    for enz, L in result:
        if L:
            print enz.ljust(6), L
        else:
            print enz.ljust(6), 'not found'
    print len(seq)

And we do this:

.. sourcecode:: python

    > python script.py 
    BamHI  [0]
    EcoRI  [3335]
    HindIII not found
    MluI   [787, 2356]
    PstI   [493, 3284]
    3341

This example is more complicated than those we've seen so far, but if we break it down it will make sense.  First of all, we do the ``import`` as before, so we don't need to write the code to load the data.  In about the middle of the script, we split the sequence away from the title line.  This:

.. sourcecode:: python

    seq = ''.join(seq.split())

will remove any whitespace that might be in the sequence (as we said, it contains newlines originally).

We define the enzyme recognition sites as a list of tuples.  Going back to the top of the listing, the first function, ``map_one``, is called for each enzyme target site.  I hope you will recognize the logic from the example :ref:`while True <while-True>`.  It's exactly the same.

The next function, ``map_all``, is what we call from the main part of the code at the bottom.  In turn, it repetitively calls ``map_one`` for each enzyme.  Finally, we check the results to see if any are empty lists of indexes, and print an appropriate message for those.

**Errors**

In writing this code from scratch, I made a number of errors.  In the first version, I forgot to remove the newlines from the sequence.  Then, I misplaced the return and append statements in ``map_all``.  Try it for yourself and see.  What happens if the second to the last line has only four spaces in front?  What if the last line is indented eight spaces?  What does this do?

.. sourcecode:: python

    def map_all(seq,eL):
        rL = list()
        for enz,site in eL:
            L = map_one(seq,site)
            rL.append((enz,L))
        return rL

Debugging is important.  I'll just comment for now that my usual way of finding bugs is to insert ``print`` statements.  If things aren't working (or even if they seem like they are), and I think a variable should have a particular value at some place in the code, I just try printing it and see.  

This method is deprecated by the name 'caveman debugging' but it works for simple code and it's what I usually do.

As a last example for this first real bioinformatics section, let's examine one of the genes in this DNA sequence.  I happen to know

http://www.ncbi.nlm.nih.gov/nuccore/154102 

that the coordinates of the hemA gene are ``732..1988``.  Let's take a look:

.. sourcecode:: python

    import utils
    data = utils.load_data('mfg.txt')
    seq = data.strip().split('\n', 1)[1]
    seq = ''.join(seq.split())

    sub = seq[732:1988]   # error
    print sub[:6], sub[-6:]
    
Run it this way:

.. sourcecode:: python

    > python script.py 
    TGACCC GAGTAG

What happened?  We forgot to account for Genbank's standard use of indexes starting at 1.  So the 732 should have been 731, and we lost the first nt of the ATG.  On the other end, if we'd remembered Python's 0-based indexing, we might have used 1987.  But, this is a **half-open range**, so the last nt we want is at index 1987, and the index we should use for the sentry at the end of the sequence is 1988, because the sentry is not included in the range.  This happens to be exactly what we did.

By the way, I used a comment for the first time in this short code segment.  The ``# error`` is a comment.  The ``#`` means that any text following the symbol on the same line is ignored by Python.  It provides a useful way of saying something meaningful about the code so that other people who read it will know what you were thinking.

The ``range`` function has optional arguments, it can take as many as three:

range(start,stop,step)

So for example:

>>> range(10)
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> range(2,10)
[2, 3, 4, 5, 6, 7, 8, 9]
>>> range(2,10,4)
[2, 6]

For our DNA sequence, one way to break it up into codons is to generate a list of indexes with a step size of 3, like this:

>>> sub = seq[731:1988]
>>> R = range(0,len(sub),3)
>>> print R[:5]
[0, 3, 6, 9, 12]
>>> L = list()
>>> for i in R:
...     triplet = sub[i:i+3]
...     L.append(triplet)
... 
>>> print L[:3]
['ATG', 'ACC', 'CTT']
>>> for codon in ('ATG','TGG'):
...     print codon, L.count(codon)
... 
ATG 8
TGG 4

The HemA protein has 8 methionine and 4 tryptophan residues.  I'd like to find their positions.  We can't actually use ``find`` (a string method) because lists don't have that.

From the command line:

.. sourcecode:: python

    import utils

    data = utils.load_data('mfg.txt')
    seq = data.strip().split('\n', 1)[1]
    seq = ''.join(seq.split())

    sub = seq[731:1988]
    R = range(0,len(sub),3)
    L = list()
    for i in R:
        triplet = sub[i:i+3]
        L.append(triplet)
    
    M = 'ATG'
    print L.index(M)

.. sourcecode:: python

    > python script.py 
    0
    
Not what we were looking for.

Lists have do an ``index`` method but it only returns the first index found (and it's an error if the search term is not in the list).  I think the best way to solve this is to use a list comprehension.  That's for the next section.