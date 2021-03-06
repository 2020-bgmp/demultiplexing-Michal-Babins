#!/usr/bin/env python

from itertools import permutations
import gzip

import argparse
#Argparse takes in arguments that are callable when running the code.

def args():
        parser=argparse.ArgumentParser(description = "Demultiplexing code")
        parser.add_argument("-file1", help="R1", required = True, type = str)
        parser.add_argument("-file2", help="R2", required = True, type = str)
        parser.add_argument("-file3", help="R3", required = True, type = str)
        parser.add_argument("-file4", help="R4", required = True, type = str)
        parser.add_argument("-index", help="index", required = True, type = str)
        return parser.parse_args()
args = args()#Set args as parser for callables


# file1 = '/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz'
# file2 = '/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz'
# file3 = '/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz' 
# file4 = '/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz'
file1 = args.file1
file2 = args.file2
file3 = args.file3
file4 = args.file4
index = args.index

def rev_comp(sequence):
    ''' Take the compliment and reverse postion, will be used for index 2'''
    rev_seq = {'A' : 'T', 'T' : 'A', 'G' : 'C', 'C' : 'G', 'N' : 'N'}
    rev = ''
    for char in sequence:
        char = rev_seq[char] 
        rev = char + rev
    return rev

def convert_phred(letter):
    '''Conver the q scores to numerical integers. Will be used to assess cut off score'''
    for i in letter:
       con =  ord(i) - 33
    return con

def iter_lines(file):
    ''' Pull the needed lines out of the file'''
    seq = file.readline().strip()
    plus = file.readline().strip()
    qual_s = file.readline().strip()
    return seq, plus, qual_s


def add_index(r1_read, seq2, seq3, r4_read):
    ''' Add seq2 and seq to the headers to get dual matched headers '''
    index = seq2 + '-' + seq3
    r1_head = r1_read + index 
    r4_head = r4_read + index
    return r1_head, r4_head

def permutation(index):
    ''' Create permuations list for reference'''
    with open(index, 'r') as index_list:
        index_list.readline()
        index_l = []
        perm_dict = {}
        for line in index_list:
            line.strip()
            split_list = line.split()
            index_l.append(split_list[4])
        perm = permutations(index_l, 2)
    for i in perm:
        perm_dict[i] = 0
    return perm_dict



def fill_index_to_filehandles_map(index):
    '''populate index_to_file_handles dict with index as keys, 2tuple fh as value. '''
    with open(index, 'r') as index_list:
        index_list.readline()
        index_to_filehandles_map = {}
        for line in index_list:
            line = line.strip()
            split_list = line.split()
            index1 = split_list[4]
            forward_index_fh =  open('./Read1{}.fastq'.format(index1), 'w')
            reverse_index_fh = open('./Read4{}.fastq'.format(index1), 'w')
            index_to_filehandles_map[index1] = (forward_index_fh, reverse_index_fh)
    return index_to_filehandles_map


def demultiplex(file1, file2, file3, file4, index_list):
    '''Main function that will open files, refence made functions, and match conditions to write out to files.'''
    errorR1 = open('output'+ 'errorR1.fastq','w')
    errorR4 = open('output' + 'errorR4.fastq', 'w')
    hoppedfileR1 = open('output' + 'hoppedR1.fastq', 'w')
    hoppedfileR4 = open('output' + 'hoppedR2.fastq','w')
    stats = open('output' + 'stats.txt', 'w')
    perm_dict = permutation(index_list)
    #key:index sequence, value: 2tuple:(out_i1, out_i2) outfiles for forward and reverse read respectively
    index_to_filehandles_map = fill_index_to_filehandles_map(index)
    counter_index = {}
    count_swapped = 0
    count_error = 0
    total_paired = 0
    total_output = 0
    index_l = []
    perm_dict = {}
    paired_read1 = {}
    paired_read2 = {}
    with gzip.open(file1, 'rt') as fh, gzip.open(file2, 'rt') as fh2, gzip.open(file3, 'rt') as fh3, gzip.open(file4, 'rt') as fh4:
        for r1_read, r2_read, r3_read, r4_read in zip(fh, fh2, fh3, fh4):
            seq1, plus1, qual_s1 = iter_lines(fh)
            seq2, plus2, qual_s2 = iter_lines(fh2)
            seq3, plus3, qual_s3 = iter_lines(fh3)
            seq4, plus4, qual_s4 = iter_lines(fh4)
            seq3 = rev_comp(seq3)
            add_index(r1_read, seq2, seq3, r4_read)
            qual_conR2 = convert_phred(qual_s2)
            qual_conR3 = convert_phred(qual_s3)
            if qual_conR2 < 20 or qual_conR3 < 20:
                errorR1.write(r1_read + '\n' + seq1 + '\n' + plus1 + '\n' + qual_s1 + '\n')
                errorR4.write(r4_read + '\n' + seq4 + '\n' + plus4 + '\n' + qual_s4 + '\n')
                count_error += 1
            elif seq2 not in index_to_filehandles_map:
                errorR1.write(r1_read + '\n' + seq1 + '\n' + plus1 + '\n' + qual_s1 + '\n')
                errorR4.write(r4_read + '\n' + seq4 + '\n' + plus4 + '\n' + qual_s4 + '\n')
                count_error +=1
            elif seq2 == seq3:
                (forward_index_fh, reverse_index_fh) = index_to_filehandles_map[seq2]
                forward_index_fh.write(r1_read + '\n' + seq1 + '\n' + plus1 + '\n' + qual_s1 + '\n')
                reverse_index_fh.write(r4_read + '\n' + seq4 + '\n' + plus4 + '\n' + qual_s4 + '\n')
                total_paired += 1
            elif seq2 != seq3:
                hoppedfileR1.write(r1_read + '\n' + seq1 + '\n' + plus1 + '\n' + qual_s1 + '\n')
                hoppedfileR4.write(r4_read + '\n' + seq4 + '\n' + plus4 + '\n' + qual_s4 + '\n')
                count_swapped += 1
            elif seq2 or seq3 in perm_dict:
                errorR1.write(r1_read + '\n' + seq1 + '\n' + plus1 + '\n' + qual_s1 + '\n')
                errorR4.write(r4_read + '\n' + seq4 + '\n' + plus4 + '\n' + qual_s4 + '\n')
                count_error += 1
        total_output = count_error + total_paired+ count_swapped
        mappedR = (total_paired/total_output) * 100
        stats.write(str(count_swapped) + '\n' + str(count_error) + '\n' + '\n' + str(total_output) + '\n' + str(mappedR) + '%')
    fh.close()
    fh2.close()
    fh3.close() 
    fh3.close()


demultiplex(file1, file2, file3, file4, index)