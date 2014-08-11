.. _restriction:

#################
Restriction Sites
#################

A standard resource for restriction site information is at NEB:

http://rebase.neb.com/rebase/rebase.files.html

I downloaded the file of prototypes (#5) to ``proto.txt'``.  The part of the file that's of interest starts like this::

    	    TYPE II ENZYMES
    	    ---------------

    AarI                           CACCTGC (4/8)
    AatII                          GACGT^C
    AbsI                           CC^TCGAGG

I made a number of simplifying changes to the data.  Entries with ambiguous bases were skipped, even positions with only purine or only pyrimidine, which we'd normally want to keep.  I skipped entries containing something like '(4/8)' which have offset cut sites, and also all entries that were not exactly 6 nucleotides in length (6-cutters).  And I removed information about the position of cleavage.

Here is the function to parse this data into a dictionary:

.. sourcecode:: python

    def init_enz(fn):
        def filter(site):
            site = site.strip()
            if 'N' in site or '(' in site:
                return
            site = site.replace('^','')
            if len(site) != 6:
                return
            for c in site:
                if c not in 'ACGT':
                    return
            return site
        data = load_data(fn)
        data = data.split('TYPE I ENZYMES')[0].strip()
        data = data.strip().split('\n')
        while not 'TYPE II' in data[0]:
            data.pop(0)
        L = data[3:]
        D = dict()
        for line in L:
            enz,site = line.strip().split(' ',1)
            result = filter(site)
            if not result:
                continue
            D[enz.strip()] = result
        return D

We can use it like this:

>>> import utils
>>> eD = utils.init_enz('proto.txt')
>>> for k in sorted(eD.keys())[:5]:
...     print k.ljust(8), eD[k]
... 
AatII    GACGTC
AclI     AACGTT
AflII    CTTAAG
AgeI     ACCGGT
AhaIII   TTTAAA

Now, let's employ the restriction site data to accomplish something useful.  If we were frequently manipulating a gene (say to introduce site-directed mutations), we might want to break it up into smaller pieces of 500 nt or so, in order not to have to re-sequence the whole thing for each mutation introduced on a PCR fragment.  Often, the gene lacks suitably placed restriction sites.

We use the synonyms dictionary from ``utils.py`` discussed in the section on the Genetic Code.

Here is the code to look for synonomous changes to the coding sequence of ``mfg.txt`` that introduce restriction sites not present in the original:

.. sourcecode:: python

    import utils

    def init_seq():
        fn = 'mfg.txt'
        data = utils.load_data(fn)
        title,seq = data.strip().split('\n',1)
        return ''.join(seq.split())
    
    # includes nonsense codons
    synD = utils.makeSyn()
    seq = init_seq()[731-6:1988+3]
    eD = utils.init_enz('proto.txt')

    known = [e for e in eD if eD[e] in seq]

    # we have extra 6 nt before and after codon
    R = range(0,len(seq),3)[:-4]
    for i,j in enumerate(R):
        pre,post = seq[j:j+6],seq[j+9:j+15]
        codon = seq[j+6:j+9]
        for syn in synD[codon]:
            if syn in ['TAG','TGA','TAA']:
                continue
            target = ''.join([pre, syn, post])
            for enz,site in eD.items():
                if enz in known:
                    continue
                if site in target[1:-1]:
                    print '  ' + ' '.join([pre, codon, post])
                    print '*',
                    print ' '.join([pre, syn, post]), 
                    print i+2, enz.ljust(8), site
                    print

Here is a bit of the output::

      AGCGGT CTG GATTCA
    * AGCGGT CTA GATTCA 108 XbaI     TCTAGA

      GATTCA CTG GTGCTG
    * GATTCA CTA GTGCTG 111 SpeI     ACTAGT

At codon 108 we find that a change from 'CTG' to 'CTA' (both encoding Leu), will introduce a new XbaI site, and there are no XbaI sites in the original sequence.

**Generalized restriction mapping code**

(Note:  this section is a bit more complicated than I'd like for this early in the book, but it fits here.  So, feel free to skip ahead if it looks like too much.)

Here is another use of the same file of restriction enzyme recognition sites.  It's parsed a little differently, splitting on double newlines.  (Note:  the structure of the file is a little weird.  Some segments that look like they should be double newlines are actually ``'\n \n'`` so the split doesn't happen there).

In this example, we use all the enzymes, even those that recognize ambiguous sites.

Also, I use the ``re`` module to compile a 'regular expression' for each enzyme's site.  That should make it faster, but more important, it makes it easy to search for those ambiguous sites.  For an introduction to regular expressions, see:

http://docs.python.org/howto/regex.html

http://tldp.org/LDP/abs/html/x16947.html

.. sourcecode:: python

    import re
    import utils

    sample_dna = '''
     ATGACCCTTTTAGCGCTCGGTATTAACCATAAAACGGCACCTGTATCGCT
     GCGAGAACGCGTAACGTTTTCGCCGGACACGCTTGATCAGGCGCTGGACA
     GCCTGCTTGCGCAGCCAATGGTGCAGGGCGGGGTCGTGCTGTCAACCTGT
     AACCGTACAGAGCTGTATCTGAGCGTGGAAGAGCAGGATAACCTGCAAGA'''

    # downloaded from
    # http://rebase.neb.com/rebase/link_proto
    def load_data(fn = 'book/data/proto.txt'):
        data = utils.load_data(fn)
        L = data.strip().split('\n\n')
        return L[3].strip()  # type II enzymes only

    # parse data into names and sites
    def preprocess(data):
        L = data.strip().split('\n')
        names = list()
        sites = list()
        for e in L:
            n,s = e.split(' ',1)
            names.append(n)
            words = s.strip().split()
            if words[0][0] == '(':
                sites.append(words[1])
            else:
                sites.append(words[0])
        return names,sites

    # codes for degenerate positions
    # http://www.bioinformatics.org/sms/iupac.html 
    def get_pattern(s):
        D = { 'A':'A','C':'C','G':'G','T':'T',
              'R':'[AG]','Y':'[CT]','N':'.',
              'S':'[GC]','W':'[AT]','K':'[GT]',
              'M':'[AC]','B':'[CGT]','D':'[AGT]',
              'H':'[ACT]','V':'[ACG]' }
        rL = [D[c] for c in s]
        return ''.join(rL)

    # dictionary of pre-compiled regexps
    def make_dict(data):
        names,sites = preprocess(data)
        D = dict()
        for n,s in zip(names,sites):
            i = s.find('^')
            s = s.replace('^','')
            p = get_pattern(s)
            p = re.compile(p)
            rD = { 'name':n,'site':s,
                   'pattern':p,'i':i }
            D[n] = rD
        return D
    
    def search(dna,D,minlength=4,ignore_ambig=True):
        N = max([len(n) for n in D.keys()])
        M = max([len(D[n]['site']) for n in D])
        rL = list()
        for n in D:
            rD = D[n]
            n,p,s = rD['name'], rD['pattern'],rD['site']
            if len(s) < minlength:  
                continue
            if ignore_ambig and 'N' in s:
                continue
            m = p.search(dna)
            if m:
                i = m.start()
                j = i + len(rD['site'])
                e = [n.ljust(N),s.ljust(M)]
                e += [i,dna[i:j]]
                rL.append(e)
        def f(s):  return s[2]   # index of match
        return sorted(rL, key=f)

    def show(result):
        for line in result:
            # index i is an int, so convert to str
            line[2] = str(line[2]).rjust(4)
            print '  '.join(line)
        
    def run(v=True):
        dna = ''.join(sample_dna.split())
        data = load_data()
        D = make_dict(data)
        result = search(dna,D,minlength=6)
        if v:
            show(result)      
          
    if __name__ == '__main__':
        run()

Here's the output::

    > python script.py
    HaeII      RGCGCY             11  AGCGCT
    Eco47III   AGCGCT             11  AGCGCT
    TsoI       TARCCA             23  TAACCA
    HgiCI      GGYRCC             35  GGCACC
    AflIII     ACRYGT             56  ACGCGT
    MluI       ACGCGT             56  ACGCGT
    AclI       AACGTT             62  AACGTT
    BclI       TGATCA             83  TGATCA
    RdeGBIII   TGRYCA             83  TGATCA
    BspGI      CTGGAC             93  CTGGAC
    MstI       TGCGCA            107  TGCGCA
    BsgI       GTGCAG            120  GTGCAG
    HindII     GTYRAC            140  GTCAAC
    CchII      GGARGA            176  GGAAGA
    BspMI      ACCTGC            190  ACCTGC

