import re
import json
from operator import itemgetter
from tqdm import tqdm
import ipdb
import sys

def get_line_count(inFile):
    count = -1
    for count, line in enumerate(open(inFile, 'r')):
        pass
    count += 1
    return count

def validate_output(text, origin_text):
  if not text.replace('_', ' ') == origin_text.replace('_', ' '):
    ipdb.set_trace();

def generate_sequence(spans, tokens):
    '''
        generate evaluation sequence
    '''
    try:
      flag = [-1]*len(tokens)

      sequence = []
      for i, span in enumerate(spans):
          st = span['st']
          ed = span['ed']
          for idx in range(st, ed):
              if flag[idx] == -1:
                  flag[idx] = i
              else:
                break

      occur = set()
      for index, span_index in enumerate(flag):
          if span_index == -1:
              sequence.append(tokens[index])
          else:
              if span_index not in occur:
                  span = spans[span_index]
                  span_text = '<c>' + '_'.join(tokens[span['st']:span['ed']]) + '</c>'
                  # span_text = '_'.join(tokens[span['st']:span['ed']])
                  sequence.append(span_text)
                  occur.add(span_index)
    except Exception as e:
      print(e)
      ipdb.set_trace();

    return sequence


if __name__ == '__main__':
    # inFile = sys.argv[1]
    # outFile = sys.argv[2]
    # textFile = sys.argv[3]

    # workspaceDir = '/scratch/home/hwzha/workspace'
    # dataset = 'test'
    # method = 'textrank'
    dataset = sys.argv[1]
    method = sys.argv[2]
    workspaceDir = sys.argv[3]

    if method == 'dbpedia':
      inFile = '{}/{}/result/{}/merged.txt_without_sentence_id2.json'.format(
          workspaceDir, method, dataset)
    else:
      inFile = '{}/{}/result/{}/merged.txt_without_sentence_id.json'.format(
          workspaceDir, method, dataset)
    outFile = '{}/{}/result/{}/merged.txt_without_sentence_id.evaluation.txt'.format(
        workspaceDir, method, dataset)
    textFile = '{}/../data/{}/merged.txt_without_sentence_id'.format(
        workspaceDir, dataset)

    lineCount = get_line_count(textFile)

    with open(inFile) as fin, open(textFile) as f_text, open(outFile, 'w') as fout:
        for i, data in enumerate(tqdm(zip(fin, f_text), total=lineCount)):
            line_spans, text = data
            text = text.strip()
            if text:
              tokens = text.split(' ')
              spans = json.loads(line_spans)
              spans = sorted(spans, key= lambda span: (span['st'], -span['ed']))
              output_tokens = generate_sequence(spans, tokens)
              output_text = ' '.join(output_tokens)
              # validate_output(output_text, text)
              fout.write(output_text)
            fout.write('\n')
