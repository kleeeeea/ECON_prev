# coding: utf-8

import json
import os
from operator import itemgetter
from pprint import pprint
import sys
from tqdm import tqdm
import spacy
from spacy.tokens import Doc
from itertools import islice
import ipdb
from collections import Counter

try:
    unicode
except NameError as e:
    unicode = str


class WhitespaceTokenizer(object):

    def __init__(self, vocab):
        self.vocab = vocab

    def __call__(self, text):
        words = text.split(' ')
        # All tokens 'own' a subsequent space character in this tokenizer
        spaces = [True] * len(words)
        return Doc(self.vocab, words=words, spaces=spaces)

nlp = spacy.load('en', disable=['ner', 'parser'])
nlp.tokenizer = WhitespaceTokenizer(nlp.vocab)


def read_span_json(inFile, num=None):
    with open(inFile) as fin:
        data = []
        for line in islice(fin, 0, num):
            data.append(json.loads(line))
        return data

def read_text(inFile, num=None):
    with open(inFile) as fin:
        texts = []
        for line in islice(fin, 0, num):
            texts.append(line)
        return texts


def get_line_count(inFile):
    count = -1
    for count, line in enumerate(open(inFile, 'r')):
        pass
    count += 1
    return count


def check_span_data(inFile_list):
    length_list = [get_line_count(inFile) for inFile in inFile_list]
    assert len(set(length_list)) == 1
    if len(set(length_list)) != 1:
        for length in length_list:
            print(length)


def add_span_to_spans(span, spans):
    exisits = False
    for i, s in enumerate(spans):
        if s['st'] == span['st'] and s['ed'] == span['ed'] and s['text'] == span['text']:
            source = set(spans[i]['source'].split(', '))
            source.add(span['source'])
            spans[i]['source'] = ','.join(list(source))
            # spans[i]['source'] = spans[i]['source'] + ',' + span['source']
            exisits = True
            break
    if not exisits:
        spans.append(span)


def merge_span_data(data_list, source_list):
    # check data length consistency
    length_list = [len(data) for data in data_list]
    print(length_list)
    assert len(set(length_list)) == 1
    length = length_list[0]
    new_data = []
    for i in tqdm(range(length)):
        new_d = []
        for j, data in enumerate(data_list):
            # new_d.extend(data[i])
            for span in data[i]:
                neat_span = {'st': span['st'], 'ed': span[
                    'ed'], 'text': span['text'], 'source': source_list[j]}
                # if neat_span not in new_d:
                #     new_d.append(neat_span)
                # print(new_d)
                add_span_to_spans(neat_span, new_d)
                # print(new_d)
                # print('--'*20)
        new_data.append(new_d)
    return new_data

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
    workspaceDir = sys.argv[2]
    validate = True

    # workspaceDir = '/home/hanwen/disk/workspace'
    # dataset = 'test'

    textFile = '{}/../data/{}/merged.txt_without_sentence_id'.format(
        workspaceDir, dataset)
    nltkFile = '{}/StructMineDataPipeline/result/{}/merged.txt_without_sentence_id.json'.format(
        workspaceDir, dataset)
    # spacyFile = '{}/spacy/result/{}/merged.txt_without_sentence_id.json'.format(
    #     workspaceDir, dataset)
    spacyNPFile = '{}/spacy_np/result/{}/merged.txt_without_sentence_id.json'.format(
        workspaceDir, dataset)
    spacyEntityFile = '{}/spacy_entity/result/{}/merged.txt_without_sentence_id.json'.format(
        workspaceDir, dataset)
    autoFile = '{}/auto/result/{}/merged.txt_without_sentence_id.json'.format(
        workspaceDir, dataset)
    textrankFile = '{}/textrank/result/{}/merged.txt_without_sentence_id.json'.format(
        workspaceDir, dataset)
    rakeFile = '{}/rake/result/{}/merged.txt_without_sentence_id.json'.format(
        workspaceDir, dataset)
    keaFile = '{}/kea/result/{}/merged.txt_without_sentence_id.json'.format(
        workspaceDir, dataset)
    dbpediaFile = '{}/dbpedia/result/{}/merged.txt_without_sentence_id2.json'.format(
        workspaceDir, dataset)

    check_span_data([nltkFile, spacyNPFile, spacyEntityFile,
                     autoFile, textrankFile, keaFile, dbpediaFile])

    print('start loading {} span json data ...'.format(dataset))
    nltkData = read_span_json(nltkFile)
    # spacyData = read_span_json(spacyFile)
    spacyNPData = read_span_json(spacyNPFile)
    spacyEntityData = read_span_json(spacyEntityFile)
    autoData = read_span_json(autoFile)
    textrankData = read_span_json(textrankFile)
    keaData = read_span_json(keaFile)
    dbpediaData = read_span_json(dbpediaFile)

    texts = read_text(textFile)

    # convert spacy data
    # spacyNPData = []
    # spacyEntityData = []
    # for d in spacyData:
    #     spacyNPData.append(d['np'])
    #     spacyEntityData.append(d['entity'])

    print('finish loading {} span json data ...'.format(dataset))

    # print('start filtering grammar ...')
    # nltkData = filter_span_data_by_grammar(nltkData, texts)
    # spacyNPData = filter_span_data_by_grammar(spacyNPData, texts)
    # spacyEntityData = filter_span_data_by_grammar(spacyEntityData, texts)
    # autoData = filter_span_data_by_grammar(autoData, texts)
    # textrankData =filter_span_data_by_grammar(textrankData, texts)
    # keaData = filter_span_data_by_grammar(keaData, texts)
    # dbpediaData = filter_span_data_by_grammar(dbpediaData, texts)
    # print('finish filtering grammar ...')

    print('start merging {} data ...'.format(dataset))
    new_data = merge_span_data(
        [nltkData, spacyNPData, spacyEntityData,
            autoData, textrankData, keaData, dbpediaData],
        # [nltkFile, spacyNPFile, spacyEntityFile, autoFile, textrankFile, keaFile, dbpediaFile],
        ['nltk', 'spacy_np', 'spacy_entity', 'auto', 'textrank', 'kea', 'dbpedia'])
    print('finish merging {} data ...'.format(dataset))

    print('start counting {} ...'.format(dataset))
    freq_counter = calc_phrase_freq(new_data)
    print('finish counting {} ...'.format(dataset))

    outDir = '{}/merge_span/result/{}'.format(workspaceDir, dataset)
    outFile = '{}/freq_in_superspab_without_filter.txt'.format(outDir)

    if not os.path.exists(outDir):
        os.makedirs(outDir)

    with open(outFile, 'w') as fout:
        for phrase, freq in freq_counter.most_common(None):
            fout.write(phrase + '\t' + str(freq))
            fout.write('\n')

