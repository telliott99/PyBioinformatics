.. _poker:

#####
Poker
#####

This is a somewhat more extensive simulation, of the card game Poker.

http://en.wikipedia.org/wiki/List_of_poker_hands

Here, the interest is in the logic of the code used to evaluate the value of a particular hand.  The format of each card is an integer from 1-13 (as a string) plus a two-character suit from 'SP','HT','CL','DI'.

.. sourcecode:: python

    import random,sys

    def count(H):
        D = dict()
        L = [c[0] for c in H]
        for n in L:
            try:  D[n] += 1
            except KeyError:  D[n] = 1
        return D

    def straight(H):
        # depends on no pairs or higher
        L = [int(c[0]) for c in H]
        L.sort()
        # ace high
        if L[0] == 1:
            if L == [1,10,11,12,13]:  
                return True
        else:  # we need else
            if L[-1] - L[0] == 4: return True
        return False

    def flush(H):
        L = [c[1] for c in H]
        return len(list(set(L))) == 1

The function ``count`` takes a 'Hand', which is just a list of tuples of value, suit.  It grabs the value information (c[0]), then makes a dictionary that holds the counts for each value in the original list.  The code shows an alternative way to set up a dictionary with a default value.

The other two functions test whether the Hand is a straight or a flush.  Notice the use of :ref:`set <set>` in ``flush``.  In fact, the code in ``count`` is kind of old-fashioned, and could be accomplished more simply by using ``set`` there as well.

In the middle segment, we do the evaluation.

.. sourcecode:: python

    def evaluate(H):
        D = count(H)
        v = D.values()
        n = len(D.values())      
        if n == 5:      s = '-'
        if n == 4:      s = 'two'
        if n == 3:
            if 3 in v:  s = 'three'
            else:       s = 'two twos'
        if n == 2:
            if 4 in v:  s = 'four'
            else:       s = 'full house'

        # don't test if has >= pair
        if s == '-' and straight(H): 
            s = 'straight'
        if flush(H):
            s += ' flush'
        return s
    
The final segment consists of code to set up and run the functions in the earlier parts.
    
.. sourcecode:: python

    def oneHand():
        random.shuffle(Deck)
        H = Deck[:5]
        pL = [format(s).rjust(4) for s in H]
        return ' '.join(pL),evaluate(H)

    def format(c):
        n,s = c
        D = {'1':'A','11':'J','12':'Q','13':'K'}
        if n in D:
            return D[n] + s
        else:
            return ''.join(c)

    def test(N=100):
        for i in range(N):
            result = oneHand()
            if not result[1] in ['-', 'two']:
                print ' : '.join(result)

    random.seed(7)
    N = [str(n) for n in range(1,14)]
    suits = ['SP','HT','CL','DI']
    Deck = [(n,s) for n in N for s in suits]
    test()

Output::

    > python poker.py
    10SP  ASP  KSP  JHT  QCL : straight
    10CL  2CL  2HT  2SP  9CL : three
     4DI  9HT  QHT  QDI  9CL : two twos
    10DI  3SP 10SP  JSP  3HT : two twos
     ACL  3DI  4DI  ASP  3HT : two twos
     3DI  KHT  KDI  6CL  6HT : two twos
    10SP  QDI  9CL  KCL  JSP : straight
     7HT  AHT  ASP  KCL  7CL : two twos
    10SP  2SP  6SP  9SP  7SP : - flush
     4SP 10DI 10HT  6SP  6DI : two twos
     QSP  2DI  6SP  2SP  6HT : two twos
     8SP  AHT  5CL  ACL  5SP : two twos
     8SP  3DI  5SP  8DI  5DI : two twos
     2DI  KSP  2CL  7DI  2SP : three

I did some more extensive runs with similar code here:

http://telliott99.blogspot.com/2009/07/python-for-simulations.html