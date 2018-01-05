.. _trees:

#####
Trees
#####


Here is a simple tree which I generated in this post:

http://telliott99.blogspot.com/search/label/phy%20trees

.. image:: /figures/ABCDEF_tr1.png
   :scale: 50 %

A dictionary is a very natural data structure for trees.  Here is a version that doesn't have the branch lengths:

.. sourcecode:: python

    trD = { '0':['A','B','1'],
            '1':['C','0','3'],
            '2':['E','D','3'],
            '3':['F','1','2'] }
        
We could add the lengths this way:

.. sourcecode:: python

    trD = { '0':[('A',1.0),('B',4.0),('1',1.0)]. . .

But it seems messy and redundant.  Perhaps it's better to just use a second dictionary:

.. sourcecode:: python

    bD = { 'A0':1.0,'B0':4.0,'C1':2.0,
           'D2':2.75,'E2':2.25,'F3':4.75,
           '01':1.0,'13':1.25,'23':0.75 }
       
The Newick representation of this tree is::
       
    (E:2.25,D:2.75,
    (((A:1,B:4):1,C:2):1.25,
    F:4.75):1.0);
    
http://en.wikipedia.org/wiki/Newick_format

Here we are working with this tree in R::

    > library(ape)
    > setwd('Desktop')
    > tr = read.tree('ABCDEF_tr.txt')
    > tr

    Phylogenetic tree with 6 tips and 4 internal nodes.

    Tip labels:
    [1] "E" "D" "A" "B" "C" "F"

    Unrooted; includes branch lengths.
    > tr$edge
          [,1] [,2]
     [1,]    7    1
     [2,]    7    2
     [3,]    7    8
     [4,]    8    9
     [5,]    9   10
     [6,]   10    3
     [7,]   10    4
     [8,]    9    5
     [9,]    8    6
     > names(tr)
     [1] "edge"        "Nnode"       "tip.label"  
     [4] "edge.length"
     > tr$edge.length
     [1] 2.25 2.75 1.00 1.25 1.00 1.00 4.00 2.00 4.75
     > tr$tip.label
     [1] "E" "D" "A" "B" "C" "F"
    > plot(tr,type='unrooted')
    > nodelabels(cex=2)

R has labeled the leaf nodes ``ABCDEF`` in order ``345216``.  This is the order they appear in the file ``tree.txt``.  The internal nodes are also labeled in the order they were encountered.

The 'edges' are numbered ``1-9`` as shown in ``tr$edge``.  For example, edge ``1`` connects nodes ``1 (E)`` and ``7`` (what we had called ``4`` at the top), and the length is 2.25.

I'd like to return to the Python dictionary representation of the tree:

.. sourcecode:: python

    trD = { '0':['A','B','1'],
            '1':['C','0','3'],
            '2':['E','D','3'],
            '3':['F','1','2'] }

    all = list()
    for k in trD:
        all.extend(trD[k])

    e_nodes = [e for e in all if not e in trD]

    def descend(node,seen,v=False):
        if v:
            print 'descend', node, seen
        seen.append(node)
        if not node in e_nodes:
            for child in trD[node]:
                if not child in seen:
                    descend(child,seen,v)

    def traverse_tree(root,v=False):
        seen = list()
        descend(i_node,seen,v)
        return seen    

    for i_node in trD:
        print i_node
        print traverse_tree(i_node)

    print 'reporting:'
    print traverse_tree('2',v=True)

For each internal node (``i_node``), we call ``traverse_tree``.  The output from the first run (without the last two lines) is::

    > python script.py
    0
    ['0', 'A', 'B', '1', 'C', '3', 'F', '2', 'E', 'D']
    1
    ['1', 'C', '0', 'A', 'B', '3', 'F', '2', 'E', 'D']
    2
    ['2', 'E', 'D', '3', 'F', '1', 'C', '0', 'A', 'B']
    3
    ['3', 'F', '1', 'C', '0', 'A', 'B', '2', 'E', 'D']

And the verbose 'report'::

    reporting:
    descend 2 []
    descend E ['2']
    descend D ['2', 'E']
    descend 3 ['2', 'E', 'D']
    descend F ['2', 'E', 'D', '3']
    descend 1 ['2', 'E', 'D', '3', 'F']
    descend C ['2', 'E', 'D', '3', 'F', '1']
    descend 0 ['2', 'E', 'D', '3', 'F', '1', 'C']
    descend A ['2', 'E', 'D', '3', 'F', '1', 'C', '0']
    descend B ['2', 'E', 'D', '3', 'F', '1', 'C', '0', 'A']
    ['2', 'E', 'D', '3', 'F', '1', 'C', '0', 'A', 'B']

The code is recursive (``descend`` calls itself).  Trace the order in which the nodes are visited.  This is called a pre-order traversal.

http://en.wikipedia.org/wiki/Tree_traversal

http://en.wikipedia.org/wiki/Depth-first_search

We definitely don't want to write our own code for dealing with trees.  We can use PyCogent.

>>> from cogent import LoadTree
>>> tr = LoadTree('ABCDEF_tr.txt')
>>> print tr.asciiArt()
          /-E
         |
         |--D
         |
-root----|                              /-A
         |                    /edge.0--|
         |          /edge.1--|          \-B
         |         |         |
          \edge.2--|          \-C
                   |
                    \-F


>>> for t in tr.preorder():
...     print t.getNewick()
... 
(E,D,(((A,B),C),F));
E;
D;
(((A,B),C),F);
((A,B),C);
(A,B);
A;
B;
C;
F;

The tree has been rooted at the node we called ``2``.  (That's why I did the verbose output with root=``2``).

The difference between the order of nodes in the two traversals is due to which child node is called 'left' and 'right' at each descent.  Remember that trees are like mobiles.

http://en.wikipedia.org/wiki/Mobile_(sculpture)
