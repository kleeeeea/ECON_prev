import spotlight
from spotlight import SpotlightException
from requests import HTTPError
import ipdb
from tqdm import tqdm
import re
import json
import os
from multiprocessing import Pool
import sys
# from pathos.multiprocessing import ProcessingPool as Pool

'''
[{'URI': 'http://dbpedia.org/resource/Indium',
  'offset': 0,
  'percentageOfSecondRank': 0.21560966948687654,
  'similarityScore': 0.8070463567236783,
  'support': 443,
  'surfaceForm': 'In',
  'types': ''}]
'''

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def get_line_count(inFile):
    count = -1
    for count, line in enumerate(open(inFile, 'r')):
        pass
    count += 1
    return count

def validate_nps(nps, tokens):
  for np in nps:
    st = np['st']
    ed = np['ed']
    token_span = tokens[st:ed]
    np_span = np['text'].split(' ')
    if token_span != np_span:
      print('token span', token_span, 'np_span', np_span)
      return False
  return True


def get_offset_to_index_dict(text):
  token_offset_to_index = {0:0}
  index = 0
  for offset, w in enumerate(text):
     if w == ' ':
         index += 1
         token_offset_to_index[offset+1] = index
  return token_offset_to_index

def dbpedia_extract_spans(line):
  validate=True
  threshold = 0.5
  text = line.strip()
  nps = []
  tokens = text.split(' ')
  try:
      token_offset_to_index = get_offset_to_index_dict(text)
      annotations = spotlight.annotate('http://localhost:2222/rest/annotate', line, confidence=threshold)
      for annotation in annotations:
        offset = annotation['offset']
        surfaceForm = annotation['surfaceForm']
        spaceNum = len(re.findall(' ', surfaceForm))
        try:
          st = token_offset_to_index[offset]
          ed = st + spaceNum + 1
          span = {'st':st, 'ed': ed, 'text': surfaceForm}
          if ' '.join(tokens[st:ed]) == surfaceForm:
            nps.append(span)
        except KeyError as e:
          pass
      if validate:
        
        if not validate_nps(nps, tokens):
          pass
          # ipdb.set_trace();
  except (SpotlightException, HTTPError) as e:
    pass
  except Exception as e:
    print(e)
    # ipdb.set_trace();
  return nps


def writeToJson(inFile, prevOutFile, outFile, validate=False):
  lineCount = get_line_count(inFile)
  # with open(inFile) as fin:
  #   texts = [line for line in fin]

  with open(inFile) as fin, open(prevOutFile) as f_prev, open(outFile, 'w') as fout:
      # p = Pool(10)
      for line, prev_lines in tqdm(zip(fin,f_prev), total=lineCount):
      # for lines in tqdm(batch(texts, 10)):
          prev_nps = json.loads(prev_lines)
          if prev_nps:
            nps = prev_nps
          else:
            nps = dbpedia_extract_spans(line)
          # nps_pool = p.map(dbpedia_extract_spans, lines)
          # for nps in nps_pool:
          fout.write(json.dumps(nps))
          fout.write('\n')

if __name__ == '__main__':
  inFile = sys.argv[1]
  prevOutFile = sys.argv[2]
  outFile = sys.argv[3]
  # for dataset in ['test', 'JMLR', 'nips', 'pubmed', 'database']:
  # dataset = 'JMLR'
  # print("start generating {} json file".format(dataset))
  # workspaceDir="/scratch/home/hwzha/workspace"
  # inFile = '{}/../data/{}/merged.txt_without_sentence_id'.format(workspaceDir, dataset)
  # outFile = '{}/dbpedia/result/{}/merged.txt_without_sentence_id.json'.format(workspaceDir, dataset)
  # outDir = '{}/dbpedia/result/{}'.format(workspaceDir, dataset)
  # if not os.path.exists(outDir):
  #     os.makedirs(outDir)

  writeToJson(inFile, prevOutFile, outFile, True)
  # print("finish generating {} json file".format(dataset))
