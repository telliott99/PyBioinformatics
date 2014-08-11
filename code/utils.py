def mean(L):
    return sum(L)*1.0/len(L)

def rev_complement(s):
    import string
    tt = string.maketrans('ACGT','TGCA')
    s = string.translate(s,tt)
    return s[::-1]

def get_crp_site_counts(fn):
    rL = list()
    data = load_data(fn)
    data = data.strip().split('\n')
    # data is weird, no extra newline, multiple '>'
    L = [e for e in data if not e.startswith('>')]
    L = [e.lower() for e in L]   # Genbank lowercase
    assert len(set([len(e) for e in L])) == 1
    for c in range(len(L[0])):
        D = dict(zip(list('acgt'), [0]*4))
        # inner loop is rows, harvest counts
        for r in range(len(L)):
            D[L[r][c]] += 1
        rL.append(D)
    return rL
    
# for a single column
def single_col_score(D):
    cL = [D[k] for k in 'acgt']
    S = sum(cL)
    fL = [n*1.0/S for n in cL]   
    sL = list()
    # score is 2 + utils.log2(freq) - correction
    # ignore correction
    for f in fL:
        if f == 0:  
            f = 0.5/S
        sL.append(2 + log2(f))
    return sL

def log2(f):
    from math import log
    return log(f)*1.0/log(2)

def load_data(fn):
    FH = open(fn, 'r')
    data = FH.read()
    FH.close()
    return data

def makeCode():
    nt = 'TCAG'
    L = list(nt)
    codons = [n1+n2+n3 for n1 in L for n2 in L for n3 in L]
    aa = 'FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRR' +\
         'IIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG'
    return dict(zip(codons, list(aa)))

def makeReverseGC(GC=None):
    if not GC:
        GC = makeCode()
    D = dict()
    for codon in GC:
        aa = GC[codon]
        if aa in D:
            D[aa].append(codon)
        else:
            D[aa] = [codon]
    return D

def makeSyn():
    GC = makeCode()
    rGC = makeReverseGC(GC)
    D = dict()
    for codon in GC:
        syn = rGC[GC[codon]][:]
        syn.remove(codon)
        D[codon] = syn
    return D

def grid(nrow,ncol):
    import numpy as np
    '''
    Return a dictionary with (0..nrow, 0..col) as keys, 
    and multipliers for x,y values to make a grid as values
    e.g. with nrow = 5, multipliers are 0, 0.25, 0.5, 0.75, 1.0
    '''
    rL = np.linspace(0,1,nrow)
    cL = np.linspace(0,1,ncol)
    D = dict()
    for i in range(nrow):
        for j in range(ncol):
            D[i,j] = (rL[i],cL[j])
    return D

def make_word_count_dict(wL):
    wD = dict()
    for w in wL:
        w = w.lower()
        for m,n in zip(w[:-1],w[1:]):
            k = m+n
            if k in wD:
                wD[k] += 1
            else:
                wD[k] = 1
    return wD

def plot_word_count_dict(D,wD,lc,scale):
    import matplotlib.pyplot as plt
    for i,u in enumerate(lc):
        for j,v in enumerate(lc):
            x,y = D[(i,j)]
            try:
                n = wD[u+v]
            except KeyError:
                n = 1
            n = 10* scale(n)
            if n < 10:
                n = 25
                c = '0.7'
                e = 'w'
            elif u in 'aeiou' or v in 'aeiou':
                c = 'maroon'
                e = 'k'
            else:
                c = 'salmon'
                e = 'k'
            plt.scatter(x,y,
                edgecolor=e,s=n,c=c)

def make_gid_dict(genomefn,groupfn):
    data = load_data(genomefn)
    D = dict()
    for line in data.strip().split('\n'):
        first,rest = line.strip().split(' ',1)
        name = rest.split(',')[0]
        name = name.replace(' ','_')
        gid,rest = first.split('|')[1].split(':')
        i,j = rest.split('-')
        D[name] = [gid,i,j]

    data = load_data(groupfn)
    data = data.strip().split('\n\n')
    L = list()
    for i,group in enumerate(data):
        for line in group.strip().split('\n')[1:]:
            gid,name = line.strip().split()
            if name in D:
                D[name].insert(0,i)
            else:
                D[name] = [i,gid]
    return D

def run(cmd):
    import os, sys, subprocess
    p = subprocess.Popen(cmd, shell=True)
    sts = os.waitpid(p.pid, 0)
    pid,exitCode = sts
    print sts
    if exitCode:
        sys.exit(exitCode)

# from BioPython
class RequestLimiter:
    def __init__(self, delay):
        self.last_time = 0.0
        self.delay = delay
    def wait(self, delay=None):
        if delay is None:
            delay = self.delay
        how_long = self.last_time + delay - time.time()
        if how_long > 0:
            time.sleep(how_long)
        self.last_time = time.time()
