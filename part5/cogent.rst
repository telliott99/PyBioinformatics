.. _cogent:

########
PyCogent
########

As it says in the `docs <http://pycogent.sourceforge.net/>`_,

    "PyCogent is a software library for genomic biology."
    
That sounds perfect.

I want to explore PyCogent a little bit here, but there are two disclaimers right away.  First, the project has excellent documentation with a cookbook 

http://pycogent.sourceforge.net/cookbook/index.html

(always my favorite), and a bunch of examples

http://pycogent.sourceforge.net/examples/index.html

Second, I've blogged about this *a lot*

http://telliott99.blogspot.com/search/label/PyCogent

so you might want to browse there as well.

I thought it would be a good exercise for us to install this software and use it a bit, and I also want the utilities to make things simpler for future explorations.  

According to the readme, the absolute requirements 

http://pycogent.sourceforge.net/README.html#required

* Python

* Numpy

* zlib (a compression library)

The optional stuff

http://pycogent.sourceforge.net/README.html#optional

* C compiler

* matplotlib

* cython

* mpi4py

* SQLAlchemy

* MySQL-python

I'd like to not worry about the optional stuff right now, although we talked about the compiler and I hope you have installed ``matplotlib`` already when we talked about that.  On OS X, all we really need to worry about is ``zib``.  On Linux, you should already have everything if you followed the instructions I gave before.

.. TODO  about zlib on OS X

To install PyCogent, just follow the instructions.  As I write this, I have the downloaded zipped files from the link here

http://sourceforge.net/projects/pycogent/

I unpack it on the Desktop and do

http://pycogent.sourceforge.net/README.html#installation

like this::

    cd PyCogent
    python setup.py build
    sudo python setup.py install


more about ``sudo``
more about administrator accounts

Let's see:

>>> import cogent
>>> cogent.__version__
'1.6.0dev'

We can use cogent to get sequences from NCBI

.. sourcecode:: python

    from cogent.db.ncbi import EFetch
    ef = EFetch(id='AY207063')
    print ef.read()

.. sourcecode:: python

    >gi|29290057|gb|AY207063.1|. . .
    GACGAACGCTGGCGGTGTGCCTAATACATG. . .

One slight difficulty that I needed to work through is that sometimes I'm interested in only a part of a sequenced bacterial genome.  One option would be to download a complete genome, grab the rRNA gene sequence and just throw the rest away.  But it seems wasteful.

As I've blogged 

http://telliott99.blogspot.com/2011/02/fetching-sequences-from-ncbi.html

the URL that we would normally use (say as given by the RNA __ link 

http://telliott99.blogspot.com/2011/02/fetching-sequences-from-ncbi.html

reached from the overview page 

http://www.ncbi.nlm.nih.gov/sites/genome/?term=115&dopt=Overview

of the genome projects page 

http://www.ncbi.nlm.nih.gov/genomes/lproks.cgi

at NCBI) would be

http://www.ncbi.nlm.nih.gov/nuccore/NC_000913?from=4164682&to=4166223

Something like that is what I really need to construct.

I have a solution that works for me, though I'm not sure it's the best thing to do.  It's described in this post

http://telliott99.blogspot.com/2011/02/fetching-sequences-from-ncbi.html

I changed line 134-135 in ``cogent.util.ncbi`` to::

    PrintedFields = dict.fromkeys(['db', 'rettype', 'retmode', 'query_key',\
        'id', 'from', 'to',
        'WebEnv', 'retmax', 'retstart', 'tool', 'email'])
    
The change was to take ``id`` out of line 135 and add the new line in the middle.

A strange thing is that according to a test, this may not be necessary when working from the interpreter, but it was necessary from a script.  If it's real I suspect the difference may have to do with the order of the keys within the URL that cogent constructs.  NCBI seems not to like it if the 'id' comes after the 'to' and 'from'.  More testing is needed to be sure. . .

Anyway, from the interpreter now I can do:

>>> from cogent.db.ncbi import EFetch
>>> D = {'id':'NC_000913','from':'4164682','to':'4166223'}
>>> ef = EFetch(**D)
>>> print ef.read()
>gi|49175990:4164682-4166223 Escherichia coli. . .
AAATTGAAGAGTTTGATCATGGCTCAGATTGAA . . .

And it works!  You should have about 1500 nt in the sequence, rather than 4.6 million.

.. _genbank_record:

GenBank Record
--------------

We can use PyCogent to parse a Genbank record very easily.  Here is a script that fetches the sequence of the *Salmonella typhimurium* genome from Genbank.  We save it to disk before reloading it for processing.  We write a list of all the genes and their coordinates.

.. sourcecode:: python

    from cogent.db.ncbi import EUtils
    from cogent.parse.genbank import RichGenbankParser

    def fetch_seq(gid,gb_fn):
        e = EUtils(db="nucleotide", rettype="gb")
        outfile = open(gb_fn,'w')
        outfile.write(e[gid].read())
        outfile.close()
    
    def get_cds(gb_fn):
        FH = open(gb_fn,'r')
        parser = RichGenbankParser(FH)
        accession, seq = [record for record in parser][0]
        def gene_and_cds(f):
            return f['type'] == 'CDS' and 'gene' in f
        return [f for f in seq.Info.features if gene_and_cds(f)]
    
    def get_locations(cL):
        for cds in (cL):
            print cds['gene'][0].ljust(6),
            loc = cds['location']
            print loc.first(), loc.last(),
            if loc.strand() == 1:
                print 'cw'
            else:
                print 'ccw'
    
    if __name__ == '__main__':
        gid = 'AE006468'
        gb_fn = 'seq.gb'
        #fetch_seq(gid,gb_fn)
        L = get_cds(gb_fn)
        get_locations(L)

Just uncomment the third to last line to do the sequence fetch.
We save with a redirect:

.. sourcecode:: python

    python script.py > genes.txt

At this point the data looks like this::

    thrL   190 255 cw
    thrA   337 2799 cw
    thrB   2801 3730 cw
    thrC   3734 5020 cw
    yaaA   5114 5887 ccw
    yaaJ   5966 7396 ccw
    talB   7665 8618 cw . . .

and we can process it however we like.

Something to remember here is that *some people* count starting from 1, while Python starts at 0.  When we get data like this, and we'll be reading the sequence for ourselves later on, we need to think about possible conflicts.  I think a good approach is to adopt the policy that conversion happens on reading or writing the data.  That is, ``get_locations`` should modify the data to have Python-style indexing.  We'll fix that next time we use it.

.. sourcecode:: python

    print int(loc.first()) - 1, int(loc.last()) - 1,

I was curious to see how it would handle a split gene.  The example I've wrestled with repeatedly over the years is the *E. coli prfB* gene.

So I re-ran the script with ``U00096.2``.  I got::

    prfB   3033206 3034304 ccw

If you look in the actual text of the Genbank record::

    gene            complement(3033206..3034304)
                    /gene="prfB"
    CDS             complement(join(3033206..3034228,3034230..3034304))
                    /gene="prfB"

What's happening is that the **gene** shows only the extent of the gene and not the detail of the switched reading frame.  This will cause an error later on if we were not aware of it.  On the other hand, there are very few genes like this and it's a pain to deal with.  So I've just left it as an unsolved problem.

Check out the PyCogent Cookbook

http://pycogent.sourceforge.net/cookbook/index.html
