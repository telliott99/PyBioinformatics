.. _simulation:

##########
Simulation
##########

Python is just great for simulations.  

Simulations are used to illuminate what is may happen given certain conditions where the results are not completely determined because the process of interest is stochastic.

Simulations can even provide verification that results obtained analytically are actually correct.

The ``random`` module contains what we need.  Call the function ``random`` to get a random number between 0 and 1.  Note that the module and the function have the same name, so the call looks a bit redundant:  ``random.random()``.  This is actually a fairly common pattern in Python modules.

Other useful functions are ``choice`` and ``shuffle`` and ``randint``.

>>> import random
>>> random.random()
0.79197025812327393
>>> L = list('abcde')
>>> rL = [random.choice(L) for i in range(20)]
>>> ''.join(rL)
'bdebbbaaebdaddaaaedb'
>>> L
['a', 'b', 'c', 'd', 'e']
>>> random.shuffle(L)
>>> L
['a', 'b', 'c', 'e', 'd']
>>> random.randint(10,20)
12

For debugging purposes it's quite useful to have the same sequence of "random" numbers generated in each run of a program.  To obtain this, use ``seed``:

>>> import random
>>> random.seed(153)
>>> random.choice('abcde')
'e'
>>> random.random()
0.075667158047686311

Try again (that is, start Python fresh and run this code), and you will always get the same result.

.. _Counter-class:

**Counter**

The standard distribution is uniform.  Let's look at some results.  If you have Python 2.7 you can just import ``Counter`` from ``collections``, otherwise, see

http://code.activestate.com/recipes/576611-counter-class/

This version uses ``Counter.py`` downloaded and saved to the Desktop.  (The code is the same either way).

>>> import random
>>> import Counter
>>> R = range(5)
>>> L = [random.choice(R) for i in range(10000)]
>>> c = Counter.Counter(L)
>>> print c
Counter({3: 2047, 0: 2038, 4: 1992, 2: 1972, 1: 1951})

Other distributions are available:

>>> mu = 5
>>> sigma = 1
>>> L = [random.normalvariate(mu,sigma) for i in range(10000)]
>>> L.sort()
>>> L[9750]
6.9906452222243765

**Nothing in biology . . .**

Michael Yarus wrote a nice book 

http://www.amazon.com/gp/product/0674060717

(Life from an RNA world) in which he describes a simulation to generate Theodosius `Dobzhansky <http://en.wikipedia.org/wiki/Theodosius_Dobzhansky>`_'s famous `generalization <http://people.delphiforums.com/lordorman/permission.html>`_ starting from random letters.

We just carry out random mutagenesis, and keep the result if it's closer to our target.  This is a actually a pretty bad model for evolution, because the individual changes that are fixed should mostly have some selective value.  We might try (later) to generate words or something.  But let's take the simple case first.

.. sourcecode:: python

    import random, string
    alpha = string.letters + ' '

    def hamming(s1,s2):
        L = [1 for c1,c2 in zip(s1,s2) if c1 == c2]
        return sum(L)

    t = 'nothing in biology makes sense '
    t += 'except in the light of evolution'
    tL = list(t)
    sL = [random.choice(alpha) for i in range(len(tL))]
    print str(0).ljust(6), ''.join(sL)

    R = range(len(sL))
    h = hamming(sL,tL)
    i = 0

    while True:
        i += 1
        candidate = sL[:]
        j = random.choice(R)
        candidate[j] = random.choice(alpha)
        if hamming(candidate,tL) > h:
            sL = candidate
            h += 1
            print str(i).ljust(6), ''.join(sL)
        if sL == tL:
            break
            
We've seen everything here before.  ``t`` stands for target.  We use a list for the sequence we're changing so changes can be made in place before they are accepted.

Rather than keep track of the actual result of ``hamming(candidate,tL)``, we take advantage of the fact that any change will be +1.

Output:

.. sourcecode:: python

    > python script.py
    0      WoECCQymZoBcEMzwENiZSZzRfrEnzZEqjjLoaiKEGLBqDqHlGTKdUHlupjYiTaq
    12     WoECCQymZoBcEMzwENiZSZzRfrEnzZEqjjLoaiKnGLBqDqHlGTKdUHlupjYiTaq
    154    WoECCQymZoBcEozwENiZSZzRfrEnzZEqjjLoaiKnGLBqDqHlGTKdUHlupjYiTaq
    215    WoECCQymZoBcEozwENiZSZzRfrEnzZEqjjLoaiKnGtBqDqHlGTKdUHlupjYiTaq
    230    WoECCQymZoBbEozwENiZSZzRfrEnzZEqjjLoaiKnGtBqDqHlGTKdUHlupjYiTaq

    7199   Wothing in biology makes sensZ except in the light ofHeuolution
    9975   nothing in biology makes sensZ except in the light ofHeuolution
    10169  nothing in biology makes sensZ except in the light ofHevolution
    10514  nothing in biology makes sense except in the light ofHevolution
    10782  nothing in biology makes sense except in the light of evolution


