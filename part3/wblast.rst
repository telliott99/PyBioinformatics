.. _wblast:

#########
Web BLAST
#########

Here is an example for how to run a BLAST search at NCBI using a Python script, but rolling your own PUT and GET requests.  It uses a the ``RequestLimiter`` class from BioPython.

.. sourcecode:: python

    import time
    class RequestLimiter:
        # This class implements a simple countdown timer for delaying WWW
        # requests.
        def __init__(self, delay):
            self.last_time = 0.0
            self.delay = delay
        def wait(self, delay=None):
            if delay is None:
                delay = self.delay
            how_long = self.last_time + delay - time.time()
            if how_long > 0:
                time.sleep(how_long)
            self.last_time = time.time()

.. sourcecode:: python

    import urllib, urllib2, time, RequestLimiter
    from utils import load_data
    blast = "http://www.ncbi.nlm.nih.gov/blast/Blast.cgi"

    def init():
        data = load_data('achromo.mod.txt')
        data = data.strip().split('\n\n')
        return data[0].strip()

    def build_put(seq,v=False):
        print 'blastq', seq[:40]
        seq = seq.strip()
        program = 'blastn'
        database = 'nr'
        query = [('DATABASE',database),
                ('PROGRAM',program),
                ('QUERY',seq),
                ('CMD', 'Put')  ]
        msg = urllib.urlencode(query)
        request = urllib2.Request(blast,
                msg)
        if v:
              print 'PUT request'
              print 'query',
              for t in query:
                  if t[0] == 'QUERY':
                      print t[0], t[1][:50]
              print 'message',msg[:50]
              print 'url',request.get_full_url()
              print 'method',request.get_method()
              print 'data',request.get_data()[:50]
        return request

    def send_put(request):
        # Send off the initial query to qblast.
        start = time.time()
        handle = urllib2.urlopen(request)
        # get the rid we'll use later
        rid = handle.read().split("RID =")[1].split("\n")[0]
        print 'rid', rid
        return start, rid

    def build_get(rid):
        query = [ ('RID',rid), ('CMD', 'Get'),
                ('FORMAT_TYPE','XML')]
        # why use urllib here?
        message = urllib.urlencode(query)
        request = urllib2.Request(blast, message)
        return request

    def get_results(request,start,v=False):
        limiter = RequestLimiter.RequestLimiter(10)
        while True:
            print '%3.1f' % (time.time() - start), 'seconds'
            limiter.wait()
            # take a look
            if v:
                    print 'GET request'
                    print 'query',query
                    print 'message',message
                    print 'url',request.get_full_url()
                    print 'method',request.get_method()
                    print 'data',request.get_data()
                    print

            handle = urllib2.urlopen(request)
            results = handle.read()
            # XML results don't have the Status tag when finished
            # doesn't seem to work unless we ask for XML
            if results.find("Status=") < 0:
                break
            else:
                if v:
                    print results
                    print
        return results

    def save(results):
        FH = open('results.xml','w')
        FH.write(results)
        FH.close()

    def doit():
        fasta_seq = init()
        request1 = build_put(fasta_seq,v=True)
        start, rid = send_put(request1)
        request2 = build_get(rid)
        results = get_results(request2,start)
        save(results)

    if __name__ == '__main__':
        doit()

The data file is from:

Here is the output::

    > python script.py
    blastq >Ax1
    AGTTTGATCCTGGCTCAGATTGAACGCTAGCGGGA
    PUT request
    query QUERY >Ax1
    AGTTTGATCCTGGCTCAGATTGAACGCTAGCGGGATGCCTTACAC
    message DATABASE=nr&PROGRAM=blastn&QUERY=%3EAx1%0AAGTTTGAT
    url http://www.ncbi.nlm.nih.gov/blast/Blast.cgi
    method POST
    data DATABASE=nr&PROGRAM=blastn&QUERY=%3EAx1%0AAGTTTGAT
    rid  6PTSCME1011
    1.7 seconds
    2.5 seconds
    12.3 seconds
    22.8 seconds
    32.3 seconds
    46.1 seconds
    52.6 seconds
    62.9 seconds
    73.0 seconds

You should have a file ``results.xml`` on the Desktop.  We won't do it, but the parsing code is :ref:`here <markup>`.

We'll look at other ways to do this later.