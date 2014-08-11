.. _why:

####
Why?
####

Have you ever said to yourself "I'd like to learn how to do some programming?"  And then perhaps you thought "it's probably too hard" or something like that.

The purpose of this book is to convince you that it's **not too hard**.  The target audience is a motivated person with no knowledge of programming, although it will help to have some interest in bioinformatics.

One great thing about Python is that you can learn enough to be productive with a small investment of time.  Of course, skills improve with practice.  Also I'm certain that Python is the right language for you to learn first.

**Scripting**

Recently I `came across <http://telliott99.blogspot.com/2011/08/advice-to-neuroscientist.html>`_ this `quote <http://blog.ketyov.com/2011/08/career-advice.html>`_ from a neuroscientist

    learn how to do your own data analysis. Know statistics well. Know at least some basic programming/scripting in Python, R, Matlab, etc. This will be of immense value in helping you get your research done efficiently and correctly, without needing to rely on other people's code (and time and commitment). This will become more important as our field becomes more data driven. 

The challenge is that young people studying biology sometimes follow this path because they are uncomfortable with mathematics, and think of programming as a type of math.  Nevertheless, all biologists should learn a scripting language.  If you don't, you will not be part of the future of the discipline.  In ten years, the number of non-programming neuroscientists and cancer biologists will be negligible.  The reason is simply that biology is already all about the data, except for the ideas of course, and there's *a lot* of data.  the transformation won't be immediate only because we're waiting for the old folks like me to move along.

I don't need to repeat what's been said in the discussion of relative virtues of scripting languages versus something like C++ or Java.  If you're interested, here is  a `pdf <http://www.stanford.edu/~ouster/cgi-bin/papers/scripting.pdf>`_ of a classic article by John Ousterhout.  

Scripting is terrific, and further, the requirement for quick productivity demands that you choose scripting and not C++ or Java.  Programming in a language like Python is a joy for someone who revels in instant gratification (like me).

**Python**

The most important reason to write new code in Python rather than other choices (like Perl or Ruby) is that readability really counts.  Python has been called executable pseudo-code and that is right on target.

There are several reasons for this.  Python resists the temptation to use modifier symbols like ``$`` and ``@`` for special purposes.  This means that the same variable name isn't modified to refer to different things as in Perl depending on the extra symbol (ignoring another technical issue called 'namespaces').  It's an illustration of the general Python principle that "there should be one-- and preferably only one --obvious way to do it."  This is also known as TOOWTDI.

http://wiki.python.org/moin/TOOWTDI
http://www.python.org/dev/peps/pep-0020/

In addition, Python does not use braces { to delimit statements that belong together; } and the semicolon is not usually employed either.  Admittedly this comes at the cost of enforcing the whitespace or indentation rule.  More `on whitespace <http://www.secnetix.de/olli/Python/block_indentation.hawk>`_.

For example::

    if some_statement_that_is_True_or_False:
        do_some_nifty_thing()

The indentation on the second line is required.  It could be anything you like, as long as it's consistent within a file, but I will always use 4 spaces (*not* a tab).

As I said, readability really counts.  Although you may work alone, you will find that when you come back to old code after a few months it's hard to figure out what's going on.  The clarity of Python helps a lot.

**No typing**

A second reason (arguably more important) is the tremendous flexibility that comes with a lack of 'typing'---explicit (and rigid) definition of what a variable refers to or what a complex object comprises.  If I decide that I need to add an piece of something to an object, or to return two objects instead of one from a function, I just make the change in a line or two.  I don't need to also redefine the object's type, or change the return type of a function or change its declaration.  It doesn't have one.

Every language has its enthusiasts.  Perl has been popular for bioinformatics, but from my perspective, that's a historical anomaly. Python is 100 times better.  I'm not trying to pick a fight or anything but Perl lacks readability, it violates the TOOWTDI rule above, and it doesn't handle objects and classes very well.

Furthermore, having an existing code base in a particular language is *not* a good reason to write new code in the same language.  We still use Fortran routines for math, but I really doubt anybody writes new code in it (I suppose I could be wrong).  We use those existing programs because they work, and at least as important, they have been thoroughly tested.  If someone tells you "I have this Perl script that can do X...", well, you can easily call Perl scripts from Python.  You can call C code for that matter, and I'll show you several ways to do it.  

Ruby is a popular choice and seems pretty sophisticated, but I think it violates the readability rule.  However, I know very smart people who like it, so I'm reserving judgement.

Knowing R (a toolkit that is widely used for statistical analysis) is a fundamental bioinformatics skill.  Python and R interoperate very well these days, but if you must code functions (or understand others' code) in R then you have my sympathy.  We will use R several times in this book.

I am certain that Python is the best language to learn first.  It might well be the only language you'll ever need.

**Why this book**

Why should you read this book?  And why did I write it?  I think the problem with introductory programming books is that they go too slow for the motivated student.  This book helps you to jump right in, with examples that are relevant to bioinformatics, focusing particularly on sequences.  Yet I hope that I can make the examples short enough, and the explanations clear enough, that you will be able to follow along easily.

At some point, you may become impatient for a more complete and less eclectic dose of Python.  When you reach there, I would suggest the Python `tutorial <http://docs.python.org/tutorial/>`_.  However, I also hope that in this case you will come back later to get the material on matplotlib and the advanced examples.

OK, that's enough philosophy.  As Mark Pilgrim says, it's time to "dive in."

**Introductory resources**

* Python `tutorial <http://docs.python.org/tutorial/>`_
* A gentle introduction to `programming <http://greenteapress.com/thinkpython/>`_
* `Zelle <http://www.amazon.com/gp/product/1887902996>`_:  Python Programming
* Norm Matloff's `notes <http://heather.cs.ucdavis.edu/~matloff/Python/PythonIntro.html>`_

**Intermediate level**

* A Primer on Scientific Programming with Python --- `Langtangen <http://www.amazon.com/gp/product/3642183654>`_
* A Python bioinformatics course at the `Pasteur Institute <http://www.pasteur.fr/formation/infobio/python/index.html>`_
* Mark Pilgrim's `Dive Into Python <http://diveintopython.org/index.html>`_
* Another Python book from `S. Lott <http://homepage.mac.com/s_lott/books/index.html>`_

A great resource for general skills is

* `Software Carpentry <http://software-carpentry.org/>`_

When you're ready for C or even C++:  

* Bruce `Eckel <http://www.mindview.net/Books/TICPP/ThinkingInCPP2e.html>`_
* An ocw `C course <http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-087-practical-programming-in-c-january-iap-2010/>`_

A bit more o'philosophy

* Peter `Norvig <http://norvig.com/21-days.html>`_

Oh, one last thing.  As I said in other words at the very beginning, the goal of this text is to make you comfortable enough so that when faced with a problem that can be solved with Python, your first response is to say, "Hey, I'll just write a script to do that."

Since we're trying to improve understanding while maintaining comfort, the methods given here are not always the *best* way to achieve whatever we're trying to do at a given place in the text.  Partly that's because we're building our skills in stages, and partly it's that for any complex task you should use someone else's code if you can.  And finally, for most tasks efficiency is not the critical issue (and certainly not minimizing lines of code, that's just silly).  Our goal is readability, and correctness.

I won't emphasize it, but keep in the back of your mind an awareness of the great seduction of scripting languages.  If you just wrote a nifty bit of code in half an hour this afternoon, your jewel will undoubtedly break under some (perhaps many) unexpected or as yet untested conditions.  If you hope to use your product for serious work, you must test, test and test again.

Don't say I didn't warn you.

