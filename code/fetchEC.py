from cogent.db.ncbi import EUtils
from cogent.parse.genbank import RichGenbankParser

def fetch_seq(gid,gb_fn):
    e = EUtils(db="nucleotide", rettype="gb")
    outfile = open(gb_fn,'w')
    outfile.write(e[gid].read())
    outfile.close()

def get_cds(gb_fn):
    FH = open(gb_fn,'r')
    parser = RichGenbankParser(FH)
    accession, seq = [record for record in parser][0]
    def gene_and_cds(f):
        return f['type'] == 'CDS' and 'gene' in f
    return [f for f in seq.Info.features if gene_and_cds(f)]

def get_locations(cL):
    for cds in (cL):
        print cds['gene'][0].ljust(6),
        loc = cds['location']
        print int(loc.first()) - 1, int(loc.last()) - 1,
        if loc.strand() == 1:
            print 'cw'
        else:
            print 'ccw'

if __name__ == '__main__':
    gid = 'U00096.2'
    gb_fn = 'seq.gb'
    #fetch_seq(gid,gb_fn)
    L = get_cds(gb_fn)
    get_locations(L)
