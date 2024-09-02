import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Get Helper Function
def create_yearly_air_quality_df(df):
    yearly_air_quality_df = df.groupby(by=['station', 'year']).agg({
        'PM2.5': 'mean',
        'PM10': 'mean',
    })
    return yearly_air_quality_df

def create_corr_matrix(df):
    fig, ax = plt.subplots(figsize=(10, 8))
    corr_matrix = df.select_dtypes('number').corr()
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', ax=ax)
    ax.set_title("Air Quality Correlation Heatmap", fontsize=15, loc="center")
    ax.set_xlabel(None)
    ax.set_ylabel(None)

    return fig

def create_bystation_df(df, pm_type='PM2.5'):
    bystation_df = df.groupby(by='station').agg({
        'PM2.5': 'mean',
        'PM10': 'mean',
        'SO2': 'mean',
        'NO2': 'mean',
        'CO': 'mean',
        'O3': 'mean'
    })
    if pm_type == 'PM10':
        bystation_df = bystation_df.sort_values(by='PM10', ascending=False)
    else:
        bystation_df = bystation_df.sort_values(by='PM2.5', ascending=False)
    return bystation_df

# Load Dataset
air_all_df = pd.read_csv('dashboard/air_all_station_data.csv')
air_main_df = air_all_df
bystation_df_pm25 = create_bystation_df(air_main_df, pm_type='PM2.5')
bystation_df_pm10 = create_bystation_df(air_main_df, pm_type='PM10')

# HEADER
st.header('Air Quality Dashboard :cloud:')

st.subheader('Air Quality Trend from 2013 to 2017')
station_select = st.selectbox(
    label='Select Station',
    options=air_all_df['station'].unique(),
)

yearly_air_quality_df = create_yearly_air_quality_df(air_main_df)
all_stations = air_all_df['station'].unique()
fig, ax = plt.subplots(figsize=(10, 7))
for station in all_stations:
    if station != station_select:
        continue
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label='PM10', value=round(bystation_df_pm10.loc[station, 'PM10'],2))
    with col2:
        st.metric(label='PM2.5', value=round(bystation_df_pm25.loc[station, 'PM2.5'], 2))
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label='SO2', value=round(bystation_df_pm10.loc[station, 'SO2'],2))
    with col2:
        st.metric(label='NO2', value=round(bystation_df_pm25.loc[station, 'NO2'], 2))
    with col3:
        st.metric(label='CO', value=round(bystation_df_pm10.loc[station, 'CO'],2))
    with col4:
        st.metric(label='O3', value=round(bystation_df_pm25.loc[station, 'O3'], 2))
    sns.lineplot(
        x='year',
        y='PM2.5',
        data=yearly_air_quality_df.loc[station],
        color='red',
        marker='o',
        linestyle='solid',
        linewidth=3,
        label='PM2.5',
    )
    sns.lineplot(
        x='year',
        y='PM10',
        data=yearly_air_quality_df.loc[station],
        color='orange',
        marker='o',
        linestyle='solid',
        linewidth=3,
        label='PM10',
    )
    ax.set_title(f"{station} Air Pollution from 2013 to 2017", fontsize=20, loc="center")
    ax.set_xlabel(None)
    ax.set_ylabel('PM2.5/PM10', fontsize=15)
    ax.set_xticks(yearly_air_quality_df.loc[station].index)

st.pyplot(fig)

st.subheader('Air Quality by Station')

col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(10, 10))
    colors = ['#C01919','#F4BB94','#F4BB94','#F4BB94','#F4BB94','#F4BB94','#F4BB94','#F4BB94','#F4BB94','#F4BB94','#F4BB94','#78B21F']
    sns.barplot(y=bystation_df_pm25.index, x='PM2.5', data=bystation_df_pm25, ax=ax, palette=colors)
    ax.set_title("Average PM2.5 by Station", fontsize=30, loc="center")
    ax.set_xticklabels(ax.get_xticklabels(), fontsize=22)
    ax.tick_params(axis="y", labelsize=22)
    st.pyplot(fig)
with col2:
    fig, ax = plt.subplots(figsize=(10, 10))
    colors = ['#C01919','#F4BB94','#F4BB94','#F4BB94','#F4BB94','#F4BB94','#F4BB94','#F4BB94','#F4BB94','#F4BB94','#F4BB94','#78B21F']
    sns.barplot(y=bystation_df_pm10.index, x='PM10', data=bystation_df_pm10, ax=ax, palette=colors)
    ax.set_title("Average PM10 by Station", fontsize=30, loc="center")
    ax.set_xticklabels(ax.get_xticklabels(), fontsize=22)
    ax.tick_params(axis="y", labelsize=22)
    ax.invert_xaxis()
    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()
    st.pyplot(fig)
st.subheader('Correlation Matrix of Air Quality')
st.pyplot(create_corr_matrix(air_main_df))

st.caption('Dashboard made by: Muhammad Zydan Priambada')
st.caption('Email: dan80308@gmail.com')
st.caption('Dicoding username: itsdan911')