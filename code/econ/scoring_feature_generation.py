import sys
from gensim.models import word2vec, Word2Vec
import numpy as np
import re
import cPickle
from conceptMining.embedding.embedding import display_concept, re_concept_tagged, normalize_concept
import logging
logging.basicConfig(level=logging.DEBUG)


dataset = 'machine_learning'

dataset2BASIC_THRESHOLD = {
    'pubmed': .5,
    'database': .3,
    'machine_learning': .5,
}
BASIC_THRESHOLD = dataset2BASIC_THRESHOLD[dataset]

dataset2restrict_vocab = {
    'pubmed': 100000,
    'database': 50000,
    'machine_learning': 200000,
}
restrict_vocab = dataset2restrict_vocab[dataset]

dataset2TOPN = {
    'pubmed': 20,
    'database': 20,
    'machine_learning': 20,
}
TOPN = dataset2TOPN[dataset]


if len(sys.argv) > 1:
    dataset = sys.argv[1]

model_post_fix = ''
if len(sys.argv) > 2:
    dataset = sys.argv[2]

model_save_path = './data/%s/embedding_tmp.bin%s' % (dataset, model_post_fix)
# syn0norm_path = './data/%s/syn0norm.bin' % dataset
concept_feature_path = './data/%s/concept_feature.txt%s' % (dataset, model_post_fix)
concept_score_path = './data/%s/concept_score.txt' % dataset


# try:
#     syn0norm = cPickle.load('./data/%s/syn0norm.bin')
# except Exception as e:
#     model.init_sims()
#     cPickle.dump(model.wv.syn0norm, open('./data/%s/syn0norm.bin'))

# def gpu():
#     import torch
#     model.init_sims()
#     syn0norm_targets = model.wv.syn0norm[target_concept_index_set]
#     with torch.cuda.device(1):
#         t = torch.Tensor(model.wv.syn0norm).cuda()
#         r = torch.mm(t[:1000], torch.t(t))


model = Word2Vec.load(model_save_path)

index2word_normalize_conceptd = [normalize_concept(w) for w in model.wv.index2word]
index2word_normalize_conceptd_reverse = {w: i for i, w in enumerate(index2word_normalize_conceptd)}

re_nonASCII = re.compile(r'[^\x00-\x7F]+')
wiki_concept_set = set()
# load target_word_set
for l in open('/scratch/home/hwzha/workspace/AutoPhrase/data/EN/wiki_quality.txt'):
    concept = l.strip()
    if not re_nonASCII.search(l):
        wiki_concept_set.add(normalize_concept(concept).replace(' ', '_'))

dbpedia_concept_set = set()
for l in open("/scratch/home/hwzha/workspace/%s/result/%s/phrase_list.txt" % ('dbpedia', dataset)):
    concept, score = l.strip().split('\t')
    if len(concept.split(' ')) > 1 or concept.isupper():
        dbpedia_concept_set.add(normalize_concept(concept).replace(' ', '_'))

target_concept_set = wiki_concept_set | dbpedia_concept_set

# try:
#     from gensim.similarities.index import AnnoyIndexer
#     model.init_sims()
#     annoy_index = AnnoyIndexer(model, 100)
#     indexer = annoy_index
# except Exception as e:
#     indexer = None
target_concept_index_set = sorted([index2word_normalize_conceptd_reverse[w] for w in target_concept_set & set(index2word_normalize_conceptd)])


concept_feature_dict = {}


def computeFeatures(concept, model):

    neighbor_word2sim = {normalize_concept(w): sim for w, sim in model.most_similar(concept, topn=TOPN, restrict_vocab=restrict_vocab, partition_only=True) if sim > BASIC_THRESHOLD}
    if len(neighbor_word2sim) < 2:
        return np.array([0, 0, 0, 0])

    # Meaningfulness: no. neighbors
    meaningfulness = len(neighbor_word2sim)
    # Purity:avg. similarity

    purity = np.mean(neighbor_word2sim.values())

    # Targetness:no. known words
    targetness = len(set(neighbor_word2sim.keys()) & target_concept_set)
    # {normalize_concept(w): sim for w, sim in model.most_similar(concept, topn=3, limited_index=target_concept_index_set) if sim > BASIC_THRESHOLD}
    # len(set(neighbor_word2sim.keys()) & target_concept_set)c

    completeness = -len([w for w in neighbor_word2sim.keys() if normalize_concept(concept) in w])
    # contained_by_set = [w for w in index2word_normalize_conceptd if w.endswith(normalize_concept(concept))]
    # contained_by_index_set = [index2word_normalize_conceptd_reverse[w] for w in contained_by_set]
    # # Completeness:do not have phrase that contains it
    # completeness = {normalize_concept(w): sim for w, sim in model.most_similar(concept, topn=3, limited_index=contained_by_index_set) if sim > BASIC_THRESHOLD}

    return np.array([meaningfulness, purity, targetness, completeness])


def process():
    with open(concept_feature_path, 'w') as f_out:
        for i, w in enumerate(model.wv.index2word):
            if i % 1000 == 0:
                logging.debug('%sth concept' % i)
            if re_concept_tagged.match(w):
                concept_feature_dict[w] = computeFeatures(w, model)
                f_out.write('%s\t%s\n' % (display_concept(w), concept_feature_dict[w]))

    cPickle.dump(concept_feature_dict, open('data/%s/concept_feature_dict.bin' % dataset, 'w'))

    # concept_feature_matrx = np.array([concept_feature_dict[w] for w in model.wv.index2word])

if __name__ == '__main__':
    process()
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.svm import SVC
# from sklearn.linear_model import SGDClassifier, LogisticRegression

# C = 1.0

# Y = [1, 0, 1]
# Y_index = [2, 4, 5]

# classifiers = {'L1 logistic': LogisticRegression(C=C, penalty='l1'),
#                'L2 logistic (OvR)': LogisticRegression(C=C, penalty='l2'),
#                'Linear SVC': SVC(kernel='linear', C=C, probability=True,
#                                  random_state=0),
#                'RandomForest': RandomForestClassifier(max_depth=2, random_state=0),
#                }

# for k, v in classifiers.items():
#     clf = classifiers[k]
#     clf.fit(X[Y_index], Y)

#     concept_score_matrix = clf.predict(X)
#     print concept_score_matrix
#     with open(concept_score_path, 'w') as f_out:
#         for i, w in enumerate(model.wv.index2word):
#             f_out.write('%s\t%s' % (w, concept_score_matrix[i]))

#     # feature normalization?
