.. _eutils:

######
EUtils
######

Here is a simple example that uses the 'history' mechanism of EUtils.  We construct a query to send for an 'esearch' that includes 'usehistory=y'.  We get back XML data that is parsed with ``ElementTree`` to recover the 'WebEnv' and 'QueryKey'.

In the second part, we go back to NCBI and do an 'efetch'.  I'll show the output first::

    > python script.py
    Count 2
    QueryKey 1
    WebEnv NCID_1_124792067_130.14.22.101_9001_1317251842_1898036850
    >gb|M60064.1|STYHEML:1-50 S.typhimurium glutamate 
    GATCTCTGCGCCGTAAACGCACAATTTGCTGAGCTAAAAAGGTGGAAGTG
    >gb|J04243.1|STYHEMAPRF:1-50 S.typhimurium hemA ge
    GGATCCACTGCCGCAGGCTGTTTAACGGAATCGGCATCCCGGTGAGTTTG

Here is ``script.py``:

.. sourcecode:: python

    import sys, urllib2
    import xml.etree.ElementTree as ET

    eutils = 'http://www.ncbi.nlm.nih.gov/entrez/eutils/'
    esearch = 'esearch.fcgi?'
    efetch = 'efetch.fcgi?'

    def part1():
        url = eutils + esearch + '&db=nucleotide'
        L = ['M60064', 'J04243']
        url += '&term=' + ','.join(L)
        url += '&retmax=0&usehistory=y'
        FH = urllib2.urlopen(url)

        # parse the WebEnv stuff:
        D = dict()
        terms = ['Count','WebEnv','QueryKey']
        tree = ET.parse(FH)
        for t in terms:
        	D[t] = tree.findtext(t)
        for k,v in D.items():
            print k,v
        return D

    def part2(D):
        # now, do the efetch
        f = eutils + efetch
        f += '&db=nucleotide'
        f += '&seq_start=1'
        f += '&seq_stop=50'
        f += '&rettype=fasta'
        f += '&retstart=0'
        f += '&query_key=' + D['QueryKey']
        f += '&WebEnv=' + D['WebEnv']	
        FH = urllib2.urlopen(f)
        data = FH.read()
        L = data.strip().split('\n\n')
        for item in L:
            title,seq = item.strip().split('\n')
            print title[:50]
            print seq

    D = part1()
    part2(D)