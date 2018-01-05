.. _sitesintro:

###########
Information
###########

Biological sequences are all about information.  To quote James Gleick:

    "As the smallest possible quantity of information, a bit represents the amount of uncertainty that exists in the flipping of a coin. The coin toss makes a choice between two possibilities of equal likelihood: in this case p1 and p2 each equal 1/2; the base 2 logarithm of 1/2 is -1; so H = 1 bit. A single character chosen randomly from an alphabet of 32 conveys more information: 5 bits, to be exact, because there are 32 possible messages and the logarithm of 32 is 5."
    
http://www.amazon.com/gp/product/0375423729

According to Shannon, information content is related to the number of symbols necessary to transmit a message.  For example, the message::

    DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD

might be given as::

    Dx50

So it has very little information.

But this example leads to something that's counterintuitive. Namely, the least compressible message is a completely random string of the allowed characters, and by this argument such a string has the highest possible information content.

What's surprising is that this (high information for random sequence) actually makes sense. If we happen to possess just the right one-time pad, such a message could be very informative.

**Sites for a DNA-binding protein**

We're going to explore a simple method that evaluates a sequence for the presence of sites for a DNA-binding protein.  The method was detailed in a paper from Larry Gold's lab by Tom Schneider and Gary Stormo.

http://www.ncbi.nlm.nih.gov/pubmed/3525846>

I've discussed this in some detail here:

http://telliott99.blogspot.com/search/label/DNA%20binding%20sites

An extensive collection of validated binding sites for various DNA-binding proteins of *E. coli* is at:

http://arep.med.harvard.edu/ecoli_matrices/

I downloaded the data for the Crp protein, which is a cAMP-dependent transcription factor.  It's in ``crp.dat.txt``.  The first function we'll need is 

.. sourcecode:: python

    def get_crp_site_counts(fn):
        rL = list()
        data = load_data(fn)
        data = data.strip().split('\n')
        # data is weird, no extra newline, multiple '>'
        L = [e for e in data if not e.startswith('>')]
        L = [e.lower() for e in L]   # Genbank lowercase
        assert len(set([len(e) for e in L])) == 1
        for c in range(len(L[0])):
            D = dict(zip(list('acgt'), [0]*4))
            # inner loop is rows, harvest counts
            for r in range(len(L)):
                D[L[r][c]] += 1
            rL.append(D)
        return rL

The title lines are funny, but we just throw them away.  I put in as ``assert`` test for the length of all the sites to be the same:

.. sourcecode:: python

    assert len(set([len(e) for e in L])) == 1

We construct a set of the int values for length.  If they're all the same, there should be only a single member of the set.

We have to be careful about the loops.  Here, the outer loop is over the columns, so the data will be for position 1, then 2, and so on.  We save it in a dictionary to guard against confusion later.  But eventually, we'll pass a single array of values to a C function, so we can't use dicts there.

The second function is

.. sourcecode:: python

    # for a single column
    def single_col_score(D):
        cL = [D[k] for k in 'acgt']
        S = sum(cL)
        fL = [n*1.0/S for n in cL]   
        sL = list()
        # score is 2 + utils.log2(freq) - correction
        # ignore correction
        for f in fL:
            if f == 0:  
                f = 0.5/S
            sL.append(2 + log2(f))
        return sL
    
Note:  log2 is defined in utils, so there's no import needed.

.. sourcecode:: python

    def log2(f):
        from math import log
        return log(f)*1.0/log(2)

This constructs a score according to an approach suggested by information theory.  There is supposed to be a correction the ensure that the average score is actually 0, but I left it out.  The correction is complicated to determine, and we're just going to rank the sites and take the highest-value ones.  We don't care about the actual scores.

One reason for that is the system is not very smart.  It does not take account of affinity of the DNA-binding protein, but treats all example sites as equal.

Although this paper from Schneider suggests these correlate:

PMID `17617646 <http://www.ncbi.nlm.nih.gov/pubmed/17617646>`_

The two functions above are put into ``utils.py`` as usual (after some testing).  Here is ``script.py``:

.. sourcecode:: python

    import utils

    def run(fn, v=False):
        cL = utils.get_crp_site_counts(fn)
        L = [utils.single_col_score(D) for D in cL]
        rL = list()
        for c,sL in zip(cL,L):
            rL.extend(sL)
            if v:  
                print c
            if v:  
                for item in sL:
                    print round(item,2),
                print
        return rL

    if __name__ == '__main__':
        fn = 'crp.dat.txt'
        rL = run(fn, v=True)
        for f in rL:
            print f

Here is the first part of the output.

.. sourcecode:: python

    > python script.py 
    {'a': 23, 'c': 1, 't': 21, 'g': 4}
    0.91 -3.61 -1.61 0.78
    {'a': 23, 'c': 2, 't': 18, 'g': 6}
    0.91 -2.61 -1.03 0.56
    {'a': 18, 'c': 4, 't': 18, 'g': 9}
    0.56 -1.61 -0.44 0.56
    {'a': 0, 'c': 8, 't': 39, 'g': 2}

We can check the math for the very first one:

>>> from math import log
>>> f = 23.0/49
>>> 2 + log(f)/log(2.0)
0.90885211194180471

with v = False, we do:

.. sourcecode:: python

    python script.py > scores.txt

The file ``scores.txt`` has::

    0.908852111942
    -3.61470984412
    -1.61470984412
    0.777607578664. . .