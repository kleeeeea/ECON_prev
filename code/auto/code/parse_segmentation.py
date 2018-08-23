import sys
import json
from tqdm import tqdm
import ipdb
import re


def get_line_count(inFile):
  count = -1
  for count, line in enumerate(open(inFile, 'r')):
     pass
  count += 1
  return count

def removeMarker(text):
  # '<phrase>'
  return re.sub(pattern='<phrase>[\w ]+</phrase>', repl=lambda m:m.group(0)[8:-9], string=text)

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

def writeToJson(inFile, outFile):
  with open(inFile, 'r') as fin, open(outFile, 'w') as fout:
  # with open(inFile, 'r') as fin:
    total = get_line_count(inFile)

    cnt = 0 
    data = []
    for line in tqdm(fin, total=total):
      text = line.strip()

      tokens = text.split(' ')
      clean_tokens = removeMarker(text).split(' ')
      nps = []
      for idx, token in enumerate(tokens):
        if '<phrase>' in token:
          if token.startswith('<phrase>'):
            span = {'st':idx}
          else:
            span = {}
        elif '</phrase>' in token:
          if token.endswith('</phrase>'):
            try:
              if span:
                span['ed'] = idx + 1
                span['text'] = ' '.join(clean_tokens[span['st']:span['ed']])
                nps.append(span)
              span = {}
            except Exception as e:
              print(e)
              ipdb.set_trace()
          else:
            span = {}
      if nps:
        if not validate_nps(nps, clean_tokens):
          ipdb.set_trace()
      fout.write(json.dumps(nps))
      fout.write('\n')


      # fout.write(json.dumps(nps))
      # fout.write('\n')

if __name__ == '__main__':

    inFile = sys.argv[1]
    outFile = sys.argv[2]
    # inFile = "/scratch/home/hwzha/workspace/AutoPhrase/models/test/segmentation.txt"
    # outFile = "/scratch/home/hwzha/workspace/auto/result/test/merged.txt_without_sentence_id.json"
    writeToJson(inFile, outFile)
    
