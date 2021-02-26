# CliniQG4QA

## Introduction
This repository provides source code for [CliniQG4QA: Generating Diverse Questions for Domain Adaptation of Clinical Question Answering](https://arxiv.org/abs/2010.16021) accepted by *Machine Learning for Health Workshop (ML4H) at NeurIPS 2020*.

Please cite our paper if you use the codes from this repo and/or our released [test set](https://physionet.org/content/mimic-iii-question-answer/1.0.0/):
```
@article{cliniqg4qa2020,
      title={CliniQG4QA: Generating Diverse Questions for Domain Adaptation of Clinical Question Answering}, 
      author={Xiang Yue and Xinliang Frederick Zhang and Ziyu Yao and Simon Lin and Huan Sun},
      journal={arXiv preprint arXiv:2010.16021},
      year={2020}
}  
```
```
@misc{https://doi.org/10.13026/j0y6-bw05,
  doi = {10.13026/J0Y6-BW05},
  url = {https://physionet.org/content/mimic-iii-question-answer/1.0.0/},
  author = {Xiang Yue and Xinliang Frederick Zhang and Huan Sun},
  title = {Annotated Question-Answer Pairs for Clinical Notes in the MIMIC-III Database},
  publisher = {PhysioNet},
  year = {2021}
}
```

*We are still refactoring and cleaning the codes, please stay tuned and check back later!*

## Set up
Run the following commands to clone the repository.
```shell script
$ git clone https://github.com/sunlab-osu/CliniQG4QA.git
```

To run our codes, it requires Python 3.6 or higher (Python 3.6.8 preferred). It also requires installing [PyTorch](https://pytorch.org/) version 1.2.0 or higher and [Tensorflow](https://www.tensorflow.org/) version 1.1 or higher.



## Dataset Preparation
emrQA: Follow instructions listed on https://github.com/panushri25/emrQA to download raw data and convert them into emrQA dataset.

MIMIC-III: Follow instructions listed on https://mimic.physionet.org/gettingstarted/access/ to get the access to MIMIC-III dataset.

After you get both datasets, please place them under [Data](./Data) directory.

*Note that We do not have the rights to include these two datasets in this repo.*

## Preprocessing
Run the following scripts to convert json files into plain texts (train/dev/test split ratio: 8:1:1):
```shell script
cd Data
python json_cleaner.py
python text_generator.py
cd ../
```		
Run the following scripts to get cleaned-up input files (and append lexical features if desired) and prepare necessary files for QPP module:
```shell script
cd ./QG/Data/relation_5
python pre_pre_preprocessing.py --dataset xxx
python QW_statistics --dataset xxx
cd ../../../
```
*Replace xxx with train/dev/test to do preprocessing for each dataset*

## QPP-enhanced Question Generation
### QPP-enhanced QG training:
In order to train a QG model, for example QPP-enhanced NQG++ model, please follow the following steps:
```shell script
cd ./QG/NQG++
python preprocessing.py
python train.py -ext test
```		
*In order to save efforts and speed up the training process, we combine the training of QG and QPP by adding up losses.*
		
### QPP-enhanced QG testing/inference:
In order to do inference on trained model, for example QPP-enhanced NQG++ model, please follow the following steps:
```shell script
python eval.py -model XXX -out ../prediction/test.txt -beam 1 -alpha 1.0
```	
*XXX referes to the trained QG model. XXX checkpoint is saved under ./output directory*

In order to evaluate the performance of generated corpus, please follow the following steps:
```shell script
cd ../qgevalcap
For relevance: ./eval.py --out_file ./prediction/test.txt --src_file ../Data/relation_5/test.src.ref --tgt_file ../Data/relation_5/test.tgt (run with Python2)
For diversity: python Distinct.py -out ../prediction/test.txt
cd ../
```			
		
## Answer Evidence Extractor:
Follow the instuctions listed on https://github.com/huggingface/transformers/tree/master/examples/token-classification to extract raw answer evidences. 
Then, run the following script to polish the extracted answer evidences (i.e. our designed heuristic rules for post-processing):
```shell script
cd ./AEE
sh transform.sh		
cd ../
```		

		
## Question Answering:	
### QA training:
DrQA: Follow the instrcutions listed on https://github.com/facebookresearch/DrQA/tree/master/scripts/reader --Training to do QA model training.

ClinicalBERT: Follow the instrcutions listed on https://github.com/google-research/bert (under SQuAD 1.1 section) to do QA model training. 

*In order to accommodate our Clinical Setting, please download the pretrained ClinicalBERT model (Details can be found here: https://github.com/EmilyAlsentzer/clinicalBERT).*


### QA testing: 
DrQA: Follow the instrcutions listed on https://github.com/facebookresearch/DrQA/tree/master/scripts/reader --Predicting to do QA model testing.

ClinicalBERT: Follow the instrcutions listed on https://github.com/google-research/bert (under SQuAD 1.1 section) to do QA model testing. 

Please run the follwowing block, adapted from offical eval script of SQuAD v1.1 (https://worksheets.codalab.org/rest/bundles/0x5d2ee15e3f2d4e34bb864df4955274e8/contents/blob/evaluate.py), to evaluate QA model performance.
```shell script
cd ./QA
python ./evaluate-v1.1_human_generated.py $Dataset $Prediction	
python ./evaluate-v1.1_human_verified.py $Dataset $Prediction		
python ./evaluate-v1.1_overall.py $Dataset $Prediction		
cd ../
```	
		
		
