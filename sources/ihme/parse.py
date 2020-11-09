#!/usr/bin/env python3

import os
import re
import sys

import pandas as pd

import requests
import requests_cache
requests_cache.install_cache("cache",expire_after=24*60*60)

dfc = pd.read_csv("data/Summary_stats_all_locs.csv")
# US states
df_states = dfc[dfc.location_id.between(523,573)]

ids = df_states["location_id"].values

locstr = "&".join(["location[]={}".format(i) for i in ids])

url = f"https://covid19.healthdata.org/api/data/hospitalization?{locstr}&measure=prop_mask_use&scenario[]=6&scenario[]=1"

r = requests.get(url)
js = r.json()
keys = js.keys()
df_masks = pd.DataFrame(js["values"], columns=js["keys"])

df_masks = df_masks.merge(df_states[["location_id","location_name"]], on="location_id")

df_masks = df_masks.query("data_type_name=='observed'").drop([
    "data_type_name","upper","lower","date_upper","date_lower","covid_measure_name","scenario_id","date_mean",
    ],axis=1)

df_masks.to_json("data/df_masks.jsonl.gz", orient="records", lines=True)
