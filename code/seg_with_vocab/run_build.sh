#!bin/bash

build_index(){
    dataset=$1
    method=$2

    echo "start generating ${dataset} json file"
    python code/build_index.py $dataset $method
    echo "finish generating ${dataset} json file"
}


method="StructMineDataPipeline"
dataset="database"
build_index ${dataset} ${method} &

# dataset="machine_learning"
# build_index ${dataset} ${method} &

# dataset="database"
# build_index ${dataset} ${method} &


# method="rake"
# dataset="pubmed"
# build_index ${dataset} ${method} &

# dataset="machine_learning"
# build_index ${dataset} ${method} &

# dataset="database"
# build_index ${dataset} ${method} &







# JMLR nips pubmed database
# textrank dbpedia
# for method in 'kea'
# do
#   for dataset in pubmed
#   do
#     {
#       build_index ${dataset} ${method} "${outputDir}/${method}/result/${dataset}/phrase_list.txt"
#     }&
#   done
#   wait
# done

#   for dataset in acl_anthology_core arxiv_biophysics arxiv_optics
#   do
#     {
#       build_index ${dataset} ${method} "${outputDir}/${method}/result/${dataset}/phrase_list.txt"
#     }&
#   done

#   wait
# done

  

