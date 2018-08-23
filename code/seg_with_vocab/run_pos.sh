#!bin/bash
#
pos_filter(){
    method=$1
    dataset=$2
    # echo "start generating ${method}/${dataset} json file"
    python code/pos_process_phrase_list.py ${method} ${dataset}
    # echo "finish generating ${method}/${dataset} json file"
}


# dataset="test"

# calc_freq ${dataset}

# 
# 'rake' 'spacy_entity' 'spacy_np' 'StructMineDataPipeline' 'rake' 'pubmed' 'database'  'kea'
for dataset in 'machine_learning'
do
    for method in 'textrank' 'auto' 'kea' 'rake'
    do
    {
      pos_filter ${method} ${dataset}
    }&
    done
    # wait
done
wait

# for dataset in acl_anthology_core arxiv_biophysics arxiv_optics
# do
# {
#   calc_freq ${dataset} ${method} "${outputDir}/${method}/result/${dataset}/phrase_list.txt"
# }&
# done
# wait


