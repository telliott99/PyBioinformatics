.. _text:

####
Text
####

I have a file containing exam questions.  Here is part of it::

    Which has had the largest impact on average life \
    expectancy of humans:
    the internet
    Viagra
    antibiotics
    advances in cancer therapy
    clean drinking water and vaccination

The ``\`` was added to make the line wrap and fit the page.

.. sourcecode:: python

    fn = 'questions.txt'
    FH = open(fn, 'r')
    data = FH.read().strip()
    FH.close()

    rL = list()
    for i, item in enumerate(data.split('\n\n')):
        sL = list()
        q, rest = item.split('\n', 1)
        sL.append(str(i+1) + '.  ' + q)
        answers = rest.split('\n')
        for j, a in enumerate(answers):
            sL.append('ABCDE'[j] + '.  ' + a)
        rL.append('\n'.join(sL))

    print '\n\n'.join(rL)

.. sourcecode:: python

    > python script.py 
    
Output::

    1.  Which has had the largest impact on average life \
    expectancy of humans:
    A. the internet
    B. Viagra
    C. antibiotics
    D. advances in cancer therapy
    E. clean drinking water and vaccination

This example illustrates the power of our approach, since I didn't have to spend two hours manually adding numbers and letters to my questions.  (But I did spend more time than I should admit debugging the script).  This can easily be extended to randomly scrambling the questions and the foils, and generating a key for each scrambled version.  I'll leave that as an exercise.

**Ulysses**

I obtained a copy of *Ulysses*, probably the most famous novel written in the English language, on the web.  No, I didn't smuggle it into the U.S., it's from Project Gutenburg.

http://www.gutenberg.org/etext/4300

Although I suppose it could be a munition of some kind.  We might have to worry about export.

http://en.wikipedia.org/wiki/Arms_Export_Control_Act

Re-focus on *Ulysses*.

I deleted a short header and footer.  Let's load it into memory.  We simplify a bit by using all lowercase, and removing punctuation except for newlines and spaces.

.. sourcecode:: python

    import random

    fn = 'ulysses.txt'
    FH = open(fn, 'r')
    data = FH.read().strip()
    FH.close()

    data = data.replace('\r','')
    data = data.lower()
    text = ''.join([c for c in data if c.isalpha() or c in ' \n'])
    print len(text)
    print text[-54:], '\n'

    D = dict()
    for word in text.split():
        if word in D:
            D[word] += 1
        else:
            D[word] = 1
        
    def f(k):
        return D[k]
    L = sorted(D.keys(), key=f)
    sL = L[-10:]
    m = max([len(w) for w in sL])
    for w in L[-10:]:
        print w.ljust(m+2), D[w]

    euphemism = 'sh*t'
    badword = euphemism.replace('*','i')
    print '%s occurs %i times.' % (euphemism, D[badword])

.. sourcecode:: python

    > python script.py 
    1424388
    heart was going like mad and yes I said yes I will Yes

    that   2606
    i      2697
    his    3333
    he     4031
    in     4924
    to     4962
    a      6500
    and    7214
    of     8138
    the    14932
    sh*t occurs 4 times.

Now let's try to do something more interesting than counting 'bad' words.  As we scan through the text, treat each word and the one following as a pair, and for each pair of words add the second to a list held in a dictionary keyed by the first.  We can then form Joyce-like text by making a Markov chain starting, of course, from 'i'.

.. sourcecode:: python

    def parse(s):
        words = s[:20000]
        D = dict()
        e1 = words.pop(0).strip()
        while words:
            e2 = words.pop(0).strip()
            try:  D[e1].append(e2)
            except KeyError:  D[e1] = [e2]
            e1 = e2
        for k in D:
            D[k] = list(set(D[k]))
        return D

    def speak(D,first,N=50):
        L = [first]
        w1 = first
        for i in range(N):
            w2 = random.choice(D[w1])
            L.append(w2)
            w1 = w2
        return ' '.join(L)

    def pprint(s):
        i = 0
        n = 40
        while True:
            j = s.find(' ',i+n)
            if j == -1:  
                print s[i+n:]
                break
            if i:  print s[i+1:j]
            else:  print s[:j]
            i = j

    D = parse(text.split())
    result = speak(D,first='i')
    pprint(result)
    
Here it is:

    i couldnt stomach that we could have enjoyed ourselves new garters strings twanged night sky moon in rapt attention his master it cant see my people with mute bearish fawning unheeded he calls it buck mulligans voice when esther osvalts shoe went to clear loose

After trying many times, I still like this one best

http://telliott99.blogspot.com/2009/07/python-for-simulations-5.html

    i pass on coronation day by the brazen cars woodshadows floated silently by greed and behold they wait no she said as i wanted to win in a cockney accent o thats our hearts his gaze and squat its loose tobaccoshreds slanted
    
I think I hear Joyce's voice.