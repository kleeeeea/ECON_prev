import cPickle
from gensim.models import word2vec
from gensim import corpora, models, similarities
import sys
import logging


INITIALIZE = True

logging.basicConfig(level=logging.DEBUG)

# dataset = 'machine_learning'

if len(sys.argv) > 2:
    dataset = sys.argv[1]
    approach = sys.argv[2]

# APPROACHES = ['kea', 'rake']


def index(file_pureText):
    with open(file_pureText) as f:
        lines = f.readlines()

    logging.debug('processing %s' % file_pureText)
    try:
        if INITIALIZE:
            raise Exception
        corpus = corpora.MmCorpus(file_pureText + '.corpus')
        dictionary = corpora.Dictionary.load(file_pureText + '.dict')
        modelTfidf = models.TfidfModel.load(file_pureText + '.modelTfidf')
    except Exception, e:
        print 'using new model'
        wordsLists = [line.lower().split() for line in lines]
        dictionary = corpora.Dictionary(wordsLists)
        corpus = [dictionary.doc2bow(text) for text in wordsLists]
        modelTfidf = models.TfidfModel(corpus)

        dictionary.save(file_pureText + '.dict')  # store the dictionary, for future reference
        corpora.MmCorpus.serialize(file_pureText + '.corpus', corpus)  # store to disk, for later use
        corpus = corpora.MmCorpus(file_pureText+'.corpus')
        modelTfidf.save(file_pureText+'.modelTfidf')

    try:
        if INITIALIZE:
            raise Exception
        index = cPickle.load(open(file_pureText+'.index', 'rb'))
    except Exception as e:
        print 'using new index'
        modelTfidfCorpus = modelTfidf[corpus]
        index = similarities.Similarity(file_pureText+'.modelTfidfindex', modelTfidfCorpus, num_features=modelTfidfCorpus.corpus.num_terms)
        index.num_best = None
        cPickle.dump(index, open(file_pureText+'.index', 'wb'))

def process(dataset, approach):
    file_pureText = "/scratch/home/hwzha/workspace/%s/result/%s/merged.txt_without_sentence_id.evaluation.txt" % (approach, dataset)
    try:
        index(file_pureText)
    except Exception as e:
        print e

# for dataset in ['database', 'machine_learning']:
# for approach in APPROACHES:
process(dataset, approach)