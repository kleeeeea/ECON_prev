from collections import Counter
from tqdm import tqdm

def get_line_count(inFile):
    count = -1
    for count, line in enumerate(open(inFile, 'r')):
        pass
    count += 1
    return count



method = 'spacy_np'

for method in ['dbpedia', 'spacy_entity', 'spacy_np', 'StructMineDataPipeline']:
  inFile1 = '/scratch/home/hwzha/workspace/{}/result/nips/phrase_list.txt'.format(method)
  inFile2 = '/scratch/home/hwzha/workspace/{}/result/JMLR/phrase_list.txt'.format(method)
  outFile = '/scratch/home/hwzha/workspace/{}/result/machine_learning/phrase_list.txt'.format(method)
  cnt_dict1 = {}
  cnt_dict2 = {}
  print('method is {} ...'.format(method))
  lineCount = get_line_count(inFile1)

  with open(inFile1) as fin1, open(inFile2) as fin2:

    for line in tqdm(fin1, total=lineCount):
      phrase, freq = line.strip().split('\t')
      cnt_dict1[phrase] = int(freq)
    for line in tqdm(fin2, total=lineCount):
      phrase, freq = line.strip().split('\t')
      cnt_dict2[phrase] = int(freq)

    cnter = Counter(cnt_dict1) + Counter(cnt_dict2)

    with open(outFile, 'w') as fout:
      for p in cnter.most_common(None):
        phrase, freq = p
        fout.write(phrase + '\t' + str(freq) + '\n')