import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

df_n=pd.read_csv("o9lya07lijgg_2022-08-18T180000_4b4b4661a0bb79b34174ff5307e4bad1_c3575d.csv")

# st.write()
nets=df_n["{network_name}"].unique().tolist()
# st.write(nets)
# st.write(df_n.columns)
df_n = df_n.dropna(axis = 1, how = 'all')
# st.write(df_n.columns)
df_n=df_n[df_n.duplicated("[Phone]")]
networks=df_n["{network_name}"].unique().tolist()
select_network=st.multiselect("Which network you want to choose?",nets)
df_up=df_n["{network_name}"].isin(select_network).value_counts()
st.write(df_up)
a=df_up.plot.bar(x='{network_name}', y='val', rot=0)
st.write(a)
