#!/usr/bin/env python3

import os
import pandas as pd

os.system("mkdir -p data/")
dfc = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv")
dfc = dfc.drop(["fips"],axis=1)

nunique_counties = dfc["county"].nunique()
nunique_states = dfc["state"].nunique()
first_date = dfc["date"].min()
last_date = dfc["date"].max()
current_cases = dfc[dfc["date"] == last_date]["cases"].sum()
print(f"""
Read csv with:
- {nunique_counties} unique counties
- {nunique_states} unique states
- dates between {first_date} and {last_date}
- {current_cases} current_cases
""")
dfc.to_json("data/cases.json.gz", orient="records", indent=4)

