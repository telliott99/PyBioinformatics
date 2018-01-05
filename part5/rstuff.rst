.. _rstuff:

#################
R is for plotting
#################

Now for my big example.  I have a file containing data for medium-sized set of strains of Streptococcus.  It is ``groups.txt``::

    strep1
    AY005045     Streptococcus_mitis_bv2
    AB293402     Firmicutes_clone_CH-37
    D39          Streptococcus_pneumoniae_D39
    AY518677     Streptococcus_mitis_Sm91
    EF705292     Bacilli_clone_MS159A1_H02
    AB038371     Streptococcus_sp._PSH2
    FJ405281     Streptococcus_sp._F1

    strep2
    SK36         Streptococcus_sanguinis_SK36
    AY134908     Streptococcus_sp._12F
    AY211388     Streptococcus_clone_VA13408_01
    AB008313     Streptococcus_cristatus
    AY005042     Streptococcus_clone_BW009
    AB121930     Streptococcus_clone_BP2-57
    AM420202     Streptococcus_clone_502H08
    AY485606     Streptococcus_gordonii_10558

    strep3
    AF003933     Streptococcus_parasanguis
    DQ232536     Streptococcus_oralis_104985
    DQ016715     Streptococcus_clone_4.24

    strep4
    AF104671     Streptococcus_intermedius_ATCC27335
    AF145239     Streptococcus_anginosus_367

    strep5
    M58839       Streptococcus_salivarius
    AM696962     Uncultured_bacterium_BF0002A147

    strep6
    NEM316	     Streptococcus_agalactiae_NEM316
    X59032       Streptococcus_agalactiae_strain
    GAS          Streptococcus_pyogenes_M1_GAS

    strep7
    UA159        Streptococcus_mutans_UA159

I also have positions for rRNA genes within the (relatively few) complete genomes in the list, in the file ``genomes.txt``::

    >gi|116515308:15164-16621 Streptococcus pneumoniae D39, complete genome
    >gi|125716887:16379-17929 Streptococcus sanguinis SK36, complete genome
    >gi|25010075:16522-17930 Streptococcus agalactiae NEM316, complete genome
    >gi|15674250:17067-18616 Streptococcus pyogenes M1 GAS, complete genome
    >gi|24378532:16877-18428 Streptococcus mutans UA159, complete genome

I wrote a function to parse this data and put it in ``utils.py``

.. sourcecode:: python

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

I can exercise it from this script

.. sourcecode:: python

    import sys
    from cogent.db.ncbi import EFetch
    import utils

    D = utils.make_gid_dict('genomes.txt',
        'groups.txt')
    
    def f(k):
        return (D[k][0],k)
    if 1:
        for k in sorted(D.keys(),key=f):
            print k, D[k]
        sys.exit()

    for k in sorted(D.keys(),key=f):
        L = D[k]
        if len(L) == 2:
            gid = L[1]
            ef = EFetch(id=gid)
        else:
            kD = {'id':L[1],'from':L[2],'to':L[3]}
            gid, i, j = L[1:]
            ef = EFetch(**kD)
        print ef.read()

It looks like this:

.. sourcecode:: python

    > python script.py
    Bacilli_clone_MS159A1_H02 [0, 'EF705292']
    Firmicutes_clone_CH-37 [0, 'AB293402']
    Streptococcus_mitis_Sm91 [0, 'AY518677']
    Streptococcus_mitis_bv2 [0, 'AY005045']
    Streptococcus_pneumoniae_D39 [0, '116515308', '15164', '16621']
    Streptococcus_sp._F1 [0, 'FJ405281']
    Streptococcus_sp._PSH2 [0, 'AB038371']
    Streptococcus_clone_502H08 [1, 'AM420202']
    Streptococcus_clone_BP2-57 [1, 'AB121930']
    Streptococcus_clone_BW009 [1, 'AY005042']
    Streptococcus_clone_VA13408_01 [1, 'AY211388']
    Streptococcus_cristatus [1, 'AB008313']
    Streptococcus_gordonii_10558 [1, 'AY485606']
    Streptococcus_sanguinis_SK36 [1, '125716887', '16379', '17929']
    Streptococcus_sp._12F [1, 'AY134908']
    Streptococcus_clone_4.24 [2, 'DQ016715']
    Streptococcus_oralis_104985 [2, 'DQ232536']
    Streptococcus_parasanguis [2, 'AF003933']
    Streptococcus_anginosus_367 [3, 'AF145239']
    Streptococcus_intermedius_ATCC27335 [3, 'AF104671']
    Streptococcus_salivarius [4, 'M58839']
    Uncultured_bacterium_BF0002A147 [4, 'AM696962']
    Streptococcus_agalactiae_NEM316 [5, '25010075', '16522', '17930']
    Streptococcus_agalactiae_strain [5, 'X59032']
    Streptococcus_pyogenes_M1_GAS [5, '15674250', '17067', '18616']
    Streptococcus_mutans_UA159 [6, '24378532', '16877', '18428']

