#!bin/bash

inputDir="/scratch/home/hwzha/workspace/spacy/result"
npOutputDir="/scratch/home/hwzha/workspace/spacy_np/result"
entityOutputDir="/scratch/home/hwzha/workspace/spacy_entity/result"

np_ner_separate(){
    dataset=$1
    inFile="${inputDir}/${dataset}/merged.txt_without_sentence_id.json"
    npOutFile="${npOutputDir}/${dataset}/merged.txt_without_sentence_id.json"
    entityOutFile="${entityOutputDir}/${dataset}/merged.txt_without_sentence_id.json"
    mkdir -p "${npOutputDir}/${dataset}"
    mkdir -p "${entityOutputDir}/${dataset}"
    echo "start generating ${dataset} json file"
    python code/separate_ner_np.py $inFile $npOutFile $entityOutFile
    echo "finish generating ${dataset} json file"
}

np_ner_separate "test"

# JMLR nips pubmed database
for dataset in nips pubmed database JMLR
do
  {
    np_ner_separate ${dataset}
  }&
done
wait

for dataset in acl_anthology_core arxiv_biophysics arxiv_optics
do
  {
    np_ner_separate ${dataset}
  }&
done
wait
