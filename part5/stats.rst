.. _stats:

##########
Statistics
##########

I don't want to go into too much detail about statistics, I'm just going to use one particular topic as a way of sharpening our Python skills.  If you really want to do statistical analysis in Python, look at the PyCogent Cookbook

http://pycogent.sourceforge.net/cookbook/index.html

or install and then explore SciPy

http://www.scipy.org/

or use RPy to call the R routines from Python.

**Chi-squared distribution**

You can read about this famous distribution here

http://en.wikipedia.org/wiki/Chi-squared_distribution

It comes up in combinations of random variables (e.g. the sum of the squares of n such variables is distributed with df = n, where df stands for *degrees of freedom*).

I thought I'd show a bit about the distribution based on the problem of 'Calculus grades' from Grinstead and Snell (pdf)

http://www.dartmouth.edu/~chance/teaching_aids/books_articles/probability_book/book.html

========  ========  ========  =========
Grade     Female    Male      Total
========  ========  ========  =========
A         37        56        93
B         63        60        123
C         47        43        90
F         5         8         13
Total     152       167       319
========  ========  ========  =========

The question to be investigated is whether the number of A's and B's and so on is distributed as expected under the hypothesis that the fraction awarded to male v. female students is randomly distributed (uniform random, that is), or whether there might be some systematic bias.

If we wanted to simulate this in Python, we would just put 167 copies of 'M' and 152 copies of 'F' in a list and then do ``random.shuffle`` on it.  After that, we'd assign the first 93 'M'/'F' symbols as corresponding to 'A' grades, and the next 123 as 'B', and so on.

Note that the total number of grades in different categories is not variable in the problem, nor is the number of male and female students.

Here, there are 8 relevant entries in the table, but only three *degrees of freedom*.  Once we've decided the fraction of A's, B's and C's awarded to females (or to males, for any 3 out of 4 of the grade categories), the rest of the table can be filled using simple arithmetic.

We can easily calculate the expected values for all the grades based on the numbers of different sexes:

.. sourcecode:: python

    F = 152;  M = 167
    N = M + F
    f = F*1.0/N;  m = M*1.0/N

    grades = [93,123,90,13]
    # expected values:
    EF = [f*g for g in grades]
    EM = [m*g for g in grades]

    for x,y in zip(EF,EM):
        print round(x,2),round(y,2)

Output::

    > python script.py
    44.3 48.7
    58.6 64.4
    42.9 47.1
    6.2 6.8

========  ========  ========  =========
Grade     Female    Male      Total
========  ========  ========  =========
A         44.3      48.7      93
B         58.6      64.4      123
C         42.9      47.1      90
F         6.2       6.8       13
Total     152       167       319
========  ========  ========  =========

Each entry is just the fraction of the total that is female or male times the number of individuals receiving that grade.

Now, for each item, we calculate ``(O-E)**2/E``, where ``O`` is the observed value and ``E`` is the expected value, based on the assumption of independence. We sum that result over all items to obtain the statistic. According to theory, this has a chi-squared distribution with degrees of freedom df = 3.

.. sourcecode:: python

    def chisq(OF,OM):
        result = list()
        for o,g in zip(OF,grades):
            e = f*g
            result.append( (o-e)**2/e )
        for o,g in zip(OM,grades):
            e = m*g
            result.append( (o-e)**2/e )
        return result

    OF = [37,63,47,5]
    OM = [56,60,43,8]
    result = chisq(OF,OM)
    for value in result:
        print round(value,2)
    print sum(result)

The repetition in the code above could be eliminated, but it would make it a bit harder to understand, since we vary both the list of values and the multiplier.  Simple is good, if it's possible.

Output::

    1.21
    0.33
    0.4
    0.23
    1.1
    0.3
    0.36
    0.21
    4.1287764639

The purpose of printing out the individual values is to double-check the math.

>>> (37-44.3)**2/44.3
1.2029345372460487

The total chi-squared statistic matches what I calculated previously:

http://telliott99.blogspot.com/2009/08/grade-disparity-chi-squared-analysis.html

and what is given in the book.  All that remains is to look up the chi-squared distribution for df = 3 in wikipedia:

http://en.wikipedia.org/wiki/Chi-squared_distribution

or just use PyCogent if it's installed:

>>> from cogent.maths.stats import chisqprob
>>> chisqprob(4.13,3)
0.24776432555405664

About 1/4 of the  distribution has a statistic more extreme (higher) than the one we calculated.  Also:

>>> from cogent.maths.stats.distribution import chdtri
>>> chdtri(3,0.05)
7.8147279032511783

The 95th percentile is at 7.81.

Since our result is not greater than 7.81, the observed deviation from the null hypothesis is *not* significant.  (Which is not to say that there is no systematic bias, just that we couldn't detect any by this test).

If *all* we have is ``numpy``, that's no problem:

>>> from numpy import random
>>> L = random.chisquare(3,10000)
>>> L.sort()
>>> L[9500]
7.8792912437813047
>>> import bisect
>>> bisect.bisect_left(L,4.13)
7565

There is a slight deviation, due to the fact that this is a random sample so it doesn't follow the distribution exactly.

``chisquare`` draws ``N=10000`` samples from the distribution with ``df=3``.  ``bisect_left`` takes a sorted array and finds the insertion point for the argument ``x`` that keeps the array in sorted order.

Probably the simplest example of the chi-squared distribution is of rolling dice. If an n-sided die is rolled many times, then the distribution of the counts for each of the n-sides should take on a chi-squared distribution (with df = n-1). 

I simulated that in Python and posted it here:

http://telliott99.blogspot.com/2010/04/chi-squared-revisited.html

Here is the graphic for reference:

.. image:: /figures/dice.png
   :scale: 50 %

The dotted red line is the predicted distribution (based on the gamma distribution).  It looks as we expect.

It's not hard to simulate the grades problem (with random assignment of the fraction of grades), and show that we get the predicted result.  That is, to show that the distribution of the statistic follows the chi-squared distribution.

I've often found that 're-inventing the wheel' in Python solidifies my understanding of how a particular technique works.  One of my favorite example is ANOVA, which I posted about here

http://telliott99.blogspot.com/2011/05/intro-to-anova.html