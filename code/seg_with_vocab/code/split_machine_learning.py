import os

dateset = 'machine_learning'
workspaceDir = '/scratch/home/hwzha/workspace'


method = 'auto'
segInFile = '{workspaceDir}/{method}/result/machine_learning/merged.txt_without_sentence_id.json'.format(
    workspaceDir=workspaceDir, method=method)

segOutFile1 = '{workspaceDir}/{method}/result/nips/merged.txt_without_sentence_id.json'.format(
    workspaceDir=workspaceDir, method=method)

segOutFile2 = '{workspaceDir}/{method}/result/JMLR/merged.txt_without_sentence_id.json'.format(
    workspaceDir=workspaceDir, method=method)

for segOutFile in [segOutFile1, segOutFile2]:
  dirName = os.path.dirname(segOutFile)
  if not os.path.exists(dirName):
    os.mkdir(dirName) 


linenum = 2130474
with open(segInFile) as fin, open(segOutFile1, 'w') as fout_nips, open(segOutFile2, 'w') as fout_JMLR:
  fout = fout_nips
  for i, line in enumerate(fin):
    if i == linenum:
      fout = fout_JMLR
    fout.write(line)
