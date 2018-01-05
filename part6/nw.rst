.. _nw:

################
Needleman-Wunsch
################

The Needleman-Wunsch algorithm (PMID: 5420325), carries out a global alignment on two sequences. The method produces a global rather than a local alignment. It is guaranteed to be the best possible (highest scoring) alignment. It is not guaranteed to be biologically relevant.

Having worked through a simple example of dynamic programming, we can now apply the technique to the problem of aligning two sequences.  I have written extensively about this, so rather than repeat all the introductory material here, I'll just wait while you go read it.  

http://telliott99.blogspot.com/2009/08/alignment-needleman-wunsch.html

The wikipedia article (not their best):

http://en.wikipedia.org/wiki/Needleman–Wunsch_algorithm

Another good source:

http://www.ludwig.edu.au/course/lectures2005/Likic.pdf

In this version, we'll work with DNA sequences and not worry about scoring systems for 'similar' characters.  We just assign +5 for a match, -2 for a mismatch, and -6 for an insertion.  In our first attempt, we won't bother to allow the user to input sequences, but just hard-code them in the script.

The first part of the script is the setup.  The code is somewhat obscure, but you can see clearly what it does from the output::

      0 -   -6 L  -12 L  -18 L  -24 L  -30 L  -36 L
     -6 U    0 *    0 *    0 *    0 *    0 *    0 *
    -12 U    0 *    0 *    0 *    0 *    0 *    0 *
    -18 U    0 *    0 *    0 *    0 *    0 *    0 *
    -24 U    0 *    0 *    0 *    0 *    0 *    0 *
    -30 U    0 *    0 *    0 *    0 *    0 *    0 *
    -36 U    0 *    0 *    0 *    0 *    0 *    0 *
    -42 U    0 *    0 *    0 *    0 *    0 *    0 *
    -48 U    0 *    0 *    0 *    0 *    0 *    0 *

We construct a matrix of tuples of (score, path).  Later, we will overwrite these initial values in the table, except for the first row and column.  I just put them in at the beginning so that the appropriate element will already exist when we want to write there.

The second part of the script does the scoring.  Overall, we go by columns, and within each column by rows, retrieving the tuples from up, left and along the diagonal.  We calculate potential scores and take the path that gives the best one, breaking ties by choosing the diagonal.  If you look carefully you may notice a bug in the script for the situation where the diagonal score is less than the others, and the up and left scores are equal.

We can see the output::

      0 -   -6 L  -12 L  -18 L  -24 L  -30 L  -36 L
     -6 U    5 D   -1 D   -7 L  -13 L  -19 D  -25 L
    -12 U   -1 U    3 D   -3 D   -9 D  -15 D  -21 D
    -18 U   -7 U   -3 D    8 D    2 L   -4 L  -10 L
    -24 U  -13 D   -2 D    2 U    6 D    7 D    1 L
    -30 U  -19 U   -8 U    3 D    0 D    4 D    5 D
    -36 U  -25 U  -14 U   -3 U    1 D   -2 D    2 D
    -42 U  -31 D  -20 D   -9 U   -5 D    6 D    0 L
    -48 U  -37 U  -26 U  -15 U   -4 D    0 U   11 D

The third phase is the traceback or trackback.  This is a global alignment, so we start in the lower right-hand corner at (11,'D') and follow the 'pointers' back to the origin.  That path is given in the output from the the third phase::

    r 8 c 6 A A (11, 'D')
    r 7 c 5 T T (6, 'D')
    r 6 c 4 G A (1, 'D')
    r 5 c 3 C C (3, 'D')
    r 4 c 2 T T (-2, 'D')
    r 3 c 1 C T (-7, 'U')
    r 2 c 1 G T (-1, 'U')
    r 1 c 1 T T (5, 'D')
    r 0 c 0 A A (0, '-')

We accumulate the actual nucleotides along the way and then print the alignment::

    TGCTCGTA
    T--TCATA

Here is the script.  If you read through the listing and you already understand what we're supposed to be doing, I think the logic will be obvious.

.. sourcecode:: python

    def show(L):
        for sL in L:  
            for e in sL:
                print str(e[0]).rjust(4), e[1],
            print

    # list elements are tuples of (score, path)
    # seq1 down the side
    # seq2 across the top
    def init(**attrD):
        R = attrD['R']
        C = attrD['C']
        GAP = attrD['GAP']
        L = [[(0,'-')]]
        L[0].extend( [(GAP*c,'L') for c in range(1,C)])
        for r in range(1,R):
            L.append([(GAP*r,'U')])
            L[r].extend([(0,'*') for c in range(1,C)])
        return L

    def score(seq1,seq2,L,attrD,blosumD=None):
        R = attrD['R']
        C = attrD['C']
        for c in range(1,C):
            for r in range(1,R):
                diag = L[r-1][c-1]
                up = L[r-1][c]
                left = L[r][c-1]
            
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
                up_score = up[0] + attrD['GAP']
                left_score = left[0] + attrD['GAP']
    
                if diag_score >= max(up_score,left_score):
                    t = (diag_score,'D')
                elif up_score > max(diag_score,left_score):
                    t = (up_score,'U')
                elif left_score > max(diag_score,up_score):
                    t = (left_score,'L')
                else:
                    assert 0 == 1
                L[r][c] = t
        
    def trackback(seq1,seq2,L,attrD,v=False):
        r = attrD['R'] - 1
        c = attrD['C'] - 1
        pL1 = list()
        pL2 = list()
        while True:
            t = L[r][c]
            s1 = seq1[r-1]
            s2 = seq2[c-1]
            if v:
                print 'r', r, 'c', c, s1, s2, t

            if t[1] == 'D':
                pL1.append(s1)
                pL2.append(s2)
                r -= 1
                c -= 1
            elif t[1] == 'U':
                pL1.append(s1)
                pL2.append('-')
                r -= 1
            elif t[1] == 'L':
                pL1.append('-')
                pL2.append(s2)
                c -= 1
            else:
                assert t[1] == '-'
                break
        return pL1,pL2
    
    def print_alignment(pL1,pL2,N=50):
        R = range(0,len(pL1),N)
        for i in R:
            if i:  print
            print ''.join(pL1[i:i+N])
            print ''.join(pL2[i:i+N])

    if __name__ == '__main__':
        seq1 = 'TGCTCGTA'
        seq2 = 'TTCATA'
        attrD = {'R':len(seq1) + 1,'C':len(seq2) + 1,
                 'GAP':-6,'MATCH':5,'MISMATCH':-2}
        L = init(**attrD)
        show(L)
        score(seq1,seq2,L,attrD)
        show(L)
        pL1,pL2 = trackback(seq1,seq2,L,attrD,v=True)
        pL1.reverse()
        pL2.reverse()
        print_alignment(pL1,pL2)


We'll try a protein example in the next section.  There is also a more elaborate example on the blog.  I'm not sure I would recommend the (fairly complicated) code to you as exemplary, but it works.

http://telliott99.blogspot.com/search/label/alignments