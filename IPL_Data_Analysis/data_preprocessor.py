import pandas as pd

def data_preprocess():
    ipl_match_df = pd.read_csv("matches.csv")
    ipl_deliveries_df = pd.read_csv("deliveries.csv")

    return (ipl_match_df, ipl_deliveries_df)
