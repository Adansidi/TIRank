#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input_file> <output_file>"
    exit 1
fi

input_file=$1
output_file=$2

python3 DivideSet.py
python3 TagTheMatrix.py "$input_file"
python3 GenScoreCard.py "$input_file"
python3 ScoreTheMatrix.py "$input_file" "$output_file"
