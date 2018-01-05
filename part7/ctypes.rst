.. _ctypes:

############
Using ctypes
############

The next thing to worry about is that Python isn't fast enough to do this unless you're willing to wait a while.  So I decided to write the actual scoring code in C.  It can do a genome in 5 or 10 seconds, so I haven't yet explored whether it can be made faster

.. sourcecode:: c

    #include <stdio.h>
    #include <string.h>

    void score(const char* dna, double p[], 
               int n, double result[]) {
        int i,j,k,N;
        double r; 
        N = strlen(dna)-n+1;
        for (i=0; i<N; i++){
            r = 0;
            for (j=0; j<n; j++){
                switch(dna[i+j]) {
                    case 'a': { k=0; break; }
                    case 'c': { k=1; break; }
                    case 'g': { k=2; break; }
                    case 't': { k=3; break; }
                }
                r += p[j*4 + k];
            }
            result[i] = r;
        }
    }
    
We'll pass into this function an array of scores (generated in the last section) with four values ('acgt') for each position in a site.  We do some magic from the command line to build a shared dynamic library in OS X::

    > clang -g -Wall -c sites.c
    > clang -dynamiclib -current_version 1.0  sites.o  -o sites.dylib
    > chmod +ux sites.dylib
    
And we make sure it's executable!

Now we use ``ctypes`` to use our C library function from Python.

http://docs.python.org/library/ctypes.html

http://telliott99.blogspot.com/search/label/ctypes

It's incredibly easy.  Here is a little test.

.. sourcecode:: python

    import ctypes, os
    pre = os.getcwd()
    mylib = ctypes.CDLL(pre + '/sites.dylib', ctypes.RTLD_GLOBAL)
                        
    dna = 'actgtcgactcgag'
    # scores---order = acgt;  site len is 2
    L = [ 0.567,  -1.603,  -0.2245, 0.3605,
         -0.1175, -0.4655, -0.5326, 0.6898 ]
     
    EightFloats = ctypes.c_double * len(L)
    ff = EightFloats(*L)
    n = int(len(L)/4)
    N = len(dna) - n + 1

    NFloats = ctypes.c_double * N
    result = [0.0] * N
    result = NFloats(*result)

    mylib.score(dna, ff, n, result)
    for i,f in enumerate(result):
        print dna[i:i+2], round(f,3)

Output::

    > python script.py
    ac 0.101
    ct -0.913
    tg -0.172
    gt 0.465
    tc -0.105
    cg -2.136
    ga -0.342
    ac 0.101
    ct -0.913
    tc -0.105
    cg -2.136
    ga -0.342
    ag 0.034