Now, I can change the ``if 1:`` in the script to ``if 0:`` and also do a redirect:

.. sourcecode:: python

    > python script.py > strep.seqs.txt
    
If I check ``strep.seqs.txt``, all the sequences are there, even the genomes::

    Bacilli_clone_MS159A1_H02
    >gi|154198058|gb|EF705292.1| Uncultured Bacilli. . .
    GACGAACGCTGGCGGCGTGCCTAATACATGCAAGTAGAACGCTGAAG. . .
    . . .
    Streptococcus_pneumoniae_D39
    >gi|116515308:15164-16621 Streptococcus pneumoniae D39, complete genome
    TGATCCTGGCTCAGGACGAACGCTGGCGGCGTGCCTAATACATGCAA. . .

Next, we'll make a phylogenetic tree with the sequences.  I realize that I don't have FASTA-formatted sequences because of the additional first line.  The reason is that I'm trying to keep the name which is used to key the dictionary above associated with the actual sequence.

For ``clustal`` we'd have to change the title lines of the sequences to be not more than eight characters.  For :ref:`muscle <muscle>` that's not necessary.  Here is what I'll do

.. sourcecode:: python

    import utils
    data = utils.load_data('strep.seqs.txt')
    data = data.strip().split('\n\n')
    for item in data:
        title,junk,seq = item.strip().split('\n',2)
        print '>' + title
        print seq
        print

.. sourcecode:: python

    python script.py > strep.mod.seqs.txt
    muscle -in strep.mod.seqs.txt -out strep.align.txt
    FastTree -nt strep.align.txt > strep.tree.txt

We can make the tree in R, using the ``ape`` library::

    library(ape)
    setwd('Desktop')
    tree = read.tree('strep.tree.txt')
    plot(tree)

That looks fine, but it's not quite snappy enough.  

.. image:: /figures/tree3.png
    :scale: 50 %

What I'd like to do is to color the species by their groups.  At this point, it is possible to be a wimp.  And I don't blame you at all.  Knowing that the list of tree$tip.label is based on the input ``tree.txt``, and that the order shouldn't change if we re-root the tree, you decide to do it by hand.

You type all the color designations following the list of nodes::

    > tree$tip.label
     [1] "Streptococcus_pneumoniae_D39"       
     [2] "Streptococcus_mitis_Sm91"           
     . . .

Like this::

    color.list=c(
    'blue','blue','maroon','maroon','maroon',
    'black','darkviolet','darkviolet','maroon','dodgerblue',
    'dodgerblue','dodgerblue','darkviolet','darkviolet','red',
    'maroon','maroon','maroon','blue','red',
    'red','red','blue','blue','blue','blue'
    )

You do the first four R commands above, and then paste the colors, and then do::

    plot(tree,tip.color=color.list,cex=1.2)

.. image:: /figures/tree4.png
    :scale: 50 %

This might be the right solution for a small plot.  But it goes against the grain to do this kind of thing by hand.  We learn from experience that we'll probably have to do it all over again, and again.

It's fragile.  Sometimes, ``ape`` will change the order of the nodes.  Then the whole structure collapses.

One way to solve this is to write an R function that goes through the ``tree$tip.label`` vector and looks up the right colors.  We need two auxiliary vectors (or a ``data frame``) with the labels and colors in corresponding order.  Something like this::

    cL = c('r','g','b')
    nL = c('A','B','C')

    f<-function(labels,df) {
        N = length(labels)
        color.list = rep('k',N)
        for (i in 1:N) {
          p = labels[i]
          x = grep(p,nL)
          if (length(x) == 1) {
            color.list[i] = cL[x]
          }
        }
        color.list
      }

    tip.label = c('B','A','C')
    color.list = f(tip.label)

Output::

    > color.list
    [1] "g" "r" "b"

Adding the complexity of a group designation seems too much.  Also, I'm sure this is not idiomatic R, but I don't know how to solve the problem that grep works on one pattern at a time.

Another way is to control R from Python using RPy2 

http://rpy.sourceforge.net/rpy2/doc-2.1/html/index.html

That's for another section.













