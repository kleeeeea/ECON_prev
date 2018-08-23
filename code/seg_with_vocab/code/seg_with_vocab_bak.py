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


def read_autophrase_list(inFile):
  with open(inFile, 'r') as fin:
    phrase_list = []
    for line in fin:
            phrase_list.append(line.split('\t')[1].strip())
    return phrase_list

def read_rake_list(inFile):
  with open(inFile, 'r') as fin:
    phrase_list = []
    for line in fin:
            phrase_list.append(line.strip())
    return phrase_list

def read_textrank_list(inFile):
  with open(inFile, 'r') as fin:
    phrase_list = []
    for line in fin:
            phrase_list.append(line.split('\t')[0].strip())
    return phrase_list

def read_phrase_list(method, inFile):
  if method == 'autophrase':
    return read_autophrase_list(inFile)
  elif method == 'rake':
    return read_rake_list(inFile)
  elif method == 'textrank':
    return read_textrank_list(inFile)
  else:
    return


def writeToJson(inFile, outFile, matcher, validate=False):
  global nlp
  with open(inFile, 'r') as fin, open(outFile, 'w') as fout:
    total = get_line_count(inFile)

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
          np = {'st':st, 'ed':ed, 'np':tokens[st:ed], 'text': ' '.join(tokens[st:ed])}
          nps.append(np)
      else:
        nps = []

      if validate:
        if not validate_nps(nps, tokens):
          import ipdb; ipdb.set_trace();

      fout.write(json.dumps(nps))
      fout.write('\n')

if __name__ == '__main__':


  inFile = sys.argv[1]
  outFile = sys.argv[2]
  dataset = sys.argv[3] 
  # # nips
 
  # writeToJson(inFile, outFile, False)

  workspaceDir = '/home/hanwen/disk/workspace'
  # inFile = '/home/hanwen/disk/data/test/merged.txt_without_sentence_id'
  # outFile = '{}/seg_with_vocab/result/test/merged.txt_without_sentence_id.json'.format(workspaceDir)
  # dataset = 'nips'

  phrase_list = []
  for method in ['textrank', 'autophrase', 'rake']:
    if method == 'autophrase':
      phraseinFile = '{workspaceDir}/AutoPhrase/models/{dataset}/AutoPhrase.txt'.format(workspaceDir=workspaceDir, dataset=dataset)
    else:
      phraseinFile = '{workspaceDir}/{method}/{dataset}_{method}_term.txt'.format(workspaceDir=workspaceDir, method=method, dataset=dataset)
    with open(phraseinFile, 'r') as fin:
      phrase_list.extend(read_phrase_list(method, phraseinFile))


  phrase_set = set(phrase_list)

  # max phrase len = 6
  phrase_set = set([v for v in phrase_set if len(v.split(' ')) <= 6 ])

  # create phrase matcher
  matcher = PhraseMatcher(nlp.vocab)
  for v in phrase_set:
    matcher.add(v, None, nlp(unicode(v))) # python3 is unicode

  writeToJson(inFile, outFile, matcher, validate=True)



