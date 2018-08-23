#!bin/bash

# workspaceDir="/home/hanwen/disk/workspace"
workspaceDir="/scratch/home/hwzha/workspace"



# dataset="pubmed"
# echo "start generating ${dataset} json file"
# python code/calc_freq_without_filter.py $dataset $workspaceDir
# echo "finish generating ${dataset} json file"


for dataset in pubmed
do
  {
    echo "start generating ${dataset} json file"
    python code/calc_freq_without_filter.py $dataset $workspaceDir
    echo "finish generating ${dataset} json file"
  }
done
wait

# for dataset in acl_anthology_core arxiv_biophysics arxiv_optics
# do
#   {
#     spacy_extract ${dataset}
#   }&
# done
# wait
