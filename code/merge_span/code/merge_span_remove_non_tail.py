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

# def read_span_json(inFile, num=None):
#     with open(inFile) as fin:
#         for line in islice(fin, 0, num):
#             yield(json.loads(line))


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


def generate_superspan(d, tokens):
    cur_super_st = -1
    cur_super_ed = -1
    superspan_cnt = -1
    superspan = {}
    superspan_list = []
    for span in sorted(d, key=itemgetter('st', 'ed')):
        # span information
        st = span['st']
        ed = span['ed']
        text = span['text']
        source = span['source']
#         print('text', text)

        if st >= cur_super_ed:
            # meet a new superspan
            cur_super_st = st
            cur_super_ed = ed
            superspan = {'super_st': cur_super_st,
                         'super_ed': cur_super_ed, 'spans': []}
            span = {'st': st, 'ed': ed, 'text': text, 'source': source}
            if span not in superspan['spans']:
                superspan['spans'].append(span)
#             superspan['text'] = ' '.join(tokens[cur_super_st:cur_super_ed])
            superspan['tag'] = 'superspan'
            superspan_list.append(superspan)
            superspan_cnt += 1
        else:
            # update super end pos
            if ed > cur_super_ed:
                cur_super_ed = ed
            superspan_list[superspan_cnt]['super_ed'] = cur_super_ed
            span = {'st': st, 'ed': ed, 'text': text, 'source': source}
            if span not in superspan_list[superspan_cnt]['spans']:
                superspan_list[superspan_cnt]['spans'].append(
                    span)
#             superspan_list[superspan_cnt]['text'] = ' '.join(tokens[cur_super_st:cur_super_ed])
    for i, superspan in enumerate(superspan_list):
        superspan_list[i]['text'] = ' '.join(
            tokens[superspan['super_st']:superspan['super_ed']])
    return superspan_list


def generate_sequence(superspan_list, tokens, validate=False):
    '''
        generate super span sequence
    '''
    flag = [-1]*len(tokens)

    sequence = []
    for i, superspan in enumerate(superspan_list):
        st = superspan['super_st']
        ed = superspan['super_ed']
        for idx in range(st, ed):
            flag[idx] = i

    occur = set()
    for index, superspan_index in enumerate(flag):
        if superspan_index == -1:
            sequence.append({'tag': 'plain', 'text': tokens[index]})
        else:
            if superspan_index not in occur:
                sequence.append(superspan_list[superspan_index])
                occur.add(superspan_index)

    return sequence


def remove_non_tail_span(superspan_list):
    try:
        new_superspan_list = []
        for superspan in superspan_list:
            new_span = []
            for span in  superspan['spans']:
                if span['ed'] == superspan['super_ed']:
                    new_span.append(span)
            superspan['spans'] = new_span
            new_superspan_list.append(superspan)
    except Exception as e:
        print(e)
        ipdb.set_trace();
    return new_superspan_list



def validate_sequence(superspan_sequence, tokens, span_list):
    # import ipdb; ipdb.set_trace();
    concatenate_tokens = []
    span_set_in_superspan = set()
    for superspan in superspan_sequence:
        if superspan['tag'] == 'superspan':
            superspan_tokens = tokens[
                superspan['super_st']:superspan['super_ed']]
            assert superspan['text'] == ' '.join(superspan_tokens)
            concatenate_tokens.extend(superspan_tokens)
            for span in superspan['spans']:
                span_set_in_superspan.add(
                    (span['st'], span['ed'], span['text']))
        else:
            concatenate_tokens.append(superspan['text'])
    assert concatenate_tokens == tokens

    span_set = set()
    for span in span_list:
        span_set.add((span['st'], span['ed'], span['text']))
    if span_set_in_superspan != span_set:
        import ipdb
        ipdb.set_trace()
        print(span_set_in_superspan)
        print(span_set)


if __name__ == '__main__':

    dataset = sys.argv[1]
    workspaceDir = sys.argv[2]
    validate = True

    # workspaceDir = '/home/hanwen/disk/workspace'
    # dataset = 'test'

    textFile = '{}/../data/{}/merged.txt_without_sentence_id'.format(
        workspaceDir, dataset)

    merge_data_filteredFile = '{}/merge_span/result/{}/merge_data_filtered.json'.format(workspaceDir, dataset)

    print('start loading {} span json data ...'.format(dataset))
    mergeData = read_span_json(merge_data_filteredFile)

    texts = read_text(textFile)

    print('finish loading {} span json data ...'.format(dataset))

    new_data = mergeData

    # ipdb.set_trace();

    outDir = '{}/merge_span/result/{}'.format(workspaceDir, dataset)
    outListFile = '{}/superspan_list_without_non_tail.json'.format(outDir)
    outFile = '{}/superspan_sequence_without_non_tail.json'.format(outDir)

    if not os.path.exists(outDir):
        os.makedirs(outDir)

    print('start generating superspan ...')
    with open(outListFile, 'w') as fout_list, open(outFile, 'w') as fout:
        lineCount = get_line_count(textFile)
        for slice_num in tqdm(range(lineCount)):
            text = texts[slice_num].strip()
            if text:
                tokens = text.split(' ')
            else:
                tokens = []

            superspan_list = generate_superspan(new_data[slice_num], tokens)
            superspan_list = remove_non_tail_span(superspan_list)

            fout_list.write(json.dumps(superspan_list))
            fout_list.write('\n')

            superspan_sequence = generate_sequence(
                superspan_list, tokens, True)
            # if validate:
            #     validate_sequence(superspan_sequence, tokens,
            #                       new_data[slice_num])

            fout.write(json.dumps(superspan_sequence))
            fout.write('\n')
