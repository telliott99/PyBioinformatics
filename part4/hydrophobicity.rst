.. _hydrophobicity:

##############
Hydrophobicity
##############

We're going to do a plot invented by Jack Kyte and Russ Doolittle

http://telliott99.blogspot.com/2010/03/kyte-doolittle-hydrophobicity-plot-in.html

I got the data for the MalG protein from Genbank (*Salmonella typhimurium*)::

    >gi|47775|emb|CAA38191.1| malG [Salmonella enterica ..
    MAMVQPKSQKLRLLITHLGLLIFIAAIMFPLLMVI
    AISLREGNFATGSLIPDKISWEHWRLALGFSVEHA
    DGRVTPPPFPVLLWLWNSVKIAGITAIGIVALSTT
    CAYAFARMRFPGKATLLKGMLIFQMFPAVLSLVAL
    YALFDRLGQYIPFIGLNTHGGVIFAYLGGIALHVW
    TIKGYFETIDSSLEEAAALDGATPWQAFRLVLLPL
    SVPILAVVFILSFIAAITEVPVASLLLRDVDSYTL
    AVGMQQYLNPQNYLWGDFAAAAVLSAIPITLVFLL
    AQRWLVNGLTAGGVKG


.. sourcecode:: python

    import matplotlib.pyplot as plt
    import numpy as np
    import utils

    s = '''
    A   1.8 C   2.5 D  -3.5 E  -3.5
    F   2.8 G  -0.4 H  -3.2 I   4.5
    K  -3.9 L   3.8 M   1.9 N  -3.5
    P  -1.6 Q  -3.5 R  -4.5 S  -0.8
    T  -0.7 V   4.2 W  -0.9 Y  -1.3'''

    D = dict()
    L = s.strip().split()
    while L:
        k,v = L.pop(0),L.pop(0)
        D[k] = float(v)
    print D
    
    data = utils.load_data('MalG.aa.txt')
    title,seq = data.strip().split('\n',1)
    prot = ''.join(seq.split())
    #-------------------------

    window = 15
    delta = 2
    rL = list()
    for i in range(0,len(prot)-window+1,delta):
        pep = prot[i:i+window]
        L = [D[aa] for aa in pep]
        rL.append((i, pep, sum(L)))

    for e in rL:
        if e[2] > 20:  print e
    X = np.arange(len(rL)) * delta
    Y = [e[2] for e in rL]

    plt.scatter(X,Y,s=40,color='r',zorder=2)
    plt.plot(X,Y,'--',lw=1.5,color='k',zorder=1)
    ax = plt.axes()
    ax.set_xlim(-10,len(prot))
    plt.savefig('MalG.png')
    
In the first half of the script, we organize the hydrophobicity data into a dictionary, then read the MalG sequence from a file.  Organizing the plot in the second half is pretty simple.  We just slide a window along the sequence and sum the values for those amino acids.  We print a few segments just to look at::

    (10, 'LRLLITHLGLLIFIA', 32.100000000000001)
    (12, 'LLITHLGLLIFIAAI', 39.099999999999994)
    (14, 'ITHLGLLIFIAAIMF', 36.199999999999996)
    (16, 'HLGLLIFIAAIMFPL', 34.599999999999994)
    (18, 'GLLIFIAAIMFPLLM', 39.699999999999996)
    (20, 'LIFIAAIMFPLLMVI', 45.0). . .

Here is the image:

.. image:: /figures/MalG.png
   :scale: 50 %

