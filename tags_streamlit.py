import pandas as pd
import regex as re
import streamlit as st
import itertools
<<<<<<< HEAD
import plotly.express as px
from collections import Counter

countries = pd.read_csv("countries.gzip",compression='gzip')
tagsSQL = pd.read_csv("tagsSQL.gzip",compression='gzip')
=======
import pickle
from collections import Counter

<<<<<<< HEAD
countries = pd.read_csv("countries.csv")
tagsSQL = pd.read_csv("tagsSQL.csv")
>>>>>>> parent of a7d92cd (csv files)
=======
countries = pickle.load(open('countries.pickle','rb'))
tagsSQL = pickle.load(open("tagsSQL.pickle","rb"))
>>>>>>> parent of 12675aa (add streamlit)

def country_transform(raw):
    global countries
    return list(countries[countries['id']==raw]['country_full'])[0] if raw in set(countries['id']) else ''

st.set_page_config(
    page_title="Populairste tags per land",
    page_icon="✅",
    layout="wide",
)

LAND = st.selectbox(
    label='Kies een land waarvoor je de populairste tags wilt zien',
    options=list(countries['id']),
    format_func=country_transform
)
TOP_N = st.number_input(
    label='Kies het aantal tags wat je wilt zien',
    min_value=1,
    max_value=100,
    value=20
)



tags = tagsSQL.copy()
tags['tag'] = tags['tag'].map(lambda x: [t.strip() for t in str(x).split(',')])

df = pd.DataFrame(tags.groupby('studieland')['tag'].apply(lambda x: list(itertools.chain(*x))))
df['counts'] = df['tag'].map(lambda x: Counter(x).most_common(TOP_N))

counts_land = {k:[v] for k,v in df['counts'][LAND]}

counts_df = pd.DataFrame(
    counts_land
    ).transpose(
    ).reset_index(
    ).rename({'index':'tag',
              0:'gebruikt'},axis=1)

fig = px.bar(x=counts_df['tag'], y=counts_df['gebruikt'], color=counts_df['tag'])
fig.update_xaxes(type='category')
st.plotly_chart(fig, use_container_width=True)
