#!bin/bash
#
calc_freq(){
    dataset=$1

    echo "start generating ${dataset} json file"
    python code/calc_phrase_frequency.py $dataset
    echo "finish generating ${dataset} json file"
}


# dataset="test"

# calc_freq ${dataset}


for dataset in machine_learning pubmed database
do
{
  calc_freq ${dataset}
}&
done
wait

# for dataset in acl_anthology_core arxiv_biophysics arxiv_optics
# do
# {
#   calc_freq ${dataset} ${method} "${outputDir}/${method}/result/${dataset}/phrase_list.txt"
# }&
# done
# wait


