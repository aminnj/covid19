#!/usr/bin/env python3

import os
import re

import pandas as pd

import requests
import requests_cache
requests_cache.install_cache("cache")

def get_df1():
    # go to https://experience.arcgis.com/experience/96dd742462124fa0b38ddedb9b25e429/
    # click triple lines on the top right > data navigator > query with no selections (can only get 2k at a time)

    base_url = "https://services1.arcgis.com/CY1LXxl9zlJeBuRZ/arcgis/rest/services/Florida_COVID19_Case_Line_Data/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&outFields=*&outSR=102100&resultOffset={offset}&resultRecordCount={count}"
    # base_url = "https://services1.arcgis.com/CY1LXxl9zlJeBuRZ/arcgis/rest/services/Florida_COVID19_Case_Line_Data/FeatureServer/0/query?outFields=*&returnGeometry=false&resultOffset=70&resultRecordCount=10&f=json&where=1%3D1"
    # base_url = "https://opendata.arcgis.com/datasets/8ec01ce7236d4f20acf96371a6f4c0b7_0/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json&resultOffset={offset}&resultRecordCount={count}"

    def fetch_df(url):
        r = requests.get(url)
        js = r.json()
        features = [feature["attributes"] for feature in js["features"]]
        df = pd.DataFrame(features)
        return df

    batchsize = 2000 # arcgis query limit
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
    
    df = pd.concat(dfs, sort=True).reset_index(drop=True)
    return df

def get_df2():
    r = requests.get("https://hub.arcgis.com/datasets/FDOH::florida-covid19-case-line-data")
    code = re.search(r"rest/content/items/[a-z0-9]+/", r.content.decode())[0].split("/")[-2]
    url = f"https://opendata.arcgis.com/datasets/{code}_0.csv"
    print("[!] url overriden after visiting page and copying by hand.")
    url = "https://opendata.arcgis.com/datasets/37abda537d17458bae6677b8ab75fcb9_0.csv"
    print(url)
    return pd.read_csv(url)

df = get_df2()
# df = get_df1()

# df = df.drop_duplicates("OBJECTID")
# df.columns = df.columns.str.rstrip("_").str.lower()
df.columns = df.columns.str.lower()
print(df.columns)
print(df.head())
print(df.shape)
# print(df["fid"])
# df = df.drop_duplicates("objectid")
# df = df.drop(["objectid","origin","travel_related","contact","jurisdiction"],axis=1)
# df = df.drop_duplicates("objectid")
# df = df.drop_duplicates("fid")
df = df.drop_duplicates("objectid")
# df = df.drop(["objectid","origin","travel_related","contact","jurisdiction"],axis=1)
# df = df.drop(["fid","origin","travel_related","contact","jurisdiction"],axis=1)
df = df.drop(["objectid","origin","travel_related","contact","jurisdiction"],axis=1)

# print(df["case"])
# df["case"] = df["case"].str.split().str[0]
# df = df[df["case"] != "NA"]

# df["case"] = pd.to_datetime(df["case"]).dt.strftime("%Y-%m-%d")
# df["eventdate"] = pd.to_datetime(df["eventdate"], unit="ms").dt.strftime("%Y-%m-%d")
# print(df)

os.system("mkdir -p data/")
df.to_json("data/data.json.gz", orient="records", indent=4)
