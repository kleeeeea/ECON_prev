import sys
import spacy
import json
from tqdm import tqdm
import ipdb
from spacy.tokens import Doc

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


nlp = spacy.load('en')
nlp.tokenizer = WhitespaceTokenizer(nlp.vocab)

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

def writeToJson(inFile, outFile, validate=False):
  global nlp
  with open(inFile, 'r') as fin, open(outFile, 'w') as fout:
    total = get_line_count(inFile)

    for line in tqdm(fin, total=total):
      text = unicode(line).strip('\r\n')

      if text:
        # text may be empty when line is \n
        doc = nlp(text)

        entities = []
        for ent in doc.ents:
          entity = {'st':ent.start, 'ed':ent.end, 'label': ent.label_, 'text':ent.text}
          entities.append(entity)
              
        nps = []
        for np in doc.noun_chunks:
          nounphrase = {'st':np.start, 'ed':np.end, 'text':np.text}
          nps.append(nounphrase)

        if validate:
          tokens = text.split(' ')
          if not validate_nps(entities, tokens):
            import ipdb; ipdb.set_trace();
          if not validate_nps(nps, tokens):
            import ipdb; ipdb.set_trace();
      else:
        nps = []
        entities = []

      fout.write(json.dumps({'entity':entities, 'np':nps}))
      fout.write('\n')

if __name__ == '__main__':


  inFile = sys.argv[1]
  outFile = sys.argv[2]
  writeToJson(inFile, outFile, False)
