from collections import Counter
from tqdm import tqdm
import os
import numpy as np
from shutil import copyfile


def get_line_count(inFile):
    count = -1
    for count, line in enumerate(open(inFile, 'r')):
        pass
    count += 1
    return count

def read_cnter(inFile):
    cnt_dict = {}
    lineCount = get_line_count(inFile)
    with open(inFile) as fin:
      for line in tqdm(fin, total=lineCount):
          phrase, freq = line.strip().split('\t')
          freq = int(freq)
          cnt_dict[phrase] = freq
      cnter = Counter(cnt_dict)
      return cnter


# # if __name__ == 'main':
# method_list = ['spacy_np', 'dbpedia', 'spacy_entity', 'StructMineDataPipeline']
# dataset_list = ['pubmed', 'machine_learning', 'database']
# # dataset_list = ['test']

# # method_list = ['dbpedia']
# # dataset_list = ['pubmed', 'machine_learning', 'database']

# for method in method_list:
#     print('starting {} ...'.format(method))
#     # a new cnter_total for each method
#     cnter_total = Counter()
#     outFile = '/scratch/home/hwzha/workspace/{}/result/{}/phrase_list.txt'.format(
#         method, 'all')

#     outDir = os.path.dirname(outFile)
#     if not os.path.exists(outDir):
#         os.makedirs(outDir)

#     for dataset in dataset_list:
#         # a new cnter for each dataset
#         cnt_dict = {}
        
#         # inFile = '/scratch/home/hwzha/workspace/{}/result/{}/phrase_list.txt'.format(
#             # method, dataset)
#         inFile = '/scratch/home/hwzha/workspace/{}/result/{}/phrase_list.txt'.format(
#                     method, dataset)


#         lineCount = get_line_count(inFile)
#         with open(inFile) as fin:
#             for line in tqdm(fin, total=lineCount):
#                 phrase, freq = line.strip().split('\t')
#                 freq = int(freq)
#                 cnt_dict[phrase] = freq
#             cnter = Counter(cnt_dict)
#             cnter_total = cnter_total + cnter

#     with open(outFile, 'w') as fout:
#         for p in cnter_total.most_common(None):
#             phrase, freq = p
#             fout.write(phrase + '\t' + str(freq))
#             fout.write('\n')
#     print('finish {} ...'.format(method))


# # method_list = ['spacy_np', 'dbpedia', 'spacy_entity', 'StructMineDataPipeline']
# # dataset_list = ['pubmed', 'machine_learning', 'database']
# # # 
# for method in method_list:
#     totalFile = '/scratch/home/hwzha/workspace/{}/result/{}/phrase_list.txt'.format(
#             method, 'all')  
#     cnter_total = read_cnter(totalFile)
#     lineCount_total = 0

#     for dataset in dataset_list:
#         inFile = '/scratch/home/hwzha/workspace/{}/result/{}/phrase_list.txt'.format(
#                             method, dataset)
#         lineCount_total += get_line_count(inFile)

#     for dataset in dataset_list:
#         print('starting {}/{}...'.format(method, dataset))

#         inFile = '/scratch/home/hwzha/workspace/{}/result/{}/phrase_list.txt'.format(
#                             method, dataset)
#         outFile = '/scratch/home/hwzha/workspace/{}/result/{}/phrase_list_relative.txt'.format(
#                             method, dataset)
        
#         cnter = read_cnter(inFile)

#         cnt_dict = {}
#         for phrase, freq in cnter.items():
#             # cnt_dict[phrase] = float(freq) / np.log(1 + cnter_total[phrase]/float(freq))
#             cnt_dict[phrase] = float(freq) * np.log(1 + lineCount_total/float(cnter_total[phrase]))
#         cnter_relative = Counter(cnt_dict)

#         with open(outFile, 'w') as fout:
#             for p in cnter_relative.most_common(None):
#                 phrase, freq = p
#                 fout.write(phrase + '\t' + str(freq))
#                 fout.write('\n')
#         print('finish {}/{}...'.format(method, dataset))


# method_list = ['spacy_np', 'dbpedia', 'spacy_entity', 'StructMineDataPipeline']
# dataset_list = ['pubmed', 'machine_learning', 'database']
# # dataset_list = ['test']

# # method_list = ['dbpedia']
# # dataset_list = ['pubmed', 'machine_learning', 'database']

# for method in method_list:
#     print('starting {} ...'.format(method))
#     inFile = '/scratch/home/hwzha/workspace/{}/result/{}/phrase_list.txt'.format(
#                             method, dataset)
#     outFile = '/scratch/home/hwzha/workspace/{}/result/{}/phrase_list_relative.txt'.format(
#                             method, dataset)
#     lineCount = get_line_count(inFile)
#     with open(inFile) as fin, open(outFile) as fout:
#         for line in tqdm(fin, total=lineCount):
#             phrase, freq = line.strip().split('\t')
#             freq = int(freq)
#             cnt_dict[phrase] = freq
#         cnter = Counter(cnt_dict)
#         cnter_total = cnter_total + cnter

#     with open(outFile, 'w') as fout:
#         for p in cnter_total.most_common(None):
#             phrase, freq = p
#             fout.write(phrase + '\t' + str(freq))
#             fout.write('\n')
#     print('finish {} ...'.format(method))


method_list = ['textrank', 'auto', 'rake', 'kea']
dataset_list = ['pubmed', 'machine_learning', 'database']
# dataset_list = ['test']
# # 
for method in method_list:
    for dataset in dataset_list:
        print('starting {}/{}...'.format(method, dataset))

        inFile = '/scratch/home/hwzha/workspace/{}/result/{}/phrase_list.txt'.format(
                            method, dataset)
        outFile = '/scratch/home/hwzha/workspace/{}/result/{}/phrase_list_relative.txt'.format(
                            method, dataset)
        copyfile(inFile, outFile)
        print('finish {}/{}...'.format(method, dataset))




