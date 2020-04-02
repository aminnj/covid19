# Did this to get covid information for each state
# curl https://covidtracking.com/api/states/info | jq '.' > links.json
# then manually read through and logged the age and gender distribution
# for cases and deaths

import pandas as pd

data = []
with open("data/raw_data.txt","r") as fh:
    parts = fh.read().split("\n\n")
    cols = None
    for part in parts:
        part = part.strip()
        if not part: continue
        lines = part.splitlines()
        state, date, url = lines[0].split(",",2)
        for line in lines[1:]:
            if "cases" in line:
                cols = line.split(",")
                continue
            vals = line.split(",")
            row = dict(zip(cols,vals))
            row["state"] = state
            row["date"] = date.replace("/","-")
            # row["url"] = url
            data.append(row)

dfc = pd.DataFrame(data)

df_ages = dfc[~dfc["age"].isna()].drop(["gender"],axis=1).reset_index(drop=True)
df_genders = dfc[~dfc["gender"].isna()].drop(["age"],axis=1).reset_index(drop=True)

df_ages.to_json("data/df_ages.json",orient="records",indent=4)
df_genders.to_json("data/df_genders.json",orient="records",indent=4)


