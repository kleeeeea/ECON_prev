# coding: utf-8

import json
import os
from operator import itemgetter
from pprint import pprint
import sys
from tqdm import tqdm
from collections import Counter
from itertools import islice
import ipdb

def read_superspan_data(inFile, num=None):
    lineCount = get_line_count(inFile)
    if num:
        MAX_PHRASES = min(lineCount, num)
    else:
        MAX_PHRASES = lineCount
    with open(inFile) as fin:
        data = []
        for line in tqdm(islice(fin, 0, MAX_PHRASES), total=MAX_PHRASES):
            # data.append(json.loads(line))
            sequence = json.loads(line)
            for d in sequence:
                if d['tag'] == 'superspan':
                    data.extend(d['spans'])
        return data

def calc_phrase_freq(data):
    freq_counter = Counter()
    for index, token in tqdm(enumerate(data)):
            # token = span['text'].lower()
            freq_counter[token] += 1
    return freq_counter


# def count_superspan_sequence(inFile, num=None):
#     cnter = Counter()
#     lineCount = get_line_count(inFile)
#     try:
#         with open(inFile) as fin:
            
#             for line in tqdm(islice(fin, 0, num), total=lineCount):
#                 data = []

#                 cnter = cnter + Counter(data)
#             return cnter
#     except Exception as e:
#         print(e)
#         ipdb.set_trace();

def get_line_count(inFile):
    count = -1
    for count, line in enumerate(open(inFile, 'r')):
        pass
    count += 1
    return count


if __name__ == '__main__':
    # dataset = sys.argv[1]
    # workspaceDir = sys.argv[2]
    # validate = True

    # workspaceDir = '/home/hanwen/disk/workspace'
    for dataset in ['machine_learning', 'pubmed', 'database']:
    # for dataset in ['machine_learning']:
        print('starting {} ...'.format(dataset))
        workspaceDir = '/scratch/home/hwzha/workspace'


        inFile = '{}/merge_span/result/{}/superspan_sequence_neat.json'.format(
            workspaceDir, dataset)
      
        data = read_superspan_data(inFile)
        freq_counter = calc_phrase_freq(data)


        outDir = '{}/merge_span/result/{}'.format(workspaceDir, dataset)
        outFile = '{}/freq_in_superspan.txt'.format(outDir)
        if not os.path.exists(outDir):
            os.makedirs(outDir)
        with open(outFile, 'w') as fout:
            for phrase, freq in freq_counter.most_common(None):
                fout.write(phrase + '\t' + str(freq))
                fout.write('\n')
        print('finishing {} ...'.format(dataset))
