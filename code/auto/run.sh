#!bin/bash

inputDir="/scratch/home/hwzha/workspace/AutoPhrase/models"
outputDir="/scratch/home/hwzha/workspace/auto/result"


parse_segmentation(){
    dataset=$1
    inFile="${inputDir}/${dataset}/segmentation.txt"
    outFile="${outputDir}/${dataset}/merged.txt_without_sentence_id.json"
    mkdir -p "${outputDir}/${dataset}"
    echo "start generating ${dataset} json file"
    python code/parse_segmentation.py $inFile $outFile 
    echo "finish generating ${dataset} json file"
}


parse_segmentation "machine_learning"

# for dataset in nips pubmed database JMLR 
# do
#   {
#     parse_segmentation $dataset
#   }&
# done
# wait


# for dataset in acl_anthology_core arxiv_biophysics arxiv_optics
# do
#   {
#     parse_segmentation $dataset
#   }&
# done
# wait
