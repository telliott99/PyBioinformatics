.. _struct:

###########
Binary data
###########

I have an example that gets into bits and bytes some more.  It involves key pairs for public key cryptography.  I hope that's not too far afield for a Bioinformatics text.

http://en.wikipedia.org/wiki/Public-key_cryptography

We can use the ``ssh-keygen`` utility from the command line to generate a new key pair.

http://en.wikipedia.org/wiki/Ssh-keygen

Normally we would encrypt the private key file with a passphrase, but today we don't::

    > ssh-keygen -b 1024 -t rsa
    Generating public/private rsa key pair.
    Enter file in which to save the key (/Users/telliott/.ssh/id_rsa): /Users/telliott/Desktop/id_rsa
    Enter passphrase (empty for no passphrase): 
    Enter same passphrase again: 
    Your identification has been saved in /Users/telliott/Desktop/id_rsa.
    Your public key has been saved in /Users/telliott/Desktop/id_rsa.pub.
    The key fingerprint is:
    5e:81:d2:97:6c:a1:3b:1e:47:7b:a0:0c:ba:f8:bd:95 telliott@c-98-XXX-XX-154.hsd1.wv.comcast.net
    The key's randomart image is:
    
Here::

    +--[ RSA 1024]----+
    |          .      |
    |       . + o     |
    |      o + O      |
    |     . + * +     |
    |    .   S + .    |
    |   . . o * .     |
    |  . .   E        |
    |   . . .         |
    |    . o.         |
    +-----------------+

Two files are generated, ``id_rsa`` and ``id_rsa.pub``.  This is ``id_rsa.pub``::

    ssh-rsa \
    AAAAB3NzaC1yc2EAAAABIwAAAIEA+f4V6hT+EzYr+GDgMgte65vkTIDUmcnmC5Pf\
    cTJ4EE/EoA8K3XAxkNmKJUlxR02LBj2EZDd0e6w3Pzy383qpTa+nkb0rKKyA9qsO\
    NzuEvc8gV7M9eVZGItV6JSmntrid+PK64KavIabCzE1qbNns6vff/HHdw1eTeIwu\
    KseIgkM= telliott_admin@c-98-236-78-154.hsd1.wv.comcast.net

I put the ``\`` in the above to indicate that those lines wrap.  The other file is ``id_rsa``::

    -----BEGIN RSA PRIVATE KEY-----
    MIICWwIBAAKBgQD5/hXqFP4TNiv4YOAyC17rm+RMgNSZyeYLk99xMngQT8SgDwrd
    cDGQ2YolSXFHTYsGPYRkN3R7rDc/PLfzeqlNr6eRvSsorID2qw43O4S9zyBXsz15
    VkYi1XolKae2uJ348rrgpq8hpsLMTWps2ezq99/8cd3DV5N4jC4qx4iCQwIBIwKB
    gFzat663Vw5zNOc57N9jTyRP2HQv2e/6iKU27JfCSdosQbfLEqoFGbl1XzJrvFxQ
    AHAIOHz+p5umXanGGHBgwonVw5UW3r7VGnCjIrIA9dmkMrIj9WU/QNozJ2oc/XlG
    ojNzRM3wBEVbqauKPgB5k0oPBcZGy0xMVfeHTtBYt7P7AkEA/4boozRaRTyApnoS
    8LPlmf6i1cvABiGS4wMeHgcuyF42s24HoXYonRkR3Q4GIAXYSJGU9zF6aeA22BGy
    W6ZCCwJBAPp0jdxkB7NfvOrn9kg68LYjEFU/gVcTf5AgmpYxLbvthn8dc38GFut+
    dnJTAvxuN5qNoG1N3fjLzqpIR30HW6kCQQCDafP8KY2CsWa8BERBRpNWgvSod2oR
    yB+n8vmLyS4ApXs3tO37RBTjFDUSmX9+LuRClAN30E2ViUDG5Iec2SlHAkBAZx0q
    CxfsS9F+O6W6zVPXEFSoNOa+np0lD7K46BMTETE2oSxT3P6UU7gOxOOCvUF/g4EG
    Kfc/+eSvcav7lC2DAkEAuMexSyTNIf/ylyX70fAC7YLFcXd2Dm6MnM20Gms5SV/O
    5vSGq+VlvXDBL6FEj+evNnqm0pXW0WNWKAkKtYv2Zg==
    -----END RSA PRIVATE KEY-----
    
