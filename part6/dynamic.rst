.. _dynamic:

###################
Dynamic Programming
###################

**Dynamic programming**

The method (and the name) 'dynamic programming' were introduced by Richard Bellman about 1953.

http://en.wikipedia.org/wiki/Richard_Bellman

Dynamic programming is not really about programming computers, but is a method for solving problems of a particular type.  He claimed that he called it dynamic to impress his boss, because "it's impossible to use the word dynamic in a pejorative sense".

Let's consider a classic example:  the 'best path' problem.  Start with a simple version:

.. image:: /figures/dyn.png
   :scale: 50 %

We have a pyramid or triangle of integers, arranged in n rows, where the length of each row = n + 1 (Python-style indexing).  The problem statement is to find the path from top to bottom that maximizes the sum of the items along the path.

Here there are 8 possible paths with these sums::

    3 + 7 + 2 + 8 = 20
    3 + 7 + 2 + 5 = 17
    3 + 7 + 5 + 5 = 20
    3 + 7 + 5 + 9 = 24

    3 + 5 + 5 + 5 = 18
    3 + 5 + 5 + 9 = 22
    3 + 5 + 4 + 9 = 21
    3 + 5 + 4 + 3 = 15

We find that the path with all values printed in red has the maximum score.  This problem is small enough to solve using enumeration, the method we used.  But if the problem is scaled up this can become impossible.  With n rows the number of paths is 2e(n-1).

Dynamic programming can help.  Consider a small segment of the two bottom rows of a large problem::

      63  66  55  68  89
    04  62  75  98  23  09

We analyze this as follows:  suppose that at some later time we were to find ourselves at the position in the (second to last) row with value 66.  What choice of path would maximize our score?  That's easy:  66 + 75 is larger than 66 + 62.  Take the 'right-hand' fork, and you'll have score = 141.

Now, add another row::

        44  89  26  35 
      63  66  55  68  89
    04  62  75  98  23  09

Suppose that we're at 89 in the first row.  From here, the choices are 66 and 55.  Should we choose 66?  The best value achievable from 66 is 66 + 75 = 141 and then 89 + 141 = 230.

But the best value achievable from 55 is 55 + 98 = 153 and 89 + 153 = 242.  So from 89 we should go right to 55 and then right again to 98, *even though* 66 > 55.

The way we will solve this problem in general is to have each position remember the maximum score that is achievable, and the path to get there.

That's a dynamic programming solution.

Suppose we have a list consisting of rows of integers.

.. sourcecode:: python

    L = [[3],[7,5],[2,5,4],[8,5,9,3]]

This code will solve the 'shortest path' problem.

.. sourcecode:: python

    def shortest(L):
        L.reverse()
        prev = [(m,[ ]) for m in L[0]]

        for row in L[1:]:
            for i,n in enumerate(row):
                left, right = prev[i],prev[i+1]
                x, pLx = left
                y, pLy = right
                if x > y:
                    n += x
                    pL = pLx[:] + ['L']
                else:
                    n += y
                    pL = pLy[:] + ['R']
                row[i] = (n,pL)
            prev = row

        s,pL = prev[0]
        return s,''.join(pL)

The approach taken is to transform each row in the data into a new list of values, where each item contains the best path from that point to the bottom plus the sum that path will yield.  In the initialization phase, we're at the bottom so the path is empty.::

    prev = [(m,[ ]) for m in L[0]]

For each successive row, using the known index i of the item we're processing, we retrieve the values of the two items below it.::

    left, right = prev[i],prev[i+1]

We evaluate which one is better and then construct a new sum by accumulation into n, and also save the direction into pL.  We modify row[i] directly.  With each pass through the loop, the items in the current row are modified in place.

Put that function into ``script.py`` along with::

    def run():
        L = [[3],[7,5],[2,5,4],[8,5,9,3]]
        print shortest(L)

    if __name__ == '__main__':
        run()

.. sourcecode:: python

    > python script.py
    (24, 'RRL')

Try something a bit bigger:

>>> import random
>>> import script
>>> L = list()
>>> R = range(100)
>>> for i in range(1000):
...     sL = list()
...     for j in range(i+1):
...          sL.append(random.choice(R))
...     L.append(sL)
... 
>>> L[:3]
[[34], [94, 29], [28, 44, 1]]
>>> script.shortest(L)
(74341, 'RRRLLLRRLLRRLRRLRRRRRRLLLLLLRLLLLLLLRRLLRLLLL
RRRLRLRLRRRRRRRLLLLRRLRLLLLLLRRRLRRRRRLLRLRRLRLLLLLLLR
. . . 
RLRLLLLLLRRLLRRLLLRRLLLRRLLLLRRRLLLLRLLLRRRLLLRLLRLLRR')

I broke up (and snipped) the output to fit.



