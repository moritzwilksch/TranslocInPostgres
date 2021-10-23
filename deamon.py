#%%
import datetime
from sqlalchemy.sql.schema import ForeignKey
from get_data import fetch_data
from sqlalchemy.orm import Session, relationship
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    DateTime,
    Float,
)

df, raw_data = fetch_data()
df["scrape_time"] = datetime.datetime.now()

data_subset_cols = [
    "id",
    "scrape_time",
    "lat",
    "lng",
    "speed",
    "heading",
]

#%%
metadata = MetaData()
engine = create_engine("postgresql://postgres:translocPassword@localhost:5431")
session = Session(bind=engine)

# raw_response = Table(
#     "raw_response",
#     metadata,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("json_data", JSON),
# )

# data_subset = Table(
#     "data_subset",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("scrape_time", DateTime),
#     Column("lat", Float),
#     Column("lng", Float),
#     Column("speed", Float),
#     Column("heading", Integer),
#     Column("raw_response", ForeignKey("raw_response.id")),
# )
#
# raw_response.create(engine, checkfirst=True)
# data_subset.create(engine, checkfirst=True)

#%%


class RawResponse(Base):
    __tablename__ = "raw_response"
    id = Column(Integer, primary_key=True, autoincrement=True)
    json_data = Column(JSON)
    data_rows = relationship("DataSubset", backref="raw_response")


class DataSubset(Base):
    __tablename__ = "data_subset"
    id = Column(Integer, primary_key=True, autoincrement=True)
    scrape_time = Column(DateTime, primary_key=True)
    lat = Column(Float)
    lng = Column(Float)
    speed = Column(Float)
    heading = Column(Integer)
    raw_response_id = Column(ForeignKey("raw_response.id"))


Base.metadata.create_all(engine)

#%%
# Insert single row with FK relationship
if False:
    rr_toinsert = RawResponse(json_data=raw_data)
    ds_toinsert = DataSubset(
        **df[data_subset_cols].iloc[0].to_dict(), raw_response=rr_toinsert.id
    )

    # establish Foreign Key relationship
    rr_toinsert.data_rows.append(ds_toinsert)

    session.add(rr_toinsert)
    session.flush()
    session.add(ds_toinsert)
    session.commit()

#%%
rr_toinsert = RawResponse(json_data=raw_data)

for record in df[data_subset_cols].to_dict(orient="records"):
    ds_toinsert = DataSubset(**record, raw_response=rr_toinsert.id)
    rr_toinsert.data_rows.append(ds_toinsert)
    session.add(ds_toinsert)


session.commit()

#%%
