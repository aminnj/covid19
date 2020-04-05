#!/usr/bin/env python3

import pandas as pd
import os

import requests
# import requests_cache
# requests_cache.install_cache("cache")

# go to https://experience.arcgis.com/experience/96dd742462124fa0b38ddedb9b25e429/
# triple lines on the top right > data navigator > query with no selections (can only get 2k at a time)

base_url = "https://services1.arcgis.com/CY1LXxl9zlJeBuRZ/arcgis/rest/services/Florida_COVID19_Case_Line_Data/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=true&spatialRel=esriSpatialRelIntersects&outFields=County%2CAge%2CGender%2CJurisdiction%2CTravel_related%2COrigin%2CEDvisit%2CHospitalized%2CDied%2CContact%2CCase_%2CEventDate%2CObjectId&outSR=102100&resultOffset={offset}&resultRecordCount={count}"

def fetch_df(url):
    r = requests.get(url)
    js = r.json()
    features = [feature["attributes"] for feature in js["features"]]
    df = pd.DataFrame(features)
    return df

batchsize = 2000
dfs = []
for offset in range(0,int(1e6),batchsize):
    url = base_url.format(offset=offset, count=batchsize)
    df = fetch_df(url)
    dfs.append(df)
    nrows = len(df)
    print(f"Fetched {nrows} rows from offset of {offset} and batchsize of {batchsize}")
    if nrows != batchsize:
        print("Didn't get a full batch of rows, so this must be the last page")
        break

df = pd.concat(dfs, sort=True).reset_index(drop=True).drop_duplicates("ObjectId")
df.columns = df.columns.str.rstrip("_").str.lower()
df = df.drop(["objectid","origin","travel_related","contact","jurisdiction"],axis=1)

df["case"] = pd.to_datetime(df["case"], unit="ms").dt.strftime("%Y-%m-%d")
df["eventdate"] = pd.to_datetime(df["eventdate"], unit="ms").dt.strftime("%Y-%m-%d")
print(df)

os.system("mkdir -p data/")
df.to_json("data/data.json.gz", orient="records", indent=4)
