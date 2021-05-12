#!/usr/bin/env python3

"""
Filter pacbio reads with contigous repeat at their start or end and trim telomeric repeats.
This script relies on the high fidelity and strandedness of PacBio HiFi reads.
The strongest assumption is that the forward motif will only occur on the right
end of the reads, while the reverse complement of the motif can only
occur on the left side.

Usage:
        filter_telomeric_reads.py [--string STR] [--times INT]
                                  [--out FILE] [--lacking FILE]
                                  [--min_len INT]

options:
    -s STR, --string STR     telomeric repeat
                            [Default: TTAGGC]
    --times INT             minimum number of contiguous occurrences.
                            [Default: 3]
    -m INT, --min_len INT   Minimum length of trimmed read
                            [Default: 100]
    -o FILE, --out FILE     filename for telomeric reads.
                            [Default: telomericReads.fasta]
    -l FILE, --lacking FILE filename for non-telomeric reads.
"""


from trim import readfq, reverse_complement_sequence, trim_seq

import sys
from docopt import docopt

from memory_profiler import profile

@profile

if __name__ == "__main__":
    args                = docopt(__doc__)
    outfile             = args['--out']
    nontelomfile        = args['--lacking']
    motif               = args['--string']
    min_len             = int(args['--min_len'])
    rev_motif           = reverse_complement_sequence(motif)
    motif_size          = len(motif)
    min_occur           = int(args['--times'])
    write_non_telomeric = bool(nontelomfile)
    non_telomeric_reads = ''
    telomeric_reads     = ''
    seq_in_mem_len      = 0

    for name, seq, qual in readfq(sys.stdin):
        trimmed_sequence = trim_seq(seq, min_occur, motif_size, motif, rev_motif)
        trimmed_len = len(trimmed_sequence)
        if trimmed_len > min_len:
            telomeric_reads += ">%s\n" % name
            telomeric_reads += "%s\n" % trimmed_sequence
            seq_in_mem_len += trimmed_len
            if seq_in_mem_len > 100000:
                with open(outfile, 'a') as ofh:
                    ofh.writelines(telomeric_reads)
                telomeric_reads = ''
                seq_in_mem_len = 0
        elif write_non_telomeric & trimmed_len == 0:
            non_telomeric_reads += ">%s\n" % name
            non_telomeric_reads += "%s\n" % seq

                
    
    if write_non_telomeric:
        with open(nontelomfile, 'w') as nofh:
            nofh.writelines(non_telomeric_reads)