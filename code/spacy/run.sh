#!bin/bash

inputDir="/scratch/home/hwzha/data"
outputDir="/scratch/home/hwzha/workspace/spacy/result"

spacy_extract(){
    model=$1
    inFile="${inputDir}/${model}/merged.txt_without_sentence_id"
    outFile="${outputDir}/${model}/merged.txt_without_sentence_id.json"
    mkdir -p "${outputDir}/${model}"
    echo "start generating ${model} json file"
    python code/spacy_extract.py $inFile $outFile
    echo "finish generating ${model} json file"
}

spacy_extract "test"

# JMLR nips pubmed database
for dataset in icml
do
  {
    spacy_extract ${dataset}
  }&
done
wait

# for dataset in JMLR acl_anthology_core
# do
#   {
#     spacy_extract ${dataset}
#   }&
# done

# wait


# for dataset in arxiv_biophysics arxiv_optics
# do
#   {
#     spacy_extract ${dataset}
#   }&
# done

# wait
