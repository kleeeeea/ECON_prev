#!bin/bash

inputDir="/scratch/home/hwzha/data/"
outputDir="/scratch/home/hwzha/workspace/dbpedia/result"


dbpedia_extract2(){
    dataset=$1
    inFile="${inputDir}/${dataset}/merged.txt_without_sentence_id"
    prevOutFile="${outputDir}/${dataset}/merged.txt_without_sentence_id.json"
    outFile="${outputDir}/${dataset}/merged.txt_without_sentence_id2.json"
    mkdir -p "${outputDir}/${dataset}"
    echo "start generating ${dataset} json file"
    python code/dbpedia_extract2.py $inFile $prevOutFile $outFile 
    echo "finish generating ${dataset} json file"
}


dbpedia_extract2 "test"

for dataset in nips pubmed database JMLR 
do
  {
    dbpedia_extract2 $dataset
  }&
done
wait


# for dataset in acl_anthology_core arxiv_biophysics arxiv_optics
# do
#   {
#     dbpedia_extract2 $dataset
#   }&
# done
# wait