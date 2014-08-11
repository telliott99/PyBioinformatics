.. searching:

#########
Searching
#########

There are ``find``, ``count`` and ``index`` methods for strings

>>> s = 'abc'
>>> s.index('b')
1
>>> s.find('b')
1
>>> s.count('a')
1
>>> s.find('z')
-1
>>> s.count('z')
0
>>> s.index('z')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: substring not found

It's an error to ask for the``index`` of an object that is not in the string.

``find`` can take additional arguments 

http://docs.python.org/library/stdtypes.html#str.find

Consider:

>>> s = 'abcabc'
>>> i = s.find('a', 0)
>>> i
0
>>> j = s.find('a', i+1)
>>> j
3
>>> s.find('a', j+1)
-1

The search starts from the beginning of s at index 0.  Python finds the first 'a' right away at index 0, and returns that value.  Next, we constrain the search to index 1 and above, and then find the next 'a' at index 3.  There is no third 'a' to be found and the function returns -1.

I have (too) quickly written code like the above that fails to update the search index by + 1, but I can't show a good example of that until we know a bit more about how to control the flow of code.  It's an easy error to make.

The count method can give counter-intuitive results for search targets larger than a single character:

>>> s = 'GAATAACAA'
>>> s.count('AA')
3
>>> s = s + 'A'
>>> s
'GAATAACAAA'
>>> s.count('AA')
3
>>> s = s + 'A'
>>> s
'GAATAACAAAA'
>>> s.count('AA')
4
>>> 'AAAAAA'.count('AA')
3

The substrings returned are non-overlapping.  Also, I should point out that a more idiomatic way to do the addition is to use '+=':

>>> s = 'ACGT'
>>> s += 'AAA'
>>> s
'ACGTAAA'

Probably the large number of methods for strings and lists has your head with that "too full" feeling.  Just put these links to the Python docs for lists and strings in an accessible place.  You'll use them a lot:

http://docs.python.org/tutorial/datastructures.html#more-on-lists

http://docs.python.org/library/stdtypes.html#string-methods