#!/usr/bin/env python3
'''
demo of working with sequences from IMGT/HLA using dbfetch
'''


import sys
import os
from tempfile import NamedTemporaryFile  # part of standard libs
import requests                         # pip install requests
from Bio import SeqIO                   # pip install biopython
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC
from Bio.SeqRecord import SeqRecord


def getHLA(acc):
    '''
    takes an accession ID and returns the sequence record from IMGT/HLA
    '''
    url = ('https://www.ebi.ac.uk/Tools/dbfetch/dbfetch?db=imgthla;id=' +
           acc + ';style=raw'
           )
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
    # create a temp file to hold the sequence record
    f = NamedTemporaryFile(mode='w+', delete=False)
    f.write(response.text)
    f.close()
    # read the dbfetch result into a sequence object
    mySeq = SeqIO.read(f.name, "imgt")
    os.unlink(f.name)
    return mySeq


def getFeatures(seqobj, kind):
    '''
    takes a sequence object and a kind of feature
    returns a list of those features
    '''
    exons = []
    for feature in seqobj.features:
        if feature.type == kind:
            exons.append(feature)
    return exons


def getExon(seqobj, num):
    '''
    takes a sequence object with exon features,
    returns another sequence object of only that exon
    '''
    exons = getFeatures(seqobj, 'exon')
    for exon in exons:
        for key, values in exon.qualifiers.items():
            if key == 'number':
                for value in values:
                    if value == str(num):
                        start = exon.location.start
                        end = exon.location.end
                        print('start = {}'.format(start))
                        print('end = {}'.format(end))
    exonSeq = SeqRecord(Seq(str(seqobj.seq[start:end]), IUPAC.ambiguous_dna),
                        id='{}, exon {}'.format(seqobj.id, num),
                        name='{}, exon {}'.format(seqobj.name, num),
                        description=("{}, exon {}, start={}, end={}".format(
                            seqobj.description, num, start, end))
                        )
    return exonSeq


def main():
    """
    do the main thing
    """
    mySeq = getHLA('HLA00001')
    print('id = {}'.format(mySeq.id))
    print('description = {}'.format(mySeq.description))
    print('len = {}'.format(len(mySeq)))
    subSeq = mySeq.seq[0:10]
    print('1st ten nucleotides = {}'.format(subSeq))
    exon2 = getExon(mySeq, '2')
    print(exon2)


if __name__ == '__main__':
    main()