Selection will shape you up quickly.  Kind of like `boot camp <http://en.wikipedia.org/wiki/Full_Metal_Jacket>`_.

**Mutagenesis**

Suppose we construct a DNA molecule with a frequency of exactly 25% of each nucleotide, but the sequence is random (see, it depends what you mean by 'random').  We ask about the frequency of 'A' in 800 random samples of 100 bases.

.. sourcecode:: python

    import random, Counter
    N = 200
    SZ = 100
    seq = list('ACGT'* N * SZ)
    random.shuffle(seq)
    R = range(0,len(seq),SZ)
    rL = [seq[i:i+SZ].count('A') for i in R]
    c = Counter.Counter(rL)
    for k in sorted(c.keys()):
        print k, 'x' * c[k]

    print sum(c.values())

.. sourcecode:: python

    > python script.py 
    13 x
    14 x
    15 xxxxxx
    16 xxxxxxxx
    17 xxxxxxxxxxxxxxxxxxxx
    18 xxxxxxxxxxxxxxxxxxxxxxxxx
    19 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    20 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    21 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    22 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    23 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    24 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    25 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    26 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    27 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    28 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    29 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    30 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    31 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    32 xxxxxxxxxxxxxxxxxxx
    33 xxxxxxxxxxx
    34 xxxxxxx
    35 xxx
    36 xxxx
    37 xxxxxx
    39 xxx
    800

For 800 normally distributed values the 97.5 percentile is 780.  There are 20 values of 34 or higher.  Suppose we have agreed in advance that we were only interested in 'A' and that if the count were non-random it could be higher or lower.  Upon observing a count of 33 'A' for a single sample, we should not be surprised.

Let's do some mutagenesis.  We start with a similar collection of 100000 randomly shuffled nucleotides.  We perform 10000 cycles in which we pick a position at random, and change that nucleotide at random to be any of the four bases:

.. sourcecode:: python

    import random
    N = 25000
    nt = 'ACGT'
    seq = list(nt * N)
    random.shuffle(seq)

    mseq = seq[:]
    R = range(len(mseq))
    for i in R:
        k = random.choice(R)
        mseq[k] = random.choice('acgt')

    def hamming(s1,s2):
        L = [1 for c1,c2 in zip(s1,s2) if not c1 == c2]
        return sum(L)

    print len(seq)
    print hamming(seq,mseq)

.. sourcecode:: python

    > python script.py 
    100000
    63214

In order to count the number of changes, we define the function ``hamming``, which uses a list comprehension, 'zip' and comparison for not ==.  All of these we've seen before.

This is should be a Poisson process (large number of trials, small probability of changing on any given trial, mean number of events per position = 1).

The distribution is:

.. image:: /figures/emmi.png
   :scale: 35 %

where m is the mean number of events, and i is the number of events for the class under consideration.  For example, here the mean is equal to 1, so the expected number of positions with no hits (i = 0) is 1/e

>>> import math
>>> 1.0/math.e
0.36787944117144233

I think that looks pretty close.  I hope you noticed that we cleverly made our changes to a different nucleotide alphabet, 'acgt'.  If we had used 'ACGT', about 1/4 of the changes would be invisible to us, and we would observe a mutation rate of around 47%.

**Central Limit Theorem**

We'll come back to simulation later, but before we go I want to give an example of how powerful it can be.  You probably know about the Central Limit Theorem.  Perhaps some sadistic statistics teacher showed you the proof, or even made you learn it.  We're going to confirm a prediction of this Theorem in a very simple way.

We construct a list of integers randomly distributed between 1 and 10 and take a sample of 5 a large number of times, and then just plot the results for the sum of the sample.

.. sourcecode:: python

    import random, Counter
    N = 10000
    R = range(1,6) * N
    random.shuffle(R)
    n = 5
    L = list()
    for i in range(0,len(R),n):
        L.append(sum(R[i:i+n]))
    c = Counter.Counter(L)
    for k in sorted(c.keys()):
        print k, 'x' * (c[k]/20)

.. sourcecode:: python

    > python script.py 
    5 
    6 
    7 xx
    8 xxxxx
    9 xxxxxxxxxxx
    10 xxxxxxxxxxxxxxxxxx
    11 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    12 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    13 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    14 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    15 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    16 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    17 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    18 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    19 xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    20 xxxxxxxxxxxxxxxxxxx
    21 xxxxxxxxxxx
    22 xxxxx
    23 xx
    24 
    25 
 
In squeezing down the distribution to print it, I have lost the tails, but you get the idea.  This is starting to look normal.
