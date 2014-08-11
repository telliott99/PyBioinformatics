.. _genetic_code:

############
Genetic Code
############

**Fun with the genetic code**

We had this function before, and placed it into the file ``utils.py``:

.. sourcecode:: python

    def makeCode():
        nt = 'TCAG'
        L = list(nt)
        codons = [n1+n2+n3 for n1 in L for n2 in L for n3 in L]
        aa = 'FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRR' +\
             'IIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG'
        return dict(zip(codons, list(aa)))

Then we can do:

.. sourcecode:: python

    from utils import makeCode
    GC = makeCode()
    print GC['TAG']

.. sourcecode:: python

    > python script.py 
    *

The next question has to be, how about the reverse?  Can we construct a reverse dictionary that has the amino acids (one-letter code) as keys, where each value is a list of the corresponding synonymous codons.  Like this:

.. sourcecode:: python

    def makeReverseGC(GC):
        D = dict()
        for codon in GC:
            aa = GC[codon]
            if aa in D:
                D[aa].append(codon)
            else:
                D[aa] = [codon]
        return D

We'll save that function in ``utils.py`` as well.  Then:

.. sourcecode:: python

    from utils import *
    GC = makeCode()
    rGC = makeReverseGC(GC)
    print rGC['S']

.. sourcecode:: python

    > python script.py 
    ['AGC', 'AGT', 'TCT', 'TCG', 'TCC', 'TCA']

Now, let's construct a dictionary that associates each codon with its synonymous codons:

.. sourcecode:: python

    from utils import *

    def makeSyn(GC,rGC):
        D = dict()
        for codon in GC:
            syn = rGC[GC[codon]][:]
            syn.remove(codon)
            D[codon] = syn
        return D

    GC = makeCode()
    rGC = makeReverseGC(GC)
    SD = makeSyn(GC,rGC)
    print SD['AGC']

.. sourcecode:: python

    > python script.py 
    ['AGT', 'TCT', 'TCG', 'TCC', 'TCA']

We obtained the list of all synonyms for a given codon with ``rGC[GC[codon]]`` without ever giving an explicit label to the amino acid that is returned by ``GC[codon]``.  Second, we intend to modify the list of codons using the list function ``remove``, therefore we first make a copy of the list using ``[:]``.  If we forgot to do this, we'd have a mess.

Also, a style point.  Your average user may just want the synonyms dictionary---it's not convenient to first explicitly construct the other dictionaries if you don't need them.  We can fix that by having these functions call the other ones directly in ``utils``, and make that transparent to the user.  

And given that we could also bundle in our special ``cmp`` method from before, this begins to look like a good candidate for a class.  We'll get to classes in a bit.