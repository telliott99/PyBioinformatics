.. _bootstrap:

#########
Bootstrap
#########

The bootstrap is a statistical technique

http://telliott99.blogspot.com/2010/12/phylogenetic-bootstrap.html

used to measure the sufficiency of data to support a certain type of hypothesis.  In phylogenetics, suppose that we've used the columns of the sequences as an alignment.  We think the individual nucleotides in each column are related somehow and we've used them to compute a measure of relatedness, like a tree.

To assess the robustness of the measure we ask what happens if one or more columns drop out of the alignment.  

The dropping out is performed by the bootstrap, which *samples columns with replacement*.

Suppose we have an alignment like this::

    AGCAGG
    AACTCC
    AGTAGC
    TGCAGC

There are 6 columns in the alignment.  For the bootstrap test, we sample the columns as many times as there are columns in the original alignment.

So if the columns are numbered 0-6 we might do something like this:

>>> from random import randint
>>> iL = [randint(0,5) for i in range(6)]
>>> iL
[5, 1, 3, 0, 2, 5]

Now we just need to find a way to select the indexed columns.  In this example we'll pick column 5 twice, and we won't use column 4 at all.

The question for our Python code really is:  how do we collect the appropriate values from a list of rows, but by column instead of by row?

Suppose we have a set of sequences in a list:

>>> L = ['GAATTC','GGATCC','GGGCCC']
>>> print '\n'.join(L)
GAATTC
GGATCC
GGGCCC

One way to get the columns is to do it by hand:

>>> L = [list(sL) for sL in L]
>>> for c in range(len(L[0])):
...     sL = list()
...     for r in range(len(L)):
...         sL.append(L[r][c])
...     print sL
... 
['G', 'G', 'G']
['A', 'G', 'G']
['A', 'A', 'G']
['T', 'T', 'C']
['T', 'C', 'C']
['C', 'C', 'C']

Now that we have them, we can choose them according to the sequence in iL, but then we're faced with the problem of turning them back into rows.

This is a use case for the quick transposition method that we cited before in :ref:`here <matrix-columns>`.

For example:

>>> iL = [5, 1, 3, 0, 2, 5]
>>> iL
[5, 1, 3, 0, 2, 5]
>>> L = ['GAATTC','GGATCC','GGGCCC']
>>> print '\n'.join(L)
GAATTC
GGATCC
GGGCCC
>>> T = zip(*L)
>>> T = [T[i] for i in iL]
>>> L = zip(*T)
>>> L = [''.join(sL) for sL in L]
>>> print '\n'.join(L)
CATGAC
CGTGAC
CGCGGC

Can you see that we have the columns in the same order as the integers in iL?

**Jackknife**

The second technique, the jackknife, involves leaving 1 or more columns out of the analysis (similar to unfolding the various items in a Swiss Army Knife.  For example, we might decide to leave 2 columns out of the above analyis and repeatedly generate subsamples missing 2 columns in each.

From columns numbered 0 to 5::

    [0, 1, 2, 3, 4, 5] 

we might generate two different subsamples::

    [2, 3, 4, 5]
    [0, 1, 2, 4]
    
etc.

Both the bootstrap and the jackknife are in PyCogent.  See, for example,

http://pycogent.sourceforge.net/cookbook/standard_statistical_analyses.html?highlight=jackknife#the-jackknife