.. _bytes:

##############
Bits and Bytes
##############

In this example, I'll post the output first::

    > python script.py
    x     00000000 00000000 00000010 10011010 = 666
    y     00000000 00000000 00000001 10111011 = 443
    x + y 00000000 00000000 00000100 01010101 = 1109
    check 666 + 443 = 1109
    x * y 00000000 00000100 10000000 01111110 = 295038
    check 666 * 443 = 295038
    z      3
    x**z  00010001 10011011 10010010 10101000 = 295408296
    check 666 ** 3 = 295408296

    x     00000000 00000000 00000000 00010101 = 21
    y     00000000 00000000 00000001 11111111 = 511
    x + y 00000000 00000000 00000010 00010100 = 532
    check 21 + 511 = 532
    x * y 00000000 00000000 00101001 11101011 = 10731
    check 21 * 511 = 10731
    z      7
    x**z  01101011 01011010 01101110 00011101 = 1801088541
    check 21 ** 7 = 1801088541

The class ``word`` in the file ``word.py`` defines a class that represents 4 byte binary words as strings and has functions to do addition, multiplication and exponentiation.  It's a bit long, but since this is not a 'dead trees' text, I'm going to include it.  Jump ahead if you wish.

The point of the example is to see something about the way binary addition and multiplication work.

Here is the critical part for addition.  We construct a string of length 2 that contains the two bits we're adding.  The logic:

.. sourcecode:: python

    if (t == '01' or t == '10'):
        if carry == '0':
            rL.append('1')
        if carry == '1':
            rL.append('0')
    elif t == '00':
        rL.append(carry)
        carry = '0'
    else:
        assert t == '11'
        if carry == '0':
            rL.append('0')
            carry = '1'
        else:
            rL.append('1')
            carry = '1'

And if you look carefully at multiplication you'll see that we're doing it by bit-shifting.  We construct a list for each position in the multiplicand that has the value ``1``, doing the multiplication by shifting appropriately, then we add all the results together at the end.

That's really fast.

http://en.wikipedia.org/wiki/Peasant_multiplication

http://en.wikipedia.org/wiki/Bitwise_operation

Here is the full listing for ``word.py``:

.. sourcecode:: python

    class word:
        SZ = 32
        def __init__(self,n):
            if type(n) == type('a'):
                b = n.rjust(word.SZ,'0')
            elif type(n) == type(1):
                b = bin(n)[2:]
            else:
                raise ValueError, "can't do that"
            self.b = b.rjust(word.SZ,'0')
        
        def __repr__(self):
            b = self.b
            s = ' '.join([b[:8], b[8:16], b[16:24], b[24:]])
            s += ' = ' + str(eval('0b' + self.b))
            return s
        
        def __add__(self, a):
            carry = '0'
            rL = list()
            for i in range(len(self.b)-1,-1,-1):
                x = self.b[i]
                y = a.b[i]
                t = x+y
                if (t == '01' or t == '10'):
                    if carry == '0':
                        rL.append('1')
                    if carry == '1':
                        rL.append('0')
                elif t == '00':
                    rL.append(carry)
                    carry = '0'
                else:
                    assert t == '11'
                    if carry == '0':
                        rL.append('0')
                        carry = '1'
                    else:
                        rL.append('1')
                        carry = '1'
            if carry == '1':
                raise ValueError, 'overflow'
            rL.reverse()
            return word(''.join(rL))
    
        def __mul__(self, a):
            L = list()
            for i in range(len(self.b)-1,-1,-1):
                x = self.b[i]
                if not x == '1':
                    continue
                n = word.SZ - i - 1
                r = word(a.b[n:] + '0'*(n))
                L.append(r)
            res = L.pop(0)
            #print 'start:       ', res
            while L:
                next = L.pop(0)
                #print 'next:        ', next
                res = res + next
                #if L:
                    #print 'intermediate:', 
                #else:
                    #print 'result:      ',
                #print res
            return res

        def __pow__(self, n):
            res = self
            for i in range(n-1):
                res = res * self
            return res

The principle behind binary multiplication is pretty simple.  The first thing is that multiplicatiion of any binary number by a power of two results in the same pattern of digits, just shifted to the left.

>>> b = '0b11001010'
>>> int(b,2)
202
>>> bin(202)
'0b11001010'
>>> for i in [2,4,8,16,32,64]:
...     n = i*int(b,2)
...     print bin(n), n
... 
0b110010100 404
0b1100101000 808
0b11001010000 1616
0b110010100000 3232
0b1100101000000 6464
0b11001010000000 12928

Python doesn't show all the zeroes to the left of the left-most 1 in the binaary version of 404 (or any of the other numbers).

The other thing is that (obviously) any multiplier can be factored into multiples of 2, including 2e0 = 1.  For example 202 is:

>>> bin(202)
'0b11001010'
128 + 64 + 8 + 2

So, to multiply 202 by itself we must add together::

    0b110010100
    0b11001010000
    0b11001010000000
    0b110010100000000

It'll help if we right-justify them and add some leading zeroes::

    0b0000000110010100
    0b0000011001010000
    0b0011001010000000
    0b0110010100000000

Adding more than two binary numbers by hand can get a little tricky, but this one is easy::

    0b0000000110010100
    0b0000011001010000
    0b0011001010000000
    0b0110010100000000

    0b1001111101100100

>>> b = '0b1001111101100100'
>>> int(b,2)
40804
>>> 202**2
40804

So that's our strategy for binary multiplication.  We identify a multiplicand (the number which is multiplied) and a multiplier.  We might pick the multiplier to be the smaller number (or perhaps, the one with the fewest 1's).  If the multiplier has a 1 in the last place, we add one of the current version of the multiplicand to an accumulating sum.  

Then, we bit-shift the multiplier to the right, and bit-shift the multiplicand to the left, and repeat.  When the multplier consists only of zeros, we're done.
            
And here is a longish ``script.py`` to 'exercise' our class:

.. sourcecode:: python

    import random
    from word import word

    R = range(1000)
    N = 10
    for i in range(N):
        x = random.choice(R)
        y = random.choice(R)    
        xw = word(x)
        print 'x    ', xw
        yw = word(y)
        print 'y    ', yw

        print 'x + y',
        r = xw + yw
        print r
        S = x+y
        assert S == int(str(r).split()[-1])
        print 'check', x, '+', y, '=', S

        print 'x * y',
        r = xw * yw
        print r
        P = x*y
        assert P == int(str(r).split()[-1])
        print 'check', x, '*', y, '=', P

        for i in range(2,N*2):
            try:
                r = xw**i
            except ValueError:
                i = i-1
                break

        z = i
        print 'z     ', z
        print 'x**z ', r
        E = x**z
        try:
            assert E == int(str(r).split()[-1])
        except AssertionError:
            print 'ran into a slight problem\n'
            continue
        print 'check', x,'**', z, '=', E
        print

The output is shown at the top of the section.  It might be fun to experiment with fast exponentiation.

http://en.wikipedia.org/wiki/Exponentiation_by_squaring