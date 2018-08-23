import sys
import spacy
import json
from tqdm import tqdm
# import ipdb
from spacy.tokens import Doc

from spacy.matcher import PhraseMatcher

try:
  unicode;
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


nlp = spacy.load('en', disable=['ner', 'parser', 'tagger'])
nlp.tokenizer = WhitespaceTokenizer(nlp.vocab)


def read_phrase_list(inFile, threshold=0.5):
  # unified phrase file format
  # input is already ranked and cut off
  # runtime complexity \t 0.7805276116 
  with open(inFile, 'r') as fin:
    phrase_list = []
    for line in fin:
        phrase = line.split('\t')[0].strip()
        score = float(line.split('\t')[1])
        if score < threshold:
          break
        phrase_list.append(phrase)
    return phrase_list


def writeToJson(inFile, outFile, matcher, validate=False):
  global nlp
  total = get_line_count(inFile)
  with open(inFile, 'r') as fin, open(outFile, 'w') as fout:

    for line in tqdm(fin, total=total):
      text = unicode(line).strip('\r\n')
      tokens = text.split(' ')

      if text:
        # text may be empty when line is \n
        doc = nlp(text.lower())
        matches = matcher(doc)
        '''
        matches:
        [(1826470356240629538, 0, 1),
         (4451351154198579052, 0, 2),
         (7342778914265824300, 1, 2),
         (3411606890003347522, 2, 3)]
        '''
        nps = []
        for m in matches:
          st = m[1]
          ed = m[2]
          np = {'st':st, 'ed':ed, 'text': ' '.join(tokens[st:ed])}
          nps.append(np)
      else:
        nps = []

      if validate:
        if not validate_nps(nps, tokens):
          import ipdb; ipdb.set_trace();

      fout.write(json.dumps(nps))
      fout.write('\n')

if __name__ == '__main__':

  try:
    inFile = sys.argv[1]
    outFile = sys.argv[2]
    phraseinFile = sys.argv[3]
    threshold = float(sys.argv[4])
    validate = True
  except Exception as e:
    # for test
    print(e)
    workspaceDir = '/home/hanwen/disk/workspace'
    dataset = 'test'
    method = 'auto'
    inFile = '{workspaceDir}/../data/{dataset}/merged.txt_without_sentence_id'.format(workspaceDir=workspaceDir, dataset=dataset)
    phraseinFile = '{workspaceDir}/{method}/result/{dataset}/phrase_list.txt'.format(workspaceDir=workspaceDir, method=method, dataset=dataset)
    outFile = '{workspaceDir}/{method}/result/{dataset}/merged.txt_without_sentence_id.json'.format(workspaceDir=workspaceDir, method=method, dataset=dataset)
    validate = True
    threshold = '0.1'

  # if not threshold
  #   threshold = 0.0


  with open(phraseinFile, 'r') as fin:
      phrase_list = read_phrase_list(phraseinFile, threshold)


  matcher = PhraseMatcher(nlp.vocab)
  for v in phrase_list:
    matcher.add(v, None, nlp(unicode(v))) # python3 is unicode

  writeToJson(inFile, outFile, matcher, validate=validate)

