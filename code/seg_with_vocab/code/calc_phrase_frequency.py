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


def read_span_json(inFile, num=None):
    with open(inFile) as fin:
        data = []
        for line in islice(fin, 0, num):
            data.append(json.loads(line))
        return data

def get_line_count(inFile):
    count = -1
    for count, line in enumerate(open(inFile, 'r')):
        pass
    count += 1
    return count


def calc_phrase_freq(data, islower=True):
    try:
        freq_counter = Counter()
        for index, spans in tqdm(enumerate(data), total=len(data)):
            for span in spans:
                if islower:
                    token = span['text'].lower()
                else:
                    token = span['text']
                freq_counter[token] += 1
        return freq_counter
    except Exception as e:
        print(e)
        ipdb.set_trace();

if __name__ == '__main__':
    dataset = sys.argv[1]
    # workspaceDir = sys.argv[2]
    # validate = True

    # workspaceDir = '/home/hanwen/disk/workspace'
    # dataset = 'test'
    workspaceDir = '/scratch/home/hwzha/workspace'

    textFile = '{}/../data/{}/merged.txt_without_sentence_id'.format(
        workspaceDir, dataset)
    nltkFile = '{}/StructMineDataPipeline/result/{}/merged.txt_without_sentence_id.json'.format(
        workspaceDir, dataset)
    spacyFile = '{}/spacy/result/{}/merged.txt_without_sentence_id.json'.format(
        workspaceDir, dataset)
    spacyNPFile = '{}/spacy_np/result/{}/merged.txt_without_sentence_id.json'.format(
        workspaceDir, dataset)
    spacyEntityFile = '{}/spacy_entity/result/{}/merged.txt_without_sentence_id.json'.format(
        workspaceDir, dataset)
    dbpediaFile = '{}/dbpedia/result/{}/merged.txt_without_sentence_id2.json'.format(
        workspaceDir, dataset)
  

    nltkData = read_span_json(nltkFile)
    # spacyData = read_span_json(spacyFile)
    spacyNPData = read_span_json(spacyNPFile)
    spacyEntityData = read_span_json(spacyEntityFile)
    dbpediaData = read_span_json(dbpediaFile)


    # convert spacy data
    # spacyNPData = []
    # spacyEntityData = []
    # for d in spacyData:
    #     spacyNPData.append(d['np'])
    #     spacyEntityData.append(d['entity'])

    for method, data in zip(['StructMineDataPipeline', 'spacy_entity', 'spacy_np', 'dbpedia'], [nltkData, spacyEntityData, spacyNPData, dbpediaData]):
    # for method, data in zip(['dbpedia'], [dbpediaData]):
        outDir = '{}/{}/result/{}'.format(workspaceDir, method, dataset)
        outFile = '{}/phrase_list.txt'.format(outDir)
        outFile_without_lower = '{}/phrase_list_without_lower.txt'.format(outDir)
        if not os.path.exists(outDir):
            os.makedirs(outDir)
        with open(outFile, 'w') as fout:
            freq_counter = calc_phrase_freq(data, islower=True)
            for phrase, freq in freq_counter.most_common(None):
                fout.write(phrase + '\t' + str(freq))
                fout.write('\n')

        with open(outFile_without_lower, 'w') as fout:
            freq_counter = calc_phrase_freq(data, islower=False)
            for phrase, freq in freq_counter.most_common(None):
                fout.write(phrase + '\t' + str(freq))
                fout.write('\n')