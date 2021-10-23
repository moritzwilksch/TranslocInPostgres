#%%
from get_data import fetch_data
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, ForeignKey

df, raw_response = fetch_data()