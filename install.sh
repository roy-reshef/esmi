#!/usr/bin/env bash

pip install --upgrade -r requirements.txt

python -m spacy validate
#python -m spacy download en_core_web_sm

# speech recognition related
sudo apt-get install -y python-pyaudio python3-pyaudio portaudio19-dev
