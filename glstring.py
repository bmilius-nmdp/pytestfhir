#!/usr/bin/env python3
"""
glstring.py

functions for getting loci, alleles, allele lists, genotypes, genotype lists
and locus blocks from a GL String

also contains class for GlString with methods to do the above.
"""

import re


class GlString:
    """
    common base class for GL Strings
    """

    def __init__(self, gls, ver):
        self.gls = gls
        self.ver = ver

    def __repr__(self):
        return("GlString('{}', '{}')".format(self.gls, self.ver))

    def loci(self):
        """
        Takes GlString, and returns a set containing all the loci
        """
        alleles = get_alleles(self.gls)
        loci = set()
        for allele in alleles:
            loci.add(allele.split('*')[0])
        return loci

    def alleles(self):
        """
        Takes a GlString, and returns a set of all the alleles
        """
        alleles = set()
        for allele in re.split(r'[/~+|^]', self.gls):
            alleles.add(GlString(allele, self.ver))
        return alleles

    def allele_lists(self):
        """
        Takes a GlString, and returns a list of allele lists it contains
        """
        allele_lists = []
        for block in re.split(r'[~+|^]', self.gls):
            if "/" in block:
                allele_lists.append(GlString(block, self.ver))
        return allele_lists

    def genotypes(self):
        """
        Take a GlString, and return a list of genotypes
        """
        genotypes = []
        for block in re.split(r'[|^]', self.gls):
            if "+" in block:
                genotypes.append(GlString(block, self.ver))
        return genotypes

    def genotype_lists(self):
        """
        Take a GlString, and return a list of genotype lists
        """
        genotype_lists = []
        for block in self.gls.split('^'):
            if "|" in block:
                genotype_lists.append(GlString(block, self.ver))
        return genotype_lists

    def locus_blocks(self):
        """
        Take a GlString, and return a list of locus blocks
        """
        locus_blocks = []
        for locus_block in self.gls.split('^'):
            locus_blocks.append(GlString(locus_block, self.ver))
        return locus_blocks

    def genotype_blocks(self):
        """
        Take a GL String as str, return a list of blocks that make up all
        genotypes found
        """
        genotypes = self.genotypes()
        genotype_blocks = []
        for genotype in genotypes:
            for block in genotype.gls.split('+'):
                genotype_blocks.append(GlString(block, self.ver))
        return genotype_blocks

    def genotype_list_blocks(self):
        """
        Take a GL String as str, return a list of blocks that make up all
        genotype lists found
        """
        genotype_lists = self.genotype_lists()
        genotype_list_blocks = []
        for genotype_list in genotype_lists:
            for block in genotype_list.gls.split('|'):
                genotype_list_blocks.append(GlString(block, self.ver))
        return genotype_list_blocks

    def haplotypes(self):
        """
        Takes a GlString, and returns a list of phased alleles it contains
        """
        haplotypes = []
        for block in re.split(r'[+|^]', self.gls):
            if "~" in block:
                haplotypes.append(GlString(block, self.ver))
        return haplotypes


def get_loci(glstr):
    """
    Takes GL String as a str, and returns a set containing all the loci

    :type glstr: string
    :param glstr: GL String
    """
    alleles = get_alleles(glstr)
    loci = set()
    for allele in alleles:
        loci.add(allele.split('*')[0])
    return loci


def get_alleles(glstr):
    """
    Takes a GL String as a str, and returns a set containing all the alleles
    """
    alleles = set()
    for allele in re.split(r'[/~+|^]', glstr):
        alleles.add(allele)
    return alleles


def get_allele_lists(glstr):
    """
    Takes a GL String as a str and returns a list of allele lists it contains
    """
    allele_lists = []
    for block in re.split(r'[~+|^]', glstr):
        if "/" in block:
            allele_lists.append(block)
    return allele_lists


def get_genotypes(glstr):
    """
    Take a GL String as a str, and return a list of genotypes
    """
    genotypes = []
    for block in re.split(r'[|^]', glstr):
        if "+" in block:
            genotypes.append(block)
    return genotypes


def get_genotype_lists(glstr):
    """
    Take a GL String as a str, and return a list of genotype lists
    """
    genotype_lists = []
    for block in glstr.split('^'):
        if "|" in block:
            genotype_lists.append(block)
    return genotype_lists


def get_genotype_blocks(glstr):
    """
    Take a GL String as str, return a list of blocks that make up all
    genotypes found
    """
    genotypes = get_genotypes(glstr)
    genotype_blocks = []
    for genotype in genotypes:
        for block in genotype.split('+'):
            genotype_blocks.append(block)
    return genotype_blocks


def get_genotype_list_blocks(glstr):
    """
    Take a GL String as str, return a list of blocks that make up all
    genotype lists found
    """
    genotype_lists = get_genotype_lists(glstr)
    genotype_list_blocks = []
    for genotype_list in genotype_lists:
        for block in genotype_list.split('|'):
            genotype_list_blocks.append(block)
    return genotype_list_blocks


def get_locus_blocks(glstr):
    """
    Take a GL String as str, and return a list of locus blocks
    """
    return glstr.split('^')


def get_haplotypes(glstr):
    """
    Takes a GL String as a str and returns a list of phased alleles it contains
    """
    haplotypes = []
    for block in re.split(r'[+|^]', glstr):
        if "~" in block:
            haplotypes.append(block)
    return haplotypes


def main():
    pass


if __name__ == '__main__':
    main()
