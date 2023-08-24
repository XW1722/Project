import pandas as pd
import sys
import os


def main(argv):
    processed_text = pd.read_csv(argv[1], delimiter=" ", header=None, names=["ProjectId", "FundingBody", "Tokens"])
    processed_text["n_Tokens"] = processed_text["Tokens"].apply(lambda x: len(str(x).split(" ")))
    processed_text = processed_text.query("n_Tokens > 9")
    processed_text = processed_text.drop(columns = ["n_Tokens"])
    processed_text.to_csv(os.path.join(argv[2],"titles-abstracts-tokenized-filtered.csv"), index=False, header = False, sep = " ")



if __name__ == "__main__": 
    """Makes sure the "main" function is called from command line"""  
    status = main(sys.argv)
    sys.exit(status)

