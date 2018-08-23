import json
import sys
from gensim.models import word2vec, Word2Vec
import numpy as np
from conceptMining.embedding.embedding import get_cleaned_superspan_sequence, WINDOW_SIZE, getNormalizedTextualUnits, re_concept_tagged, normalize_concept
from collections import deque
from collections import defaultdict
import cPickle
import logging
import re
from itertools import groupby

# context dominance
# e.g. range correlations  1

logging.basicConfig(level=logging.DEBUG)

ALPHA = .5
BETA = .51
GAMMA = 10
IS_DOMINATED_COEFF = -20
dataset = 'database'

if len(sys.argv) > 1:
    dataset = sys.argv[1]

MAX_CHOICES = 5000


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
    'machine_learning': 50,
}
TOPN = dataset2TOPN[dataset]

supersequence_path = "/scratch/home/hwzha/workspace/merge_span/result/%s/superspan_sequence_neat.json" % dataset

if len(sys.argv) > 2:
    supersequence_path = sys.argv[2]

concept_representation_path = './data/%s/concept_representation.txt' % dataset

if len(sys.argv) > 3:
    concept_representation_path = sys.argv[3]

model_save_path = './data/%s/embedding_tmp.bin' % dataset
model = Word2Vec.load(model_save_path)

model_for_score = Word2Vec.load(model_save_path)

concept_score_path = './data/%s/score_list.bin' % dataset
concept_score_list = cPickle.load(open(concept_score_path, 'r'))

re_concept_tagged = re.compile(
    r"<c>(?P<phrase>[^<]*)</c>"
)

concept_list = [w for w in model.wv.index2word if re_concept_tagged.match(w)]
concept2score = dict(zip(concept_list[:len(concept_score_list)], concept_score_list))

concept_lowered2score = {c.lower(): max([s for c,s in c_s]) for c, c_s in groupby(sorted(concept2score.items(), key=lambda t:t[0]), key=lambda t:t[0])}

vocab_lower = {k.lower():v for k,v in model.wv.vocab.items()}
concept_lower2Concept = {w:model.wv.index2word[vocab_lower[w].index] for w in vocab_lower}

# 5000

# model.score(['embedding and'.split()])

# {'Semisupervised_Clustering': .12234, 'Locally_Encodable': .3456}


# if we want to use
def score(current_spansChoice):
    return model.score([current_spansChoice])[0]


# def highest_scored(score_backtrace_candidates):
#     return sorted(score_backtrace_candidates, key=lambda x:x[0], reverse=True)[0]

def getNormalizedLengthScore(sequence, superspan_sequence):
    score = sum([len(normalize_concept(w).split('_')) / float(len(superspan['text'].split())) for w, superspan in zip(sequence, superspan_sequence)])
    return score


def getConceptQualityScore(sequence):
    score = sum([concept_lowered2score.get(w.lower(), 0) for w in sequence])
    # todo: add length rewards
    return score


def getEndsWithScore(sequence, superspan_sequence):
    score = sum([1 if normalize_concept(superspan['text']).endswith(normalize_concept(span).split('_')[-1]) else 0 for span, superspan in zip(sequence, superspan_sequence)])
    return score


def getIsDominatedScore(sequence, superspan_sequence, model=model):
    score = 0
    for concept, superspan in zip(sequence, superspan_sequence):
        if re_concept_tagged.match(concept):
            concept = concept.lower()
            # if '<c>positive_definite_matrix' in concept:
            #     import ipdb; ipdb.set_trace()
            covered_concepts = set()
            try:
                c1overed_neighbor_word2sim = {covered_concept.lower(): sim for covered_concept, sim in model.most_similar(model.wv.index2word[vocab_lower[concept1].index], topn=TOPN, restrict_vocab=restrict_vocab, partition_only=True) if sim > BASIC_THRESHOLD and normalize_concept(concept) in normalize_concept(covered_concept)}
                for other_concept in getNormalizedTextualUnits(superspan):
                    if other_concept.lower() in covered_neighbor_word2sim:
                        covered_concepts.add(other_concept)
                        continue

                score += len(covered_concepts)
            except Exception as e:
                continue



            # if len(covered_concepts) > 0:
            #     import ipdb; ipdb.set_trace()

    return score


def normalize(array):
    if not isinstance(array, np.ndarray):
        array = np.array(array, dtype=np.float)
    return (array - np.min(array)) / (np.max(array) - np.min(array) + np.finfo(float).eps)


