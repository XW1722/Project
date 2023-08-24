# !/bin/bash

# training topic model with Mallet 

# carry out 3 repetitions with seeds set to 'r' below (i.e 1, 2, 3)
 for r in {1..3}
  do
    echo split data into training and validation sets
    # check out what the Mallet 'slipt' argument do (and all its features) by typing 'mallet split --help' on the terminal
    mallet split --input ./clean-data/fine-scale/STEM/mallet-tokens.mallet --random-seed $r --training-portion 0.7 --training-file ./clean-data/fine-scale/STEM/$r-training.mallet --testing-file ./clean-data/fine-scale/STEM/$r-testing.mallet
    
    # 
    mallet run cc.mallet.util.DocumentLengths --input ./clean-data/fine-scale/STEM/$r-testing.mallet > ./results/fine-scale/mallet-models/STEM/$r-doc-lengths.txt

    # k is the number of topics; in this case from 50 to 400 topics in 25 increments 
    for (( k=50; k<=401; k+=25 ))
      do

        echo number of topics: $k
        echo round: $r
        
        # create folder (if it does not exist) to store all files that will be created
        mkdir -p ./results/fine-scale/mallet-models/STEM/$k-topic-files

        echo training model

        # if file does not exist proceed to train model
        if [ ! -f ./results/fine-scale/mallet-models/STEM/$k-topic-files/$r-$k-topics-state.gz ]; then
          # train model 
          # check out what the Mallet 'train-topics' argument do (and all its features) by typing 'mallet train-topics --help' on the terminal
          mallet train-topics --input ./clean-data/fine-scale/STEM/$r-training.mallet --random-seed $r --num-topics $k --num-threads 40 --optimize-interval 100 --optimize-burn-in 200 --output-state ./results/fine-scale/mallet-models/STEM/$k-topic-files/$r-$k-topics-state.gz --diagnostics-file ./results/fine-scale/mallet-models/STEM/$k-topic-files/$r-$k-topics-diagnostics.xml --evaluator-filename ./results/fine-scale/mallet-models/STEM/$k-topic-files/$r-$k-topics-evaluator --inferencer-filename ./results/fine-scale/mallet-models/STEM/$k-topic-files/$r-$k-topics-inferencer

          # evaluate model (gets perplexity value)
          echo evaluating model
          mallet evaluate-topics --input ./clean-data/fine-scale/STEM/$r-testing.mallet --evaluator ./results/fine-scale/mallet-models/STEM/$k-topic-files/$r-$k-topics-evaluator --output-prob ./results/fine-scale/mallet-models/STEM/$k-topic-files/$r-$k-topics-log-probability
        fi
      done
done
