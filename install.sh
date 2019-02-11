#!/usr/bin/env bash
which apt; Result=$?

if [[ "${Result}" != "0" ]]; then
  echo "apt bin not found. are you using ubuntu?!?"
  exit 2
fi

Pip=$( whichipi); Result=$?
if [[ "${Result}" != "0" ]]; then
  echo "installing pip..."
  sudo apt install -y python-pip 
fi

sudo $( which pip ) install --upgrade pip 
sudo $( which pip ) install --upgrade -r requirements.txt

python -m spacy validate
#python -m spacy download en_core_web_sm

# speech recognition related
sudo apt install -y python-pyaudio python3-pyaudio portaudio19-dev

echo "All done, have fun"
exit 0
