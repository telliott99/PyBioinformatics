.. _markup:

###
XML
###

XML is for computers to read, not people.  I went to PubMed and got a page for the article with this id:  `20853543 <http://www.ncbi.nlm.nih.gov/pubmed?term=20853543>`_.  Then I chose to save the results to a file as XML.  The file I got is called ``pubmed_result.xml``.  I'd like to parse this file.  Here is a rather long script that will do it.

.. sourcecode:: python

    import xml.etree.ElementTree as ET

    def parseArticle(article):
        D = dict()
        D['pmid'] = article.findtext(
            'MedlineCitation/PMID')
        journalinfo = article.find(
            'MedlineCitation/MedlineJournalInfo')
        D['journal'] = journalinfo.findtext('MedlineTA')
        a = article.find(
            'MedlineCitation/Article')
        D['volume'] = a.findtext(
            'Journal/JournalIssue/Volume')
        D['year'] = a.findtext(
            'Journal/JournalIssue/PubDate/Year')
        D['month'] = a.findtext(
            'Journal/JournalIssue/PubDate/Month')
        D['issue'] = a.findtext(
            'Journal/JournalIssue/Issue')
        D['title'] = a.findtext(
            'ArticleTitle')
        D['pages'] = a.findtext(
            'Pagination/MedlinePgn')
        D['abstract'] = a.findtext(
            'Abstract/AbstractText')
        authorList = list()
        authors = article.find(
            'MedlineCitation/Article/AuthorList')
        for author in authors:
            last = author.findtext('LastName')
            first = author.findtext('Initials')
            authorList.append((last, first))
        D['authorList'] = authorList
        return D

    def show(D):
        for k in ['title','authorList','journal',
                  'year','volume','pages',
                  'pmid','abstract']:
            if k == 'abstract':
                print k.ljust(15),
                abstract = D[k]
                if abstract:
                    print D[k][:40]
                else:
                    print
            elif k == 'authorList':
                L = [e[0] + ' ' + e[1] for e in D[k]]
                print k.ljust(15),
                for name in L[:-1]: 
                    print name + ', ',
                print L[-1]
            else:
                print k.ljust(15), D[k]
        print

    t = ET.parse('pubmed_result.xml')
    L = t.getroot().getchildren()
    for item in L:
        D = parseArticle(item)
        show(D)

.. sourcecode:: python

    > python script.py
    title           E. Peter Geiduschek.
    authorList      Geiduschek EP
    journal         Curr Biol
    year            2010
    volume          20
    pages           R694-5
    pmid            20853543
    abstract        Peter Geiduschek was an undergraduate Chem

I've posted more about this particular topic

http://telliott99.blogspot.com/2008/05/parsing-pubmed-with-elementtree.html

with a bunch of other stuff about XML here

http://telliott99.blogspot.com/search/label/XML

In the same way, the following code shows how to parse XML output from BLAST.

I started with the file containing sequences that we constructed in Starting with Phylogenetics called ``seqs.mod.txt``.  I renamed it to ``db.txt`` and placed it on the Desktop.  I format the database with::

    formatdb -i db.txt -p F
    
I copied out the first FASTA-formatted sequence into a file ``seq.txt`` and put that on the Desktop.  Then I run::

    blastall -p blastn -i seq.txt -o \
      blast.xml -d ~/Desktop/db.txt -m 7

After that, I put the following code into ``script.py``:

.. sourcecode:: python

    import xml.etree.ElementTree as ET

    def parseBLASTIteration(iteration, howmany=3):
        hitL = list()
        for hit in iteration.findall('Iteration_hits/Hit')[:howmany]:
            hitD = dict()
            for k in ['Hit_id','Hit_def','Hit_accession']:
                hitD[k] = hit.findtext(k)
            hitD['hsps'] = []
        
            for hsp in hit.findall('Hit_hsps'):
                hspD = dict()
                hspD['score'] =    hsp.findtext('Hsp/Hsp_score')           
                hspD['evalue'] =   hsp.findtext('Hsp/Hsp_evalue')          
                hspD['identity'] = hsp.findtext('Hsp/Hsp_identity')        
                hspD['gaps'] =     hsp.findtext('Hsp/Hsp_gaps')        
                hspD['length'] =   hsp.findtext('Hsp/Hsp_align-len')           
                hspD['query'] =    hsp.findtext('Hsp/Hsp_qseq')        
                hspD['midline'] =  hsp.findtext('Hsp/Hsp_midline')         
                hspD['hitseq'] =   hsp.findtext('Hsp/Hsp_hseq')
        
                identity = int(hspD['identity'])
                length = int(hspD['length'])
                try:
                    hspD['%identity'] = identity*100.0/length
                except ZeroDivisionError:
                    hspD['%identity'] = 'error'
                hitD['hsps'].append(hspD)
            
            hitL.append(hitD)
        return hitL
    
    def parseSingleIteration(tree,howmany=3):
        iteration = tree.find('BlastOutput_iterations/Iteration')
        hitL = parseBLASTIteration(iteration,howmany)
        return hitL
    
    def showHitList(hitL,withaccession=True):
        for j,hitD in enumerate(hitL):
            print 'hit #', j+1
            for k in ['Hit_id','Hit_def','Hit_accession']:
                print k, hitD[k]
            if withaccession:
                print hitD['Hit_accession'].ljust(10),
            hspL = hitD['hsps']
            for hspD in hspL[:1]:
                print hspD['identity'] + '/' + hspD['length'],
                print ('%3.2f' % hspD['%identity']).rjust(7)
            #print ' ' + hitD['Hit_def'].ljust(30)
                print hspD['query'][:50]
                print hspD['midline'][:50]
                print hspD['hitseq'][:50]
                print


    tree = ET.parse('blast.xml')
    hitL = parseSingleIteration(tree)
    showHitList(hitL[:3])

.. sourcecode:: python

    > python script.py
    hit # 1
    Hit_id gnl|BL_ORD_ID|0
    Hit_def A_xyl_1
    Hit_accession 0
    0          1490/1490  100.00
    AGTTTGATCCTGGCTCAGATTGAACGCTAGCGGGATGCCTTACACATGCA
    ||||||||||||||||||||||||||||||||||||||||||||||||||
    AGTTTGATCCTGGCTCAGATTGAACGCTAGCGGGATGCCTTACACATGCA

    hit # 2
    Hit_id gnl|BL_ORD_ID|3
    Hit_def A_xyl_4
    Hit_accession 3
    3          1489/1490   99.93
    AGTTTGATCCTGGCTCAGATTGAACGCTAGCGGGATGCCTTACACATGCA
    ||||||||||||||||||||||||||||||||||||||||||||||||||
    AGTTTGATCCTGGCTCAGATTGAACGCTAGCGGGATGCCTTACACATGCA

    hit # 3
    Hit_id gnl|BL_ORD_ID|1
    Hit_def A_xyl_2
    Hit_accession 1
    1          1483/1487   99.73
    AGTTTGATCCTGGCTCAGATTGAACGCTAGCGGGATGCCTTACACATGCA
    ||||||||||||||||||||||||||||||||||||||||||||||||||
    AGTTTGATCCTGGCTCAGATTGAACGCTAGCGGGATGCCTTACACATGCA

This is obviously not a comprehensive guide to parsing Pubmed or BLAST XML.  I think that if you really want to do this sort of thing you'll want to find a library or toolkit, and we will look at PyCogent later on in the book.

However, this code shows you how to get started on 'rolling your own'.