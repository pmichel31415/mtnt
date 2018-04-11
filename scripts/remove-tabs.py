import sys
from src.util import loadtxt, savetxt

in_file = sys.argv[1]
out_file = sys.argv[2]
n_fields = int(sys.argv[3])

tsv = loadtxt(in_file)
for i, l in enumerate(tsv):
    fields = l.split('\t')
    while len(fields) > n_fields:
        fields = ['%s %s' % (fields[0], fields[1])] + fields[2:]
    tsv[i] = '\t'.join(fields)
savetxt(out_file, tsv)
