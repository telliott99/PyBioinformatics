.. _change:

######
Change
######

The *change* problem is another famous problem.  I am not sure whether it is famous in computer science or it derives its fame from the book in which I encountered it:

http://mitpress.mit.edu/sicp/full-text/book/book.html

which is beloved in computer science (for the problem, see Ch. 1.2.1).  

The problem statement is to find all the ways to give change for a dollar (N = 100) using the standard U.S. coin set:  1, 5, 10, 25, 50.

For a theoretical discussion of approaches to solving this you could see the above text or you may find it in another book on algorithms.  It is in Jones and Pevzner:

http://www.amazon.com/gp/product/0262101068

I include it here because I think this is a great programming challenge for an intermediate Python coder.  One can verify by inspection whether the results are correct, and by watching the clock one can tell whether a solution is fast enough.

It turns out there are a number of ways to "solve" this problem that give correct results in a short time for N = 25, but at least some of them will not solve the N = 100 problem in a reasonable time.

(Notice that substitution.  It's very useful to try your programs out on 'toy' problems at first).

Here is my naive solution to the change problem.  The logic is easily understood.  The first half is some setup and a function to change the correct number of coins of a lower denomination into one of a higher denomination.  It handles the case of two dimes and a nickel specially.  For once, the code is heavily annotated.

.. sourcecode:: python

    # how many ways to change a dollar or whatever N equals?

    # substitute if possible
    # change n * coin 1 => coin 2;  c1 < c2
    def change(D,c1,c2):
        rD = dict()
        for k in D:  
            rD[k] = D[k]
        # 10 => 25 is special
        if c1 is 10 and c2 is 25:
            if rD[10] < 2 or rD[5] < 1:  
                return None
            else:
                rD[5] -= 1
                rD[10] -= 2
                rD[25] += 1        
        else:
            if not c1*rD[c1] >= c2:  
                return None
            rD[c1] = rD[c1] - c2/c1
            rD[c2] += 1
        return rD

A criticism of this code is that it's not generalizable to just any set of coins because we depend on the values of ``coins`` for what we do in ``change``.  Also, inside ``change`` we're using the 'global' variable ``coins``, and that's generally not thought to be a good thing.  The reason is that if some other function changes the value of ``coins`` behind your back the code could fail for reasons that might be hard to figure out.  In our case, the example is small enough we can be sure that won't happen.

The second half is a loop on ``while True`` that we ``break`` out of when there is no more work to do.  Each new arrangement of coins from the previous iteration through the loop is added to the results and then tested, for each appropriate pair of coins, whether we can do a ``change`` operation.  If at this step we generate something we haven't seen before, we save it for the next round through the loop.

.. sourcecode:: python

    def run(N):
        coins = [1,5,10,25,50]
        # each possible combination is a dict
        L = [ { 1:N,5:0,10:0,25:0,50:0 } ]
        # for each coin, try changing to higher denom
        # save results in L to explore further changes...
        # keep a temp copy so we can append within loop
        results = list()

        while True:
            temp = list()
            finished = True
            for D in L:  
                # we already checked, D is not yet in results
                results.append(D)
                # for each possible change given coins available
                for i in range(len(coins)-1):
                    for j in range(i,len(coins)):
                        # change if possible
                        rD = change(D,coins[i],coins[j])
                        #if we haven't seen this one yet
                        if rD and not (rD in results or rD in temp):
                            temp.append(rD)
                            # since there is a new one(s) do not quit
                            finished = False
            if finished:  break
            L = temp[:]
        return results

We ``run`` the whole thing from ``main``:

.. sourcecode:: python

    if __name__ == '__main__':
        N = 200
        results = run(N)
        print 'finished', str(len(results)).rjust(5)
        results.sort(reverse=True)
        for D in results[:3] + results[-3:]:  
            for k in sorted(D.keys()):
                print (str(k) + ':' + str(D[k])).rjust(5),
            print
        for D in results:
            assert sum([k*D[k] for k in D]) == N

Notice the ``assert`` on the last line.  It's easy to write, and may save us from embarrassment.

The output is::

    > python change.py
    finished   292
    1:100   5:0  10:0  25:0  50:0
     1:95   5:1  10:0  25:0  50:0
     1:90   5:2  10:0  25:0  50:0
      1:0   5:0  10:0  25:4  50:0
      1:0   5:0  10:0  25:2  50:1
      1:0   5:0  10:0  25:0  50:2

The running time is in the neighborhood of 1 second for N = 100.  And it's roughly 43 seconds for N = 300.  That doesn't bode well for N = 500!

A challenge would be to use the ``timeit`` mechanism to measure the dependence of time on N.
