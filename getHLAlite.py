#!/usr/bin/env python3
'''
demo of working with biopython and sequences from IMGT/HLA using dbfetch
'''


import sys
import os
from tempfile import NamedTemporaryFile  # part of standard libs
import requests                         # pip install requests
from Bio import SeqIO                   # pip install biopython


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


if __name__ == '__main__':
    main()
