#!/usr/bin/env python3

import pandas as pd
import os


# https://abbreviations.yourdictionary.com/articles/state-abbrev.html
raw = """
Alabama - AL
Alaska - AK
Arizona - AZ
Arkansas - AR
California - CA
Colorado - CO
Connecticut - CT
Delaware - DE
Florida - FL
Georgia - GA
Hawaii - HI
Idaho - ID
Illinois - IL
Indiana - IN
Iowa - IA
Kansas - KS
Kentucky - KY
Louisiana - LA
Maine - ME
Maryland - MD
Massachusetts - MA
Michigan - MI
Minnesota - MN
Mississippi - MS
Missouri - MO
Montana - MT
Nebraska - NE
Nevada - NV
New Hampshire - NH
New Jersey - NJ
New Mexico - NM
New York - NY
North Carolina - NC
North Dakota - ND
Ohio - OH
Oklahoma - OK
Oregon - OR
Pennsylvania - PA
Rhode Island - RI
South Carolina - SC
South Dakota - SD
Tennessee - TN
Texas - TX
Utah - UT
Vermont - VT
Virginia - VA
Washington - WA
West Virginia - WV
Wisconsin - WI
Wyoming - WY
"""

# https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/
# dfc = pd.read_csv("data/co-est2019-alldata.csv", encoding = "ISO-8859-1")
dfc = pd.read_csv("https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv", encoding = "ISO-8859-1")
dfc = dfc[["STNAME","CTYNAME","POPESTIMATE2019"]].rename({"STNAME":"state","CTYNAME":"county","POPESTIMATE2019":"population"},axis=1)

dfc = dfc[dfc["state"] != dfc["county"]]

# NOTE, to play nice with county covid data, put 5 counties' populations into New York County, then delete
# 4 of them
cs = ["Kings County", "Queens County", "Bronx County", "Richmond County"]
df = dfc.set_index(["state", "county"])
nypop = 0.
for c in cs:
    nypop += df.loc[("New York",c)]["population"]
# add these 4 county populations into New York County
dfc.loc[(dfc["state"] == "New York") & (dfc["county"] == "New York County"), "population"] += nypop
# then drop the 4 counties
dfc = dfc[~((dfc["state"] == "New York") & (dfc["county"].isin(cs)))]

abbrev_mapping = dict(map(lambda x: x.split(" - "), raw.strip().splitlines()))
dfc["state"] = dfc["state"].map(abbrev_mapping)

os.system("mkdir -p data/")
dfc.to_json("data/county_populations.json.gz", orient="records", indent=4)