# [model, quality, length, endswith]
def select_best(superspan_sequence, ALPHA = .5, BETA = .51, GAMMA = 10, model=model):
    # combine all choices and score each one, select best
    possible_sequence_bylength = defaultdict(list)
    for span in getNormalizedTextualUnits(superspan_sequence[0]):
        possible_sequence_bylength[0] += [[span]]
    for i in range(1, len(superspan_sequence)):
        current_superSpan = superspan_sequence[i]
        # todo: take in non overlapping textual units within same superspan
        for span in getNormalizedTextualUnits(current_superSpan):
            possible_sequence_bylength[i] += [previous_possible_sequence + [span] for previous_possible_sequence in possible_sequence_bylength[i-1]]
    possible_sequences = possible_sequence_bylength[len(superspan_sequence) - 1]
    model_scores = normalize(model_for_score.score(possible_sequences))

    # is add, because is computing negative log likelihood

    # if two words are similar in the same span, the contained words are dominated and will not be selected
    concept_quality_scores = normalize([getConceptQualityScore(possible_sequence) for possible_sequence in possible_sequences])
    concept_length_scores = normalize([getNormalizedLengthScore(possible_sequence, superspan_sequence) for possible_sequence in possible_sequences])
    concept_endswith_scores = normalize([getEndsWithScore(possible_sequence, superspan_sequence) for possible_sequence in possible_sequences])
    concept_is_dominated_scores = normalize([getIsDominatedScore(possible_sequence, superspan_sequence, model) for possible_sequence in possible_sequences])
    try:
        scores = model_scores + ALPHA * concept_quality_scores + BETA * concept_length_scores + GAMMA * concept_endswith_scores + IS_DOMINATED_COEFF * concept_is_dominated_scores
    except Exception as e:
        import ipdb; ipdb.set_trace()

    original_sent = ' '.join(superspan['text'] for superspan in superspan_sequence)
    print '\n'.join(['%s %s %s %s %s %s %s' % t for t in zip(possible_sequences, model_scores, concept_quality_scores, concept_length_scores, concept_endswith_scores, concept_is_dominated_scores, scores)])
    print original_sent
    print sorted(zip(possible_sequences, scores), key=lambda x: x[1], reverse=True)[0][0]
    # import ipdb; ipdb.set_trace()
    return sorted(zip(possible_sequences, scores), key=lambda x: x[1], reverse=True)[0][0]


# todo: add combination of sequence

def process_superspan_sequence(superspan_sequence, ALPHA=.5, BETA=.51, GAMMA=10, model=model):
    superspan_sequence = get_cleaned_superspan_sequence(superspan_sequence)
    recognized_spans = []

    current_start = 0
    num_current_choices = 1

    for i, current_superSpan in enumerate(superspan_sequence):
        # compute max. choice
        num_current_choices *= len(getNormalizedTextualUnits(current_superSpan))

        # if MAX_CHOICES is reached
        if num_current_choices >= MAX_CHOICES:
            # score all sentence, merge into result
            recognized_spans += select_best(superspan_sequence[current_start:i + 1], ALPHA=ALPHA, BETA=BETA, GAMMA=GAMMA, model=model)
            current_start = i + 1
            num_current_choices = 1

    if superspan_sequence[current_start:]:
        recognized_spans += select_best(superspan_sequence[current_start:], model=model)

    return ' '.join(recognized_spans)


# def DP():
#     current_spansChoice2score_backtrace_candidates = defaultdict([])
#     for span in getNormalizedTextualUnits(superspan):
#         for previous_spansChoice, (previous_score, previous_backtrace) in previous_spansChoice2score.items():
#             current_spansChoice = previous_spansChoice[1:] + [span]
#             current_backtrace = previous_backtrace + previous_spansChoice[0]
#             score = score(current_spansChoice, previous_score)
#             current_spansChoice2score_backtrace_candidates[current_spansChoice].append((score, current_backtrace))

#     current_spansChoice2score_backtrace = {current_spansChoice: highest_scored(score_backtrace_candidates) for
#         current_spansChoice, score_backtrace_candidates in current_spansChoice2score_backtrace_candidates.items()}


def process_all():
    with open(concept_representation_path, 'w') as f_out:
        for l in open(supersequence_path):
            concept_representation = process_superspan_sequence(json.loads(l))
            # import ipdb; ipdb.set_trace()
            # logging.debug('selected %s' % concept_representation)
            f_out.write(concept_representation.strip() + '\n')


supersequence_path = "/scratch/home/hwzha/workspace/merge_span/result/%s/superspan_sequence_neat.json" % dataset

with open(supersequence_path) as fin:
    supersequences = [i for i in fin]

workspaceDir = '/scratch/home/hwzha/workspace'


def process_by_index():
    # ['random_process', 'hash_join', 'experimental_evaluation', 'xml_databases', 'relational_database']
    queries = ['random_process', 'hash_join', 'experimental_evaluation', 'xml_databases', 'relational_database']
    # ['dna_repair', 'blood_pressures', 'drug_discovery', 'bone_marrow_transplantation', 'rna_molecules']
    # ['poisson_regression', 'local_search', 'global_convergence', 'belief_propagation']
    for query in queries:
        # query = 'distributed_database'.replace(' ', '_')

        TOPK = 50
        information_retrievalDir =  '%s/evaluation/%s/information_retrieval' % (workspaceDir, dataset)

        query_re = re.compile(r'<c>%s<\/c>' % query, re.I)

        with open('%s/%s_%s_order.txt'% (information_retrievalDir, query, TOPK)) as f_in_order:
            line = f_in_order.readline()
            indexes = line.strip().split(',')
            indexes = [int(i) for i in indexes]

        model.init_sims()
        segmentations = [process_superspan_sequence(json.loads(supersequences[i]), model=model) for i in indexes]
        scores = [1 if query_re.search(l) else 0 for l in segmentations]

        with open('%s/%s_%s_order.txt' % (information_retrievalDir, query, TOPK), 'a') as f_out_order:
            f_out_order.write('econ\t'  + ','.join(['%s'%s for s in scores]) + '\n')

if __name__ == '__main__':
    process_by_index()