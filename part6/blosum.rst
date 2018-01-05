.. _blosum:

######
BLOSUM
######

The extension of our previous example to a protein alignment is fairly straightforward.  We'll need to modify the score we assign for both matches and mismatches based on the values in a new dictionary ``blosumD``.

The code in the previous example is in a module called ``NW.py``.  We modify the ``score`` function slightly to accept a new argument:

.. sourcecode:: python

    def score(seq1,seq2,L,attrD,blosumD=None):

And then use that argument as follows:

.. sourcecode:: python

    m = seq1[r-1]
    n = seq2[c-1]
    # protein
    if blosumD:
        diag_score = diag[0] + blosumD[(m,n)]
    # else nt
    elif m == n:
        diag_score = diag[0] + attrD['MATCH']
    else:
        diag_score = diag[0] + attrD['MISMATCH']

If we passed in a dictionary, then we get the score from there.  Otherwise, we do as we did before.  Since we're going to use them in more than one place, we assign the sequence characters to local variables ``m`` and ``n``.

The BLOSUM data is in a file ``blosum50.txt``.  It looks like this::

    #  Matrix made by matblas from blosum50.iij
    #  * column uses minimum score
    #  BLOSUM Clustered Scoring Matrix in 1/3 Bit Units
    #  Blocks Database = /data/blocks_5.0/blocks.dat
    #  Cluster Percentage: >= 50
    #  Entropy =   0.4808, Expected =  -0.3573
       A  R  N  D  C  Q  E  G  H  I  L  K  M  F  P  S  T  W  Y  V  B  Z  X  *
    A  5 -2 -1 -2 -1 -1 -1  0 -2 -1 -2 -1 -1 -3 -1  1  0 -3 -2  0 -2 -1 -1 -5 
    R -2  7 -1 -2 -4  1  0 -3  0 -4 -3  3 -2 -3 -3 -1 -1 -3 -1 -3 -1  0 -1 -5 
    N -1 -1  7  2 -2  0  0  0  1 -3 -4  0 -2 -4 -2  1  0 -4 -2 -3  4  0 -1 -5 
    D -2 -2  2  8 -4  0  2 -1 -1 -4 -4 -1 -4 -5 -1  0 -1 -5 -3 -4  5  1 -1 -5 
    C -1 -4 -2 -4 13 -3 -3 -3 -3 -2 -2 -3 -2 -2 -4 -1 -1 -5 -3 -1 -3 -3 -2 -5 
    Q -1  1  0  0 -3  7  2 -2  1 -3 -2  2  0 -4 -1  0 -1 -1 -1 -3  0  4 -1 -5 
    E -1  0  0  2 -3  2  6 -3  0 -4 -3  1 -2 -3 -1 -1 -1 -3 -2 -3  1  5 -1 -5 
    G  0 -3  0 -1 -3 -2 -3  8 -2 -4 -4 -2 -3 -4 -2  0 -2 -3 -3 -4 -1 -2 -2 -5 
    H -2  0  1 -1 -3  1  0 -2 10 -4 -3  0 -1 -1 -2 -1 -2 -3  2 -4  0  0 -1 -5 
    I -1 -4 -3 -4 -2 -3 -4 -4 -4  5  2 -3  2  0 -3 -3 -1 -3 -1  4 -4 -3 -1 -5 
    L -2 -3 -4 -4 -2 -2 -3 -4 -3  2  5 -3  3  1 -4 -3 -1 -2 -1  1 -4 -3 -1 -5 
    K -1  3  0 -1 -3  2  1 -2  0 -3 -3  6 -2 -4 -1  0 -1 -3 -2 -3  0  1 -1 -5 
    M -1 -2 -2 -4 -2  0 -2 -3 -1  2  3 -2  7  0 -3 -2 -1 -1  0  1 -3 -1 -1 -5 
    F -3 -3 -4 -5 -2 -4 -3 -4 -1  0  1 -4  0  8 -4 -3 -2  1  4 -1 -4 -4 -2 -5 
    P -1 -3 -2 -1 -4 -1 -1 -2 -2 -3 -4 -1 -3 -4 10 -1 -1 -4 -3 -3 -2 -1 -2 -5 
    S  1 -1  1  0 -1  0 -1  0 -1 -3 -3  0 -2 -3 -1  5  2 -4 -2 -2  0  0 -1 -5 
    T  0 -1  0 -1 -1 -1 -1 -2 -2 -1 -1 -1 -1 -2 -1  2  5 -3 -2  0  0 -1  0 -5 
    W -3 -3 -4 -5 -5 -1 -3 -3 -3 -3 -2 -3 -1  1 -4 -4 -3 15  2 -3 -5 -2 -3 -5 
    Y -2 -1 -2 -3 -3 -1 -2 -3  2 -1 -1 -2  0  4 -3 -2 -2  2  8 -1 -3 -2 -1 -5 
    V  0 -3 -3 -4 -1 -3 -3 -4 -4  4  1 -3  1 -1 -3 -2  0 -3 -1  5 -4 -3 -1 -5 
    B -2 -1  4  5 -3  0  1 -1  0 -4 -4  0 -3 -4 -2  0  0 -5 -3 -4  5  2 -1 -5 
    Z -1  0  0  1 -3  4  5 -2  0 -3 -3  1 -1 -4 -1  0 -1 -2 -2 -3  2  5 -1 -5 
    X -1 -1 -1 -1 -2 -1 -1 -2 -1 -1 -1 -1 -1 -2 -2 -1  0 -3 -1 -1 -1 -1 -1 -5 
    * -5 -5 -5 -5 -5 -5 -5 -5 -5 -5 -5 -5 -5 -5 -5 -5 -5 -5 -5 -5 -5 -5 -5  1
    
