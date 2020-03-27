#!/usr/bin/env python3

import os
import pandas as pd

os.system("mkdir -p data/")
dfc = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv")
dfc.to_json("data/cases.json.gz", orient="records", indent=4)
