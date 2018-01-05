.. _sorting:

#######
Sorting
#######

Since this chapter is about algorithms, I thought I would be remiss if I didn't show at least a little bit about sorting algorithms.  The first example is selection sort.  You can read more about it, and watch a cool animation.

http://en.wikipedia.org/wiki/Selection_sort

We start with an unsorted list of values obtained from ``get_data``, and begin at index i = 0.  We search through j > i to the end of the list to find the smallest value that is less than the value at 0.  (There may not be one).  At the end of the search, if we have found a smaller one, we swap the values at i and j.  Having the smallest value at i = 0, we increment to i = 1 and then repeat.  We can ignore the list indexes < i, because they are already in sorted order.

.. sourcecode:: python

    def get_data(N):
        L = range(N)
        random.shuffle(L)
        return L

    def selection_sort(iL):
        L = iL[:]
        for i in range(len(L)-1):
            j = i
            target = L[j]
            for k in range(i+1,len(L)):
                if L[k] < target:
                    j = k
                    target = L[k]
            if j != i:
                L[i],L[j] = L[j],L[i]
        return L

If you count the number of comparisons, you'll find that ``selection_sort`` always does N*(N-1)/2 comparisons.  (It's like the birthday problem!).  And if you count swaps, you'll find that it varies slightly but we always do nearly N swaps.  The comparisons dominate the running time, which is proportional to N**2.  In official language it is O(N**2), *order* of N**2.

The second example is ``merge_sort``.  This algorithm introduces the idea of **divide and conquer**.  When presented with a large list to sort, this approach simply divides the list in half and calls itself recursively on each half.

Confident that it has somehow solved the sorting problem, ``merge_sort`` now has two sorted sublists that need to be merged.  That part is easy.  We feed the two sublists to ``merge``.  Since they are in sorted order, we just examine the next value in each and ``pop`` the smaller one.

.. sourcecode:: python

    def merge(left,right,v=False):
        rL = list()
        if v:
            print 'merge: ', left, right
        while True:
            if left and right:
                if left[0] < right[0]:
                    rL.append(left.pop(0))
                else:
                    rL.append(right.pop(0))
                continue
            if left:
                rL.extend(left)
            elif right:
                rL.extend(right)
            break
        if v:
            print 'merge return: ', rL
        return rL
    
    def merge_sort(iL,v=False):
        if v:
            print 'merge_sort', iL
        if len(iL) == 1:
            if v:
                print 'merge_sort return: ', iL
            return iL
        n = len(iL)/2
        left = merge_sort(iL[:n],v=v)
        right = merge_sort(iL[n:],v=v)
        result = merge(left,right,v=v)
        if v:
            print 'merge_sort return: ', result
        return result

When ``merge_sort`` is called on a small list, with v = True (verbose), this is what it prints::

    > python ms.py
    merge_sort [3, 2, 4, 1, 0, 5]
    merge_sort [3, 2, 4]
    merge_sort [3]
    merge_sort return:  [3]
    merge_sort [2, 4]
    merge_sort [2]
    merge_sort return:  [2]
    merge_sort [4]
    merge_sort return:  [4]
    merge:  [2] [4]
    merge return:  [2, 4]
    merge_sort return:  [2, 4]
    merge:  [3] [2, 4]
    merge return:  [2, 3, 4]
    merge_sort return:  [2, 3, 4]
    merge_sort [1, 0, 5]
    merge_sort [1]
    merge_sort return:  [1]
    merge_sort [0, 5]
    merge_sort [0]
    merge_sort return:  [0]
    merge_sort [5]
    merge_sort return:  [5]
    merge:  [0] [5]
    merge return:  [0, 5]
    merge_sort return:  [0, 5]
    merge:  [1] [0, 5]
    merge return:  [0, 1, 5]
    merge_sort return:  [0, 1, 5]
    merge:  [2, 3, 4] [0, 1, 5]
    merge return:  [0, 1, 2, 3, 4, 5]
    merge_sort return:  [0, 1, 2, 3, 4, 5]

The third algorithm is ``qsort`` (quick_sort).  I modified the implementation from here:

http://code.activestate.com/recipes/66473-just-for-fun-quicksort-in-3-lines/

.. sourcecode:: python

    def qsort(L):
        if len(L) <= 1: return L
        left = [ lt for lt in L[1:] if lt < L[0] ]
        right = [ ge for ge in L[1:] if ge >= L[0] ]
        return qsort(left) + [L[0]] + qsort(right)

If ``merge_sort`` makes sense, then this will too.  Quicksort simply breaks up the problem into smaller ones.  We select the first value in the list as the pivot.  Then we filter the list into sublists containing all values smaller than the pivot, and all values larger.  We recursively call ``qsort`` on the sublists, and then reassemble the results.

The last part of the code is a test harness for the three functions.

.. sourcecode:: python

    def timed_runs():
        for N in [10,100,1000,10000,25000]:
            L = get_data(N)
            sL = sorted(L)
            t0 = time.time()
            result = selection_sort(L)
            assert result == sL
            t1= time.time()
            result = merge_sort(L)
            assert result == sL
            t2 = time.time()
            result = qsort(L)
            assert result == sL
            t3 = time.time()
            if N >= 1000:
                for i,j in zip((t0,t1,t2),(t1,t2,t3)):
                    print round(j-i,4),
                print 

    if __name__ == '__main__':
        L = get_data(10)
        merge_sort(L,v=True)
        timed_runs()

The output from ``timed_runs`` is::

    0.0471 0.0089 0.0048
    4.7635 0.1471 0.0585
    29.3557 0.634 0.1599

The columns are for ``selection_sort``, ``merge_sort`` and ``qsort`` in that order.  The rows are for 1000, 10000, and 25000 items.

As expected, ``selection_sort`` is O(N**2).  The ratio of the running times for 25000 v. 10000 values is roughly the square of the ratio of the number of values.

It is remarkable how much more efficient ``merge_sort`` and ``qsort`` are.  The former grows a bit faster than the latter.  According to Sedgewick ``merge_sort`` is O(N log N).

I am not quite sure why we don't blow the recursion limit for these guys.  I guess it's because they follow all the way down one side before working on the other, and each problem is divided (relatively evenly) in half.  The largest number of calls on the stack would then be log2(N).

>>> from math import log
>>> log(25000)/log(2)
14.609640474436812

