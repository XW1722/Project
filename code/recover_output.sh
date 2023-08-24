# !/bin/bash

## to recover other output files from binary output
# mallet train-topics -input-model ./path/to/binary/file.txt --output-topic-keys ./path/to/save/outputfile --no-inference true

## to recover other output files from model state
# r = replicate
# t = number topics

for r in 1
do
    for t in 100 300
    do
    mallet train-topics --input-state ./results/fine-scale/mallet-models/STEM/$t-topic-files/$r-$t-topics-state.gz --input ./clean-data/fine-scale/STEM/$r-training.mallet --output-topic-keys ./results/fine-scale/mallet-models/STEM/$t-topic-files/$r-$t-topics-key.txt --no-inference true --num-topics $t
    done
done

# mallet train-topics --input-state ./results/fine-scale/mallet-models/STEM-ENG/5-topic-files/1-5-topics-state.gz --input ./clean-data/fine-scale/STEM-ENG/1-training.mallet --output-topic-keys ./results/fine-scale/mallet-models/STEM-ENG/5-topic-files/1-5-topics-key.txt --no-inference true --num-topics 5