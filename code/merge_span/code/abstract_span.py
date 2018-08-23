# coding: utf-8

import json
import os
from operator import itemgetter
from pprint import pprint
import sys
from tqdm import tqdm

def get_line_count(inFile):
    count = -1
    for count, line in enumerate(open(inFile, 'r')):
        pass
    count += 1
    return count

def read_span_json(inFile, num=None):
    with open(inFile) as fin:
        data = []
        if num:
            for i, line in enumerate(fin):
                data.append(json.loads(line))
                if i >= num:
                    break
        else:
            for line in fin:
                data.append(json.loads(line))
        return data

def neat_span_json(superspan_sequence):
    superspan_sequence_neat = []
    for superspan in superspan_sequence:
        if superspan['tag'] == 'superspan':
            spans = [v['text'] for v in superspan['spans']]
            neat_supersan = {'tag':'superspan', 'text':superspan['text'], 'spans':spans}
            superspan_sequence_neat.append(neat_supersan)
        else:
            superspan.update({'spans':[superspan['text']]})
            superspan_sequence_neat.append(superspan)
    return superspan_sequence_neat


if __name__ == '__main__':

    dataset = sys.argv[1]
    workspaceDir = sys.argv[2]

    # workspaceDir = '/home/hanwen/disk/workspace'
    # dataset = 'test'

    outDir = '{}/merge_span/result/{}'.format(workspaceDir, dataset)
    outListFile = '{}/superspan_list.json'.format(outDir)
    inFile = '{}/superspan_sequence.json'.format(outDir)
    outFile = '{}/superspan_sequence_neat.json'.format(outDir)

    try:
        with open(outFile, 'w') as fout:
            lineCount = get_line_count(inFile)
            data = read_span_json(inFile)
            for v in tqdm(data):
                superspan_sequence = neat_span_json(v)
                fout.write(json.dumps(superspan_sequence))
                fout.write('\n')
    except Exception as e:
        print(e)