The data in these files, which consists mostly of large integers, is encoded using something called Base64 encoding.  

http://en.wikipedia.org/wiki/Base64

.. image:: /figures/base64_1.png
    :scale: 50 %

As shown in the figure base64 converts the information in three standard 8-bit bytes into four text characters.  Each segment of 3 bytes (24 bits) of input data is divided into four 6-bit chunks and in the last stage, a text character is assigned to each one based on the following table::

    'A' - 'Z'  000001 - 011001
    'a' - 'z'  011011 - 110011
    '0' - '9'  011100 - 111101
    '+'        111110
    '/'        111111

.. image:: /figures/base64_2.png
    :scale: 50 %

Although the example input data is all ASCII characters, that doesn't have to be the case.  Let's look at the first few characters of the public key data:

>>> import base64
>>> f = base64.b64decode
>>> f('AAAAB3NzaC1yc2EA')
'\x00\x00\x00\x07ssh-rsa\x00'

``b64decode`` gives us back the 8-bit bytes, except that if the byte corresponds to a printable character, we get the character instead of the hexadecimal value.  I don't know a way to turn this off.  An equally valid representation would be all hex, substituting this for the 'ssh-rsa' part:

>>> ''.join([hex(ord(c)) for c in 'ssh-rsa'])
'0x730x730x680x2d0x720x730x61'

In the above line, we turn the ASCII characters in the string back into their decimal equivalents with ``ord``, then get the hexadecimal version with ``hex``.

This kind of mixture, with hex for non-printing characters and the ASCII characters for the rest, is how Python normally handles binary data.

In order for us to make sense of the bytes, we need to know how the information has been 'packed' together, i.e. what kind of data it really is.  It's not usually just binary, but a binary version of something, for example a binary integer.  In fact, the first four bytes of the data represent the binary (32-bit) version of the unsigned integer 7::

    '\x00\x00\x00\x07ssh-rsa\x00'

They tell us that the next 7 bytes to follow represent a unit of data, in this case they are the 7 ASCII characters 'ssh-rsa'.

Let's decode some more data:

>>> f('AAABIwAAAIEA')
'\x00\x00\x01#\x00\x00\x00\x81\x00'

Together with the last byte left over from above ('0x00'), the first three bytes here are the unsigned integer 1, alerting us that the following byte stands by itself.  In ASCII encoding, this would be represented as '#', but it's actually the unsigned int 35:

>>> ord('#')
35
>>> hex(35)
'0x23'
>>> chr(35)
'#'

The integer 35 is the value of the 'exponent' for our key pair.

Finally, we get to '\x00\x00\x00\x81', this is a third unsigned int

>>> int('0x00000081',16)
129

There is one byte of padding (to a new 3-byte group for the base-64 encoding), then the following 129 bytes of data should be a single "thing".  It turns out there are only 129 bytes left in the data.  If we start just past the last 'A' above::

    +f4V6hT+EzYr+GDgMgte65vkTIDUmcnmC5PfcTJ4\
    EE/EoA8K3XAxkNmKJUlxR02LBj2EZDd0e6w3Pzy3\
    83qpTa+nkb0rKKyA9qsONzuEvc8gV7M9eVZGItV6\
    JSmntrid+PK64KavIabCzE1qbNns6vff/HHdw1eT\
    eIwuKseIgkM=

