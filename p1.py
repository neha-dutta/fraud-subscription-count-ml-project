import pandas as pd
import streamlit as st
import plotly.express as px
df=pd.read_csv("Transaction Data_19th to 21st August 2022.csv")
st.write("Data set loaded for transaction , kindly apply filters to show")
df=df[df.duplicated("Phone")]
df["Date"]=pd.to_datetime(df["Date"]).dt.strftime('%Y-%m-%d')
df=df[df.duplicated("Date")]
date_options=df["Date"].unique().tolist()
select_date=st.multiselect("Which dates you want to see?",date_options)
df_up=df[df["Date"].isin(select_date)]
sub_opt=df_up["Requested Amount"].unique().tolist()
select_sub=st.multiselect("Which plan you want to select?",sub_opt)
df_up_sub=df_up[df_up["Requested Amount"].isin(select_sub)]

fig=px.bar(df_up_sub,x="Requested Amount",color="Date",)
fig.update_layout(width=800)
st.write(fig)