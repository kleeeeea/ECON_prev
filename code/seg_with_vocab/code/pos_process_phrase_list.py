from collections import Counter
from tqdm import tqdm
import spacy
from spacy.tokens import Doc
import ipdb;
from multiprocessing import Pool
from functools import partial
import sys
from itertools import islice

try:
  unicode;
except Exception as e:
  unicode = str;

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

def get_line_count(inFile):
    count = -1
    for count, line in enumerate(open(inFile, 'r')):
        pass
    count += 1
    return count

def pos_filter(text):
  # ipdb.set_trace();
  tokens = text.split(' ')
  doc = nlp(text)
  # if 'we' in text:
  #   ipdb.set_trace();
  # pos_list = [None] * len(tokens)
  # for index, token in enumerate(doc):
  #     pos_list[index] = token.pos_
  # if pos_list[-1] in ['NOUN', 'PROPN']:
  if doc and doc[-1].pos_ in ['NOUN', 'PROPN']:
      return True
  else:
     return False

def pos_process_phrase_list(method, dataset):
  inFile = '/scratch/home/hwzha/workspace/{}/result/{}/phrase_list.txt'.format(method, dataset)
  outFile = '/scratch/home/hwzha/workspace/{}/result/{}/phrase_list_noun.txt'.format(method, dataset)
  cnt_dict = {}
  # print('method is {} ...'.format(method))
  lineCount = get_line_count(inFile)

  print('start process {}/{} ...'.format(method, dataset))
  with open(inFile) as fin:
    MAX_PHRASE = min(lineCount, 700000)
    for line in tqdm(fin, total=MAX_PHRASE):
      phrase, freq = line.strip().split('\t')
      if pos_filter(phrase):
        try:
          cnt_dict[phrase] = int(freq)
        except Exception as e:
          cnt_dict[phrase] = float(freq)

    cnter = Counter(cnt_dict)

    with open(outFile, 'w') as fout:
      for p in cnter.most_common(None):
        phrase, freq = p
        fout.write(phrase + '\t' + str(freq) + '\n')
    print('finish process {}/{} ...'.format(method, dataset))



if __name__ == '__main__':
  method = sys.argv[1]
  dataset = sys.argv[2]
  # method = 'spacy_np'

  # for method in ['dbpedia', 'spacy_entity', 'spacy_np', 'StructMineDataPipeline', 'textrank', 'kea','auto', 'rake']:
  # for method in ['spacy_np']:
    # for dataset in ['machine_learning', 'pubmed', 'database']:
  pos_process_phrase_list(method, dataset)