I use the ``\`` to wrap the lines around for printing here..
Just copy the whole thing (without the newline at the very end) and paste it into a string

>>> s = '+f4V6hT+EzYr+GDgMgte65vkTIDUmcnmC5PfcTJ4\
... EE/EoA8K3XAxkNmKJUlxR02LBj2EZDd0e6w3Pzy3\
... 83qpTa+nkb0rKKyA9qsONzuEvc8gV7M9eVZGItV6\
... JSmntrid+PK64KavIabCzE1qbNns6vff/HHdw1eT\
... eIwuKseIgkM='
>>> len(s)
172
>>> 3*len(s)/4
129
>>> import base64
>>> h = base64.b64decode(s)
>>> h[:10]
'\xf9\xfe\x15\xea\x14\xfe\x136+\xf8'

One way to evaluate this is to figure out how to do for a long hexadecimal string what we did above by hand, changing '\x00\x00\x00\x81' into '0x00000081'.

>>> from binascii import b2a_hex
>>> h = b2a_hex('\x00\x00\x00\x81')
>>> h
'00000081'
>>> eval('0x' + h)
129

An example with 8 bytes:

>>> h = b2a_hex('\x00\x00\x00\x81'*2)
>>> h
'0000008100000081'
>>> eval('0x' + h)
554050781313
>>> 129 + 256**4 * 129
554050781313

Let's try the same thing on our key data:

>>> s = '+f4V6hT+EzYr+GDgMgte65vkTIDUmcnmC5PfcTJ4\
... EE/EoA8K3XAxkNmKJUlxR02LBj2EZDd0e6w3Pzy3\
... 83qpTa+nkb0rKKyA9qsONzuEvc8gV7M9eVZGItV6\
... JSmntrid+PK64KavIabCzE1qbNns6vff/HHdw1eT\
... eIwuKseIgkM='
>>> import base64
>>> h = base64.b64decode(s)
>>> h[:10]
'\xf9\xfe\x15\xea\x14\xfe\x136+\xf8'
>>> from binascii import b2a_hex
>>> t = b2a_hex(h)
>>> t[:10]
'f9fe15ea14'
>>> n = eval('0x' + t)
>>> def first_last(a):
...     if len(a) < 20:
...         print a
...     else:
...         print a[:10] + '..' + a[-10:]
... 
>>> first_last(str(n))
1755507188..4104091203

A roundabout but more transparent approach is to turn this into a list of decimal numbers, using the struct module to unpack it byte by byte:

>>> from struct import unpack
>>> iL = [unpack('B',b)[0] for b in list(h)]
>>> iL[:5],iL[-5:]
([249, 254, 21, 234, 20], [42, 199, 136, 130, 67])

What we need to do is get the last int in the list (67), and put it in another list.  Then take the second to last int (130), multiply it by 256 = 33280, and save that in the second list.  Then take the the next one (136), multiply that by 256*256 = 8912896, save it, and so on.

>>> L = list()
>>> for i in range(len(iL)):
...     n = iL[-(i+1)]
...     n *= 256**i
...     L.append(n)
... 
>>> first_last(str(sum(L)))
1755507188..4104091203  

That's our public key.  How can I be so sure we've done this correctly?  There's a module called ``rsa``.

http://stuvel.eu/rsa

We can use that to look at the corresponding private key.  It also contains the public values:

>>> import rsa
>>> with open('id_rsa') as f:
...     data = f.read()
... 
>>> k = rsa.PrivateKey.load_pkcs1(data)
>>> first_last(str(k.n))
1755507188..4104091203
>>> first_last(str(k.e))
35
>>> first_last(str(k.d))
6520455273..4309851131
>>> first_last(str(k.p))
1338303424..9883079179
>>> first_last(str(k.q))
1311740788..8002182057
>>> k.p * k.q == k.n
True

You can read my introduction to public key cryptography here:

http://telliott99.blogspot.com/2011/02/secure-communications-2.html
