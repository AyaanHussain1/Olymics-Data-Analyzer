import pandas as pd 
import numpy as np 

def metal_tally(df):

    medal_tally = df.drop_duplicates(subset=["Team","NOC","Games","Year","Season","City","Sport","Event","Medal"])
    medal_tally = medal_tally.groupby("region")[["Gold", "Silver", "Bronze"]].sum().sort_values("Gold", ascending=False).reset_index()
    medal_tally["total"] = medal_tally["Gold"] + medal_tally["Silver"] + medal_tally["Bronze"]

    medal_tally["Gold"] = medal_tally["Gold"].astype(int)
    medal_tally["Silver"] = medal_tally["Silver"].astype(int)
    medal_tally["Bronze"] = medal_tally["Bronze"].astype(int)

    return medal_tally

def country_year_list(df):

    year = df["Year"].unique().tolist()
    year.sort()
    year.insert(0,"Over All")

    country = np.unique(df.reset_index()["region"].dropna().values).tolist()
    country.sort()
    country.insert(0,"Over All")

    return year,country

def fetch_medal_tally(df,year,country):
    
    medal_df =  df.drop_duplicates(subset=["Team","NOC","Games","Year","Season","City","Sport","Event","Medal"])
    medal_df_clean = medal_df.dropna(subset=["Medal"]).copy()
    medal_df_clean[["Gold", "Silver", "Bronze"]] = medal_df_clean[["Gold", "Silver", "Bronze"]].astype(int)

    flag = 0
    
    if year  == "Over All" and country == "Over All":
        temp_df = medal_df
        
    if year == "Over All" and country != "Over All": 
        flag = 1
        temp_df = medal_df[medal_df["region"] == country]
    
    if year != "Over All" and country == "Over All": 
        temp_df = medal_df[medal_df["Year"] == int(year)]
    
    if year != "Over All" and country != "Over All": 
        temp_df = medal_df[(medal_df["region"] == country) & (medal_df["Year"] == int(year))]

    if flag ==1:
        x = temp_df.groupby("Year")[["Gold", "Silver", "Bronze"]].sum().sort_values("Year").reset_index()
    else:
        x = temp_df.groupby("region")[["Gold", "Silver", "Bronze"]].sum().sort_values("Gold", ascending=False).reset_index()
    x["total"] = x["Gold"] + x["Silver"] + x["Bronze"]

    return x

def data_over_time(df,col):
    
    nation_over_time = df.drop_duplicates(["Year",col])["Year"].value_counts().reset_index().sort_values(["Year"])
    nation_over_time.rename(columns={"count":col},inplace=True)
    
    return nation_over_time

def most_wins(df,sport):
    
    temp_df = df.dropna(subset="Medal")
    if sport != "Over All":
        temp_df = temp_df[temp_df["Sport"] == sport]
    x = temp_df["Name"].value_counts().reset_index().head(15).merge(df,on="Name",how="left")
    x.rename(columns={"count":"Medals"},inplace=True)
    return x[["Name","Medals","Sport","region"]].drop_duplicates("Name")

def country_wise_medal_tally(df,country):

    temp_df = df.dropna(subset="Medal")
    temp_df = df.drop_duplicates(subset=["Team","NOC","Games","Year","Season","City","Sport","Event","Medal"])
    
    new_df = temp_df[temp_df["region"] == country]
    final_df = new_df.groupby("Year").count()["Medal"].reset_index()

    return final_df

def country_event_heatmap(df,country):

    if country == "Over All":
        temp_df = df.dropna(subset="Medal")
    else:
        temp_df = df.dropna(subset="Medal")
        temp_df = temp_df[temp_df["region"] == country]

    temp_df = df.drop_duplicates(subset=["Team","NOC","Games","Year","Season","City","Sport","Event","Medal"])
    
    pt = temp_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)

    return pt

def most_wins_country(df,country):
    
    temp_df = df.dropna(subset="Medal")
    temp_df = temp_df[temp_df["region"] == country]

    x = temp_df["Name"].value_counts().reset_index().head(10).merge(df,on="Name",how="left")
    x.rename(columns={"count":"Medals"},inplace=True)

    return x[["Name","Medals","Sport"]].drop_duplicates("Name")

def men_vs_women(df):
    athelete_df = df.drop_duplicates(subset=["Name"])
    men = athelete_df[athelete_df["Sex"] == "M"].groupby("Year").count()["Name"].reset_index()
    women = athelete_df[athelete_df["Sex"] == "F"].groupby("Year").count()["Name"].reset_index()

    final = men.merge(women,on="Year",how="left")
    final.columns = ["Year","Male","Female"]

    final.fillna(0,inplace=True)
    return final