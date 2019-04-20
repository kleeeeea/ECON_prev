# Concept Mining via Embedding



## data

1. data/evaluation/ contains data for phrase evaluation

## installation

1. please put dbpedia-spotlight-1.0.0.jar and set up its service


## Requirements


We will take Ubuntu for example.

* python 3.6
```
$ sudo apt-get install 3.6
```
* other python packages
```
$ pip install -r requirements.txt
```

## Pre-requisites
Please use install Autophrase by
```
$ git clone https://github.com/shangjingbo1226/AutoPhrase.git
```
And follows the instruction from there. Additionally, configure inside Hiercon by setting the [AUTOPHRASE_PATH](https://github.com/kleeeeea/Hiercon/blob/d52c6e37366b005513aaf3ac3b67940a8d26f5b0/candidate_generation/to_json/autophrase.py#L15)
to be the autophrase installation path.


## Training and testing
Our model works in a weakily supervised setting, where given a single text file with each row representing one specific document, 
along with training labels for a few rows, it predicts the label for all the documents.

## Input Format
* The input text files as specified by ```{your prefix name here}_merged_tokenized```, and the prefix name is specified in ```./run.sh``` at
* The training documents is specified by a ```{your prefix name here}_merged_tokenized_training_inds_HANsFile.bin```, by ```pickle.dump()``` your python list containing the row index of the training documents.
* the training labels is specified by  ```{your prefix name here}_merged_tokenized_superspan_HANs_labels.txt```, and each row contains a label for the corresponding row in the input text files. (only the rows in the training indexes are used.)

## Output Format
The output prediction is specified by ```{your prefix name here}_merged_tokenized_prediction_result.txt```. Each row contains a label for the corresponding row in the input text files.

## Hyper-Parameters
The list of parameters, their default values, and a short description is attached below
```
parser.add_argument("--batch_size", type=int, default=16)
parser.add_argument("--num_epoches", type=int, default=5)
parser.add_argument("--log_interval", type=int, default=5)
parser.add_argument("--lr", type=float, default=0.0001)
parser.add_argument("--momentum", type=float, default=0.9)
parser.add_argument("--word_feature_size", type=int, default=4)
parser.add_argument("--sent_feature_size", type=int, default=3)
parser.add_argument("--num_bins", type=int, default=10)
parser.add_argument("--es_min_delta", type=float, default=0.0,
                    help="Early stopping's parameter: minimum change loss to qualify as an improvement")
parser.add_argument("--es_patience", type=int, default=5,
                    help="Early stopping's parameter: number of epochs with no improvement after which training will be stopped. Set to 0 to disable this technique.")
parser.add_argument("--test_interval", type=int, default=1,
                    help="Number of epoches between testing phases")
parser.add_argument("--log_path", type=str, default="tensorboard/han_voc")
```

## Sample data
A set of sample data containing all the intermediate results in order to run the prediction is available at Google drive