We write a function to load and parse the data, and then save the function in ``blosum.py``:

.. sourcecode:: python

    import utils

    def init(fn=None):
        if not fn:
            fn = 'blosum50.txt'
        data = utils.load_data(fn)
        L = data.strip().split('\n')
        L = [e for e in L if not e.startswith('#')]
        aaL = L.pop(0).strip().split()
        D = dict()
        for line in L:
            line = line.strip().split()
            k1 = line.pop(0)
            line = [int(n) for n in line]
            for k2,v in zip(aaL,line):
                D[(k1,k2)] = int(v)
        return aaL,D
    
    if __name__ == '__main__':
        aaL, D = init()
        print ' '.join(aaL)
        for t in sorted(D.keys()):
            if sorted(t,reverse=True) == list(t):
                print t, str(D[t]).rjust(3)
            assert D[(t[1],t[0])] == D[t]

If we run that code as a script by doing ``python blosum.py``, we get::

    > python blosum.py
    A R N D C Q E G H I L K M F P S T W Y V B Z X *
    ('*', '*')   1
    ('A', '*')  -5
    ('A', 'A')   5
    ('B', '*')  -5
    . . .

with all the scores.  Our actual script (in ``script.py``) is simplicity itself:

.. sourcecode:: python

    import utils, blosum, NW

    aaL, D = blosum.init('blosum50.txt')
    seq1 = 'HEAGAWGHEE'
    seq2 = 'PAWHEAE'

    attrD = {'R':len(seq1) + 1,'C':len(seq2) + 1,
             'GAP':-6,'MATCH':5,'MISMATCH':-2}

    L = NW.init(**attrD)
    #NW.show(L)
    NW.score(seq1,seq2,L,attrD,blosumD=D)
    NW.show(L)
    pL1,pL2 = NW.trackback(seq1,seq2,L,attrD,v=False)
    pL1.reverse()
    pL2.reverse()
    NW.print_alignment(pL1,pL2)

Here is the output::

    > python script.py
       0 -   -6 L  -12 L  -18 L  -24 L  -30 L  -36 L  -42 L
      -6 U   -2 D   -8 D  -14 L   -8 D  -14 L  -20 L  -26 L
     -12 U   -7 D   -3 D   -9 L  -14 D   -2 D   -8 L  -14 D
     -18 U  -13 D   -2 D   -6 D  -11 D   -8 U    3 D   -3 L
     -24 U  -19 U   -8 U   -5 D   -8 D  -14 D   -3 U    0 D
     -30 U  -25 D  -14 D  -11 D   -7 D   -9 D   -9 D   -4 D
     -36 U  -31 U  -20 U    1 D   -5 L  -10 D  -12 D  -10 U
     -42 U  -37 U  -26 U   -5 U   -1 D   -7 L  -10 D  -15 D
     -48 U  -43 U  -32 U  -11 U    5 D   -1 D   -7 L  -10 D
     -54 U  -49 D  -38 U  -17 U   -1 U   11 D    5 L   -1 D
     -60 U  -55 D  -44 U  -23 U   -7 U    5 D   10 D   11 D
    HEAGAWGHE-E
    --P-AW-HEAE
    
That ought to be enough to get you started on your own version of the Needleman-Wunsch algorithm.  For more about the origin of scoring matrices and an analysis of Dayhoff's methods see

http://telliott99.blogspot.com/2008/08/pam-point-accepted-mutation.html
http://telliott99.blogspot.com/2008/08/pam-projecting-in-time.html




