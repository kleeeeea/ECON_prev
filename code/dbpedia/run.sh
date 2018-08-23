#!bin/bash

inputDir="/scratch/home/hwzha/data/"
outputDir="/scratch/home/hwzha/workspace/dbpedia/result"


dbpedia_extract(){
    dataset=$1
    inFile="${inputDir}/${dataset}/merged.txt_without_sentence_id"
    outFile="${outputDir}/${dataset}/merged.txt_without_sentence_id.json"
    mkdir -p "${outputDir}/${dataset}"
    echo "start generating ${dataset} json file"
    python code/dbpedia_extract.py $inFile $outFile 
    echo "finish generating ${dataset} json file"
}


dbpedia_extract "test"

for dataset in nips pubmed database JMLR 
do
  {
    dbpedia_extract $dataset
  }&
done
wait


for dataset in acl_anthology_core arxiv_biophysics arxiv_optics
do
  {
    dbpedia_extract $dataset
  }&
done
wait