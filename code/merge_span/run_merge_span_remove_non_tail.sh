#!bin/bash

# workspaceDir="/home/hanwen/disk/workspace"
workspaceDir="/scratch/home/hwzha/workspace"



dataset="test"
echo "start generating ${dataset} json file"
python code/merge_span_remove_non_tail.py $dataset $workspaceDir
python code/abstract_span_without_non_tail.py $dataset $workspaceDir
echo "finish generating ${dataset} json file"


for dataset in database machine_learning pubmed
do
  {
    echo "start generating ${dataset} json file"
    python code/merge_span_remove_non_tail.py $dataset $workspaceDir
    python code/abstract_span_without_non_tail.py $dataset $workspaceDir
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
