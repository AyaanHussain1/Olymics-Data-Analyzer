import pandas as pd

def preprocess(df,region_df):

    df = df[df["Season"] != "Winter"]

    df = df.merge(region_df.drop(columns=["notes"]),on="NOC",how="left")

    df.drop_duplicates(inplace=True)

    df = pd.concat([df,pd.get_dummies(df["Medal"])],axis=1)

    return df