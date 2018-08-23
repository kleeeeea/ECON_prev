import json
import sys
from util.common import flatten
from smart_open import smart_open
import itertools
from util.common import removeNonLetter
from gensim.models import word2vec, Word2Vec
import datetime
import random
import spacy
import logging
import re
import timeit
import gensim

logging.basicConfig(level=logging.DEBUG)

INITIAL = True
WINDOW_SIZE = 5
ITER = int(5)
# int(3e4) required for one sentence to converge..
VALIDATION_SIZE = 20
REMOVE_CAPITAL = False
ONLY_ENDS_WITH = True
# nlp = spacy.load('en')

dataset = 'test'

if len(sys.argv) > 1:
    dataset = sys.argv[1]

    # parentdir = './data/%s/txt_tokenized/' % dataset
    # outputFile = './data/%s/merged.txt'

supersequence_path = "/scratch/home/hwzha/workspace/merge_span/result/%s/superspan_sequence_neat.json" % dataset
concept_representation_path = './data/%s/concept_representation.txt' % dataset

model_save_path = './data/%s/embedding_tmp.bin' % dataset
if REMOVE_CAPITAL:
    model_save_path += 'REMOVE_CAPITAL'
if ONLY_ENDS_WITH:
    supersequence_path = '/scratch/home/hwzha/workspace/merge_span/result/%s/superspan_sequence_neat_without_non_tail.json' % dataset
    model_save_path += '_ONLY_ENDS_WITH.bin'
# file = "/scratch/home/hwzha/workspace/merge_span/result/test/superspan_sequence_neat.json"


def any2unicode(text, encoding='utf8', errors='strict'):
    """Convert a string (bytestring in `encoding` or unicode), to unicode."""
    if isinstance(text, unicode):
        return text
    return unicode(text, encoding, errors=errors)
to_unicode = any2unicode


class LineSentenceAsWordPair(object):
    """
    Simple format: one sentence = one line; words already preprocessed and separated by whitespace.
    """
    def __init__(self, source, limit=None):
        self.source = source
        self.limit = limit

    def __iter__(self):
        with smart_open(self.source) as fin:
            for line in itertools.islice(fin, self.limit):
                sentence = to_unicode(line).split()
                i = 0
                for i in range(len(sentence)):
                    for j in range(i + 1, min(i + WINDOW_SIZE + 1, len(sentence))):
                        # pairs_of_words.append([sentence[i], sentence[j]])
                        yield [sentence[i], sentence[j]]


def normalizeTextualUnit(raw_textual_unit, lemmatize=False):
    try:
        if lemmatize:
            doc = nlp(raw_textual_unit)
            return '_'.join([w.lemma_ for w in doc])

        # todo: remove capital case
        if REMOVE_CAPITAL:
            if not raw_textual_unit.istitle():
                raw_textual_unit = raw_textual_unit.lower()
        return raw_textual_unit.replace(' ', '_')
    except Exception as e:
        import ipdb; ipdb.set_trace()
        raise e


def to_concepts(w):
    return '<phrase>%s</phrase>' % w.replace(' ', '_')


def getRawSpans(superspan):
    try:
        if superspan['tag'] == 'superspan':
            return ['<c>%s</c>' % concept for concept in superspan['spans']]
        else:
            return superspan['spans']
        # try=======6345-09=====xt']]
        pass
    except Exception as e:
        import ipdb; ipdb.set_trace()

def getNormalizedTextualUnits(superspan):
    textual_units_raw = getRawSpans(superspan)
    textual_units_normalized = [normalizeTextualUnit(raw_textual_unit) for raw_textual_unit in textual_units_raw]

    # if ONLY_ENDS_WITH:
    #     return [span for span in textual_units_normalized if normalize_concept(superspan['text']).endswith(normalize_concept(span).split('_')[-1])]
        #
    return textual_units_normalized


def getNormalizedTextualUnits_preprocess(superspan):
    textual_units_raw = getRawSpans(superspan)
    textual_units_normalized = [normalizeTextualUnit(raw_textual_unit) for raw_textual_unit in textual_units_raw]

    if ONLY_ENDS_WITH:
        return [span for span in textual_units_normalized if normalize_concept(superspan['text']).endswith(normalize_concept(span).split('_')[-1])]
        #
    return textual_units_normalized


def get_cleaned_superspan_sequence(superspan_sequence):
    superspan_sequence_removed_letters = [superspan for superspan in superspan_sequence if removeNonLetter(superspan['text'])]
    # if ONLY_ENDS_WITH:
    #     superspan_sequence_removed_letters_removed_nonEndingSpan = None

    return superspan_sequence_removed_letters


class LineSuperWordSequenceAsWordPair(object):
    """
    Simple format: one sentence = one line; words already preprocessed and separated by whitespace.
    """

    def __init__(self, source, limit=None):
        self.source = source
        self.limit = limit

    def __iter__(self):
        with smart_open(self.source) as fin:
            for line in itertools.islice(fin, self.limit):
                superspan_sequence = get_cleaned_superspan_sequence(json.loads(line))
                for i in range(len(superspan_sequence)):
                    for j in range(i + 1, min(i + WINDOW_SIZE + 1, len(superspan_sequence))):
                        for span_i in getNormalizedTextualUnits(superspan_sequence[i]):
                            for span_j in getNormalizedTextualUnits(superspan_sequence[j]):
                                yield [span_i, span_j]


def trim_rule(word, count, min_count):
    if re_concept_tagged.match(word):
        return gensim.utils.RULE_KEEP
    return gensim.utils.RULE_DEFAULT

re_concept_tagged = re.compile(
    r"<c>(?P<phrase>[^<]*)</c>"
)


def display_concept(w):
    # return w
    return re.sub(r'</?c>', '', w)

def normalize_concept(w):
    return display_concept(w.lower())


def validate_model(model, model_save_path='', include_score=True):
    valid_window = min(100, len(model.wv.index2word))
    validation_size = min(VALIDATION_SIZE, len(model.wv.index2word))
    top_k = 10

    # if not model_save_path:
    #     model_save_path = '/tmp/model_%s' % datetime.datetime.now()
    # model.save(model_save_path)

    print(model.wv.index2word[:100])

    valid_examples_frequent = random.sample(model.wv.index2word, validation_size / 2)
    valid_examples_phrase = random.sample([word for word in model.wv.index2word if '_' in word], validation_size / 2)

    try:
        model['analysis']
        valid_examples_frequent[0] = 'analysis'
        model['machine_learning']
        valid_examples_phrase[0] = 'machine_learning'
    except Exception, e:
        pass

    for valid_word in valid_examples_frequent + valid_examples_phrase:
        print 'valid word %s' % display_concept(valid_word)
        if include_score:
            print '%s' % [(display_concept(word), score) for word, score in model.most_similar(valid_word)]
        else:
            print '%s' % [display_concept(word) for word, score in model.most_similar(valid_word)]


if __name__ == '__main__':
    start = timeit.default_timer()

    if INITIAL:
        file = supersequence_path
        model = Word2Vec(LineSuperWordSequenceAsWordPair(file), min_count=30, window=WINDOW_SIZE, sg=1, iter=ITER, workers=32, hs=1, negative=0, trim_rule=trim_rule)
    else:
        file = concept_representation_path
        model = Word2Vec(word2vec.LineSentence(file), min_count=5, window=WINDOW_SIZE, sg=1, iter=ITER, workers=32, hs=1, negative=0)

    # Your statements here
    stop = timeit.default_timer()

    print stop - start
    model.save(model_save_path)

    new_model = Word2Vec.load(model_save_path)
    validate_model(new_model)
