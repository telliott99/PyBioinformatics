.. _strings:

#################
Strings and Lists
#################

Let's start talking about programming.  It's a little bit like swimming.  My strategy as your instructor is to have us walk right up to the edge of the swimming pool and then jump in.  Luckily, we'll find the water is only about 3 feet deep.  (Although Mark Pilgrim's excellent book is called 'Dive into Python', everyone knows you should only dive into the deep end of the pool).

My motto is "learn by doing." 

Leaving the analogy behind, the examples in this first chapter are fundamental, and the explanations (I hope) can be comprehended with very little background.

The notion of a function should be familiar enough from math for you to have an intuition about how they work before we make a formal introduction.  A function is a kind of machine into which we feed one or more values ('arguments') and then later it gives us back one or more results when it's finished.  You can think of it for now as 'black box'.

Sometimes functions are called methods, e.g. the ones 'associated' with the objects---strings and lists---we're studying in this chapter.  Don't worry about the distinction yet.

As we saw in the previous section, a string can be constructed explicitly

>>> s = 'abcde'
>>> s
'abcde'
    
In addition to the string type, the second fundamental data type in Python is the list.  Lists can be constructed explicitly using square brackets, with commas to separate the values.  Alternatively, a list can be constructed by calling the Python ``list`` function on a string.

>>> L = ['a','b','c','d','e']
>>> L
['a', 'b', 'c', 'd', 'e']
>>> L = list('abcde')
>>> L
['a', 'b', 'c', 'd', 'e']
>>> L = list(s)
>>> L
['a', 'b', 'c', 'd', 'e']

We converted a string into a list of the individual characters.  (But they are not called characters, they're strings.  These particular strings have length one). 

We can ``join`` the elements of a list of strings:

>>> L = list('abcde')
>>> L
['a', 'b', 'c', 'd', 'e']
>>> s = ''.join(L)
>>> s
'abcde'

Probably the most common operation in bioinformatics uses ``join`` and its reverse ``split``.  Suppose we have a string containing newlines:

>>> s = '>my_seq\nATGCAACGAT\nTACGTTGCTA'
>>> print s
>my_seq
ATGCAACGAT
TACGTTGCTA
>>> L = s.split('\n')
>>> L
['>my_seq', 'ATGCAACGAT', 'TACGTTGCTA']
>>> '\n'.join(L)
'>my_seq\nATGCAACGAT\nTACGTTGCTA'

The list L contains the three lines that were originally separated by newlines in a single string in the input.

Notice that we called ``join`` by doing ``'some_string'.join(some_list)``.  In the first example, the first component (pasted between each component of the list), was the empty string, but in the second it was the newline character.

One very useful technique is to separate blocks of similar data (like FASTA-formatted sequences) by double newlines.  Suppose we have this data in a file named ``seqs.txt``::

    >seq1
    ATGCA

    >seq2
    TACGT

We load the data:

>>> FH = open('seqs.txt','r')
>>> data = FH.read()
>>> FH.close()
>>> data
'>seq1\nATGCA\n\n>seq2\nTACGT'
>>> L = data.split('\n\n')
>>> L
['>seq1\nATGCA', '>seq2\nTACGT']
>>> s = '\n\n'.join(L)
>>> s
'>seq1\nATGCA\n\n>seq2\nTACGT'

In this example the list L contains two strings, each corresponding to one of the blocks of FASTA sequence in the input.

There is a quote from a famous book about computer science by Abelson et al., commonly abbreviated SICP:

    Programs must be written for people to read, and only incidentally for machines to execute.

http://mitpress.mit.edu/sicp/
    
From this it apparently follows that in real code variables should have informative names.  Not ``L`` or ``my_list`` but ``seq_list`` or ``my_fancy_data_type_list`` or something. 

Nevertheless, I routinely break this rule and will do so here.  Partly, it's just that I don't like the clutter.  

I use ``L`` only as the variable name for a list, ``s`` to signify a string, ``c`` to signify a character in a string, ``i`` for an integer, ``f`` for a floating point value, and so on.  If I have a list of items that will be returned from a function I use ``rL`` for return list;  a list of items to be ``join``-ed and printed is ``pL``.

It will make the examples clearer, but you should be preparing mentally for the day when you come back to your code after six months and need to figure out what the heck is going on.  Descriptive variable names are important in real code.

At some later time, it will be well worth it to read the docs for the most commonly used functions.  For ``split``, we learn 

http://docs.python.org/library/stdtypes.html#str.split

that the usage is::

    str.split([sep[, maxsplit]])

The brackets mean that we can call the function ``split`` in several different ways.  We can call it with no separator.  In that case, it splits on whitespace---spaces, tabs and newlines.

We can also specify the number of times to do a split but for that case we need to enter a separator just before, to tell Python clearly what we want to do, the separator and the number of splits at the same time:

>>> s = '>my_seq\nATGCAACGAT\nTACGTTGCTA'
>>> s.split()
['>my_seq', 'ATGCAACGAT', 'TACGTTGCTA']
>>> title,seq = s.split('\n',1)
>>> title
'>my_seq'
>>> seq
'ATGCAACGAT\nTACGTTGCTA'

It is an error if there are not enough variable names for all the assignments:

>>> s = '>my_seq\nATGCAACGAT\nTACGTTGCTA'
>>> title,seq = s.split()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: too many values to unpack

You can either supply enough names for all the values being returned, or a single name, in which case the values come back as a list.  (Technically, all Python functions return a single object, which may be a ``tuple``.  The tuple can be converted into a list, or unpacked into as many variables as there are items in the tuple).

Another useful string method is ``strip``, which removes whitespace from either end of a string.  This is important since if there is any extra space, then splitting on the newline will give us that space as an extra element of the resulting list.  I often use ``strip`` and ``split`` in combination.  Notice the extra single space at the end of the string s:

>>> s = ' abc.\n.xyz\n '
>>> L = s.split('\n')
>>> L
[' abc.', '.xyz', ' ']
>>> s.strip().split()
['abc.', '.xyz']

There are also versions of ``strip`` that are directional:  ``lstrip`` and ``rstrip``.

Cumulatively, I've wasted hours chasing bugs caused by an extra item after ``split``.  Use ``strip`` reflexively and you won't have that problem.