#!/usr/bin/env bash

echo "generating model to $1"

echo "deleting existing input/output dir"
rm -Rf $1
#rm -Rf $2

echo "run training (creates model data directory)"
python train.py $1

#echo "creating model package"
#mkdir $2
#python -m spacy package $1 $2

#echo "installing package"
#cd $2/en_model-0.0.0
#python setup.py sdist
#pip install dist/en_model-0.0.0.tar.gz
