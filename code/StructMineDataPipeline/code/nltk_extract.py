import sys
import nltk
import json
from tqdm import tqdm
import ipdb


def get_nps(tree, tokens):
    nps = []
    st = 0
    for subtree in tree:
        if isinstance(subtree, nltk.tree.Tree):
            if subtree.label() == 'NP':
                np = subtree.leaves()
                ed = st + len(np)
                nps.append({'np': np, 'st': st, 'ed': ed,
                            'text': ' '.join(tokens[st:ed])})
            st += len(subtree.leaves())
        else:
            st += 1
    return nps


def validate_nps(nps, tokens):
    for np in nps:
        st = np['st']
        ed = np['ed']
        token_span = tokens[st:ed]
        np_span = [tup[0] for tup in np['np']]
        if token_span != np_span:
            print(token_span, np_span)
            return False
    return True


def writeToJson(inFile, outFile, validate=False):

    grammar = r"""
   NP:
      {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
  """


  #   r"""
  #  NBAR:
  #     {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
  #  NP:
  #     {<NBAR>}
  #     {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
  # """

    cp = nltk.RegexpParser(grammar)  # chunk parser
    with open(inFile, 'r') as fin, open(outFile, 'w') as fout:
        for line in tqdm(fin):
            doc = line.strip('\r\n')
            if doc:
                tokens = doc.split(' ')
                parse_tree = cp.parse(nltk.pos_tag(tokens))

                nps = get_nps(parse_tree, tokens)
                if validate:
                    if not validate_nps(nps, tokens):
                        import ipdb
                        ipdb.set_trace()
            else:
                nps = []

            fout.write(json.dumps(nps))
            fout.write('\n')

if __name__ == '__main__':
    inFile = sys.argv[1]
    outFile = sys.argv[2]
    writeToJson(inFile, outFile)
