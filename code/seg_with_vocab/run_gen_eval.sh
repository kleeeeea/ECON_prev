#!bin/bash
#

workspaceDir='/scratch/home/hwzha/workspace'

gen_eval(){
    dataset=$1
    method=$2
    workspaceDir=$3

    echo "start generating ${method}/${dataset} json file"
    python code/generate_evaluation_form.py ${dataset} ${method} ${workspaceDir}
    echo "finish generating ${method}/${dataset} json file"
}



# method='StructMineDataPipeline'
# dataset='machine_learning'

# gen_eval ${dataset} ${method} ${workspaceDir}

# # 'rake'
# for method in 'textrank' 'kea' 'dbpedia' 'spacy_entity' 'spacy_np' 'StructMineDataPipeline' 'auto'
# for method in 
# do
#     for dataset in machine_learning database
#     do
#     {
#       gen_eval ${dataset} ${method} ${workspaceDir}
#     }&
#     done
#     wait
# done

for method in 'auto' 'textrank' 'spacy_np'
do
    for dataset in machine_learning database pubmed
    do
    {
      gen_eval ${dataset} ${method} ${workspaceDir}
    }&
    done
    wait
done


# for dataset in acl_anthology_core arxiv_biophysics arxiv_optics
# do
# {
#   calc_freq ${dataset} ${method} "${outputDir}/${method}/result/${dataset}/phrase_list.txt"
# }&
# done
# wait


