.. _crptest:

####
Test
####

The next step is to do a test run with simulated data but a real site matrix.  The code is only slightly changed from the previous version.

.. sourcecode:: python

    import ctypes, os
    import utils

    pre = os.getcwd()
    mylib = ctypes.CDLL(pre + '/sites.dylib', ctypes.RTLD_GLOBAL)
                    
    dna = 'attcgtgatagctgtcgtaaagttttgttacctgcctctaactt'
    # scores---order = acgt;  site len is 2

    data = utils.load_data('scores.txt')
    data = data.strip().split()
    L = [float(n) for n in data]
 
    Floats = ctypes.c_double * len(L)
    ff = Floats(*L)
    n = int(len(L)/4)
    N = len(dna) - n + 1

    NFloats = ctypes.c_double * N
    result = [0.0] * N
    result = NFloats(*result)

    mylib.score(dna, ff, n, result)
    for i,f in enumerate(result):
        print dna[i:i+n], round(f,3)
    
Here is the output::

    > python script.py 
    attcgtgatagctgtcgtaaag 8.039
    ttcgtgatagctgtcgtaaagt -26.235
    tcgtgatagctgtcgtaaagtt -0.293
    cgtgatagctgtcgtaaagttt -10.616
    gtgatagctgtcgtaaagtttt -12.33
    tgatagctgtcgtaaagttttg -17.499
    gatagctgtcgtaaagttttgt -19.746
    atagctgtcgtaaagttttgtt -10.117
    tagctgtcgtaaagttttgtta -12.478
    agctgtcgtaaagttttgttac -9.601
    gctgtcgtaaagttttgttacc -19.434
    ctgtcgtaaagttttgttacct -20.609
    tgtcgtaaagttttgttacctg -5.151
    gtcgtaaagttttgttacctgc -14.741
    tcgtaaagttttgttacctgcc -15.811
    cgtaaagttttgttacctgcct -23.47
    gtaaagttttgttacctgcctc -27.593
    taaagttttgttacctgcctct -10.993
    aaagttttgttacctgcctcta -11.328
    aagttttgttacctgcctctaa -4.09
    agttttgttacctgcctctaac -3.494
    gttttgttacctgcctctaact -20.369
    ttttgttacctgcctctaactt 11.785

The test sequence was constructed by concatenating the first two sites in ``crp.dat.txt``.  As you can see, we get a high score for the first position, then slide our window along and get very low scores, then when we're in register for the second site, we get a high score again.  Looks good to me.