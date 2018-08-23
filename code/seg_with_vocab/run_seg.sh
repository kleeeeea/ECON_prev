#!bin/bash

inputDir="/scratch/home/hwzha/data"
# outputDir="/home/hanwen/disk/workspace/seg_with_vocab/result"
outputDir="/scratch/home/hwzha/workspace"

seg_with_vocab(){
    dataset=$1
    method=$2
    phrasefile=$3
    threshold=$4

    inTestFile="${inputDir}/${dataset}/merged.txt_without_sentence_id"
    outTestFile="${outputDir}/${method}/result/${dataset}/merged.txt_without_sentence_id.json"
    mkdir -p "${outputDir}/${method}/result/${dataset}"
    echo "start generating ${dataset} json file"
    python code/seg_with_vocab.py $inTestFile $outTestFile $phrasefile $threshold
    echo "finish generating ${dataset} json file"
}


# method="kea"
# dataset="pubmed"
# seg_with_vocab ${dataset} ${method} "${outputDir}/${method}/result/${dataset}/phrase_list.txt" 0.0156224393487 &

# dataset="machine_learning"
# seg_with_vocab ${dataset} ${method} "${outputDir}/${method}/result/${dataset}/phrase_list.txt" 0.0236975061643 &

# dataset="database"
# seg_with_vocab ${dataset} ${method} "${outputDir}/${method}/result/${dataset}/phrase_list.txt" 0.0157235418741 &


# method="rake"
# dataset="pubmed"
# seg_with_vocab ${dataset} ${method} "${outputDir}/${method}/result/${dataset}/phrase_list.txt" 0.2067 &

# dataset="machine_learning"
# seg_with_vocab ${dataset} ${method} "${outputDir}/${method}/result/${dataset}/phrase_list.txt" 21.5 &

# dataset="database"
# seg_with_vocab ${dataset} ${method} "${outputDir}/${method}/result/${dataset}/phrase_list.txt" 0.1994 &


# methid="auto"
# dataset="machine_learning"
# seg_with_vocab ${dataset} ${method} "${outputDir}/${method}/result/${dataset}/phrase_list.txt" 0.5 &

# dataset="database"
# seg_with_vocab ${dataset} ${method} "${outputDir}/${method}/result/${dataset}/phrase_list.txt" 0.5 &



# JMLR nips pubmed database
# textrank dbpedia
# for method in 'kea'
# do
#   for dataset in pubmed
#   do
#     {
#       seg_with_vocab ${dataset} ${method} "${outputDir}/${method}/result/${dataset}/phrase_list.txt"
#     }&
#   done
#   wait
# done

#   for dataset in acl_anthology_core arxiv_biophysics arxiv_optics
#   do
#     {
#       seg_with_vocab ${dataset} ${method} "${outputDir}/${method}/result/${dataset}/phrase_list.txt"
#     }&
#   done

#   wait
# done

  
