.. _process:

##############
Unix Processes
##############

All of the standard Unix commands, which are just programs after all, can be run from within Python.  For example ``pwd`` becomes ``import os;  print os.getcwd()``.

In this chapter, we look at how to run anything that the shell can run, such as :ref:`muscle <muscle>`, from within a Python script.

Here is an example, from a previous chapter:

.. sourcecode:: python

    import subprocess, os, sys

    def run(cmd):
        p = subprocess.Popen(cmd, shell=True)
        sts = os.waitpid(p.pid, 0)
        pid,exitCode = sts
        print sts
        if exitCode:  
            sys.exit(exitCode)

    fn = 'seqs.mod.txt'
    mfn = 'align.txt'
    tfn = 'tree.txt'

    L = ['muscle', '-in', fn, '-out', 'align.txt']
    run(' '.join(L))
    L = ['FastTree', mfn, '>', tfn]
    run(' '.join(L))

We'll use ``muscle`` and :ref:`FastTree <FastTree>` to align our sequences.  If you actually run this from the file ``script.py``, by doing ``python script.py``, you'll see (among other output)::

    (10608, 0)
    (10609, 0)

These are the process ids (``pid``) and exit codes for the two processes we ran.  In Unix, an exit code of 0 is good, it means no errors occurred.

You will notice that new files ``align.txt`` and ``tree.txt`` have appeared on the Desktop, if they were not there already.  If they were present before, the previous versions have been over-written, without mercy.

There are only two programs in this example so far, but there could be a dozen or a hundred.

The third step we will take is to use R to plot the tree.  R is a little finicky.  One way to do what we want is to write the R code to be executed into a text file like ``Rcode.txt``::

    library(ape)
    tr = read.tree('tree.txt')
    pdf('plot.pdf')
    plot(tr,edge.width=3,cex=2,type='unrooted')
    dev.off()
    
We'll see another way to do it later, using ``RPy``.

Now, from the Python script do:

.. sourcecode:: python

    ifn = 'Rcode.txt'
    L = ['R CMD BATCH', ifn]
    run(' '.join(L))

If everything works, you'll get::

    (10613, 0)
    
If not, you might get::

    (10938, 256)

If it works, the exit code will be 0 and the file ``plot.pdf`` will appear on the Desktop.  If it doesn't work, you can check the file ``Rcode.txt.Rout``;  it may say something like I got in an earlier version of this script::

    > library(ape)
    > setwd('Desktop')
    Error in setwd("Desktop") : cannot change working directory
    Execution halted

I do ``setwd('Desktop')`` when I start R as R.app, because otherwise the default is something else so I can't read say, ``tree.txt`` without a full path.  But when I run R this way, we're already in the Desktop, and it complains and throws an error.  Kind of lame, but that's the way it is.

For the moment, I don't want to cover this, but if you are interested in Phylip

http://evolution.genetics.washington.edu/phylip.html

and want to run it as a process, I have a blog post you'll want to read:

http://telliott99.blogspot.com/2010/03/running-phylip-as-process.html