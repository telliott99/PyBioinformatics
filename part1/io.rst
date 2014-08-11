.. _io:

########################
Reading and writing data
########################

For any serious work, we will want to read data from a file on disk and perhaps write to disk as well.  Suppose we have a file ``data.txt`` on the Desktop with this::

    my data has five words
    for each of two lines

The method I would typically use is:

>>> fn = 'data.txt'
>>> FH = open(fn,'r')
>>> data = FH.read()
>>> FH.close()
>>> L = data.strip().split('\n')
>>> for line in L:
...     print '*' + line + '*'
... 
*my data has five words*
*for each of two lines*

(The 'r' is unnecessary, the ``read`` mode is the default, but I like the clarity).

A newer syntax would be:

>>> with open(fn) as f:
...     L = f.readlines()
... 
>>> for line in L:
...     print '*' + line + '*'
... 
*my data has five words
*
*for each of two lines
*

``readlines`` leaves the newline at the end of each line.  We usually wouldn't want that:

>>> for line in L:
...     line = line.rstrip()
...     print '*' + line + '*'
... 
*my data has five words*
*for each of two lines*

It's not necessary to do an explicit close with the second approach.

>>> f.closed
True

And writing data is similar:

>>> fn = 'data2.txt'
>>> FH = open(fn,'w')
>>> L.append('this is a third line')
>>> FH.write('\n'.join(L))
>>> FH.close()

The alternative would be:

>>> with open(fn,'w') as f:
...     f.write('\n'.join(L))
... 
