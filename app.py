import streamlit as st
import numpy as np
import pandas as pd
import preprocesser,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


df = pd.read_csv("athlete_events.xls")
region_df = pd.read_csv("noc_regions.xls")

df = preprocesser.preprocess(df,region_df)

st.sidebar.title("Olymics Analysis")
user_menu = st.sidebar.radio("Select An Option",("Medal Tally","Overall Analysis","Country Wise Analysis","Athlete Wise Analysis"))

# st.dataframe(df)

if user_menu == "Medal Tally":

    # For medal tally
    st.sidebar.header("Medal Tally")
    year,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",year)
    selected_country = st.sidebar.selectbox("Select Country",country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == "Over All" and selected_country == "Over All":
        st.title("Over All Analysis")
        
    elif selected_year == "Over All" and selected_country != "Over All":
        st.title(f"{selected_country} Analysis")
        

    elif selected_year != "Over All" and selected_country == "Over All": 
        st.title(f"Year {selected_year} Analysis")
        
    elif selected_year != "Over All" and selected_country != "Over All": 
        st.title(f"Year {selected_year} , {selected_country} Analysis")
    st.table(medal_tally)

if user_menu == "Overall Analysis":

    edition = df["Year"].unique().shape[0] - 1
    cities = df["City"].unique().shape[0] 
    sport = df["Sport"].unique().shape[0] 
    events = df["Event"].unique().shape[0] 
    nations = df["region"].unique().shape[0] 
    atheletes = df["Name"].unique().shape[0]
    
    st.title("Top Statistics")
    col1 ,col2 ,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(edition)
    with col2:
        st.header("Cities")
        st.title(cities)
    with col3:
        st.header("Sport")
        st.title(sport)
    
    st.markdown("---")

    col1 ,col2 ,col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Atheletes")
        st.title(atheletes)

    # Nations
    st.markdown("---")
    st.title("Total Nations Participations")
    st.markdown("---")

    nations_over_time = helper.data_over_time(df,"region")
    fig = px.line(nations_over_time,x="Year",y="region")
    st.plotly_chart(fig)

    # Events 
    st.markdown("---")
    st.title("Events Over Years")
    st.markdown("---")
    
    events_over_time = helper.data_over_time(df,"Event")
    fig = px.line(events_over_time,x="Year",y="Event")
    st.plotly_chart(fig)

    # Atheletes Over Years
    st.markdown("---")
    st.title("Atheletes Over Years")
    st.markdown("---")
    
    atheletes_over_time = helper.data_over_time(df,"Name")
    fig = px.line(atheletes_over_time,x="Year",y="Name")
    st.plotly_chart(fig)

    # Sport Over Time
    st.markdown("---")
    st.title("Number Of Events Over Time(Every Sport)")
    st.markdown("---")
    
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(["Year","Sport","Event"])
    ax = sns.heatmap(x.pivot_table(index="Sport",columns="Year",values="Event",aggfunc="count").fillna(0).astype(int),annot=True) # nnot represent numbers
    st.pyplot(fig)

    # Most Succesful Atheletes 
    st.markdown("---")
    st.title("Most Succesful Atheletes")
    st.markdown("---")
    
    sport_list = df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,"Over All")

    selected_sport = st.selectbox("Select Sport",sport_list)
    x = helper.most_wins(df,selected_sport)
    st.table(x)

if user_menu == "Country Wise Analysis":
    
    # Chart Plotting
    st.sidebar.title("Country Wise Analysis")
    st.markdown("---")

    country_list = df["region"].dropna().unique().tolist()
    country_list.sort()
    country_list.insert(0,"Over All")

    sl_country = st.sidebar.selectbox("Select Country",country_list)
    country_wise = helper.country_wise_medal_tally(df,sl_country)
    
    fig = px.line(country_wise,x="Year",y="Medal")
    st.title(f"{sl_country} Medal Tally Over The Years")
    st.plotly_chart(fig)

    # Heat Map
    pt = helper.country_event_heatmap(df,sl_country)

    fig,ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pt,annot=True)

    st.markdown("---")
    st.title(f"{sl_country} excels in the following sports")
    st.markdown("---")
    st.pyplot(fig)

    # Atheletes country wise
    st.markdown("---")
    st.title(f"Top 10 Atheletes of {sl_country}")
    top10_df = helper.most_wins_country(df,sl_country)
    st.table(top10_df)

if user_menu == "Athlete Wise Analysis":

    athelete_df = df.drop_duplicates(subset=["Name"])

    x1 = athelete_df["Age"].dropna()
    x2 = athelete_df[athelete_df["Medal"] == "Gold"]["Age"].dropna()
    x3 = athelete_df[athelete_df["Medal"] == "Bronze"]["Age"].dropna()
    x4 = athelete_df[athelete_df["Medal"] == "Silver"]["Age"].dropna()

    fig = ff.create_distplot([x1,x2,x3,x4],["Over All Age","Gold Medalist","Bronze Medalist","Silver Medalist"],show_hist=False,show_rug=False)
    st.title("Distribution of Age")
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)

    # men vs women
    st.markdown("---")
    st.title("Men Vs Women Participation Over the Years")
    st.markdown("---")
    final = helper.men_vs_women(df)
    fig=px.line(final,x="Year",y=["Male","Female"])
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)