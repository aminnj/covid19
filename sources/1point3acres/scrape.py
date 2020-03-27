#!/usr/bin/env python3

# pip3 install --user -U pandas requests requests_cache bs4

import time
import pandas as pd
import os
import requests
import requests_cache
import json
from bs4 import BeautifulSoup

requests_cache.install_cache(
    "cache", expire_after=5 * 3600, backend="sqlite", fast_save=True
)

base_url = "https://coronavirus.1point3acres.com"
headers = {
    "authority": "coronavirus.1point3acres.com",
    "pragma": "no-cache",
    "cache-control": "no-cache",
    "sec-fetch-dest": "script",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "dnt": "1",
    "accept": "*/*",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "no-cors",
    "referer": "https://coronavirus.1point3acres.com/en",
    "accept-language": "en-US,en;q=0.9",
}


def get_content(url):
    r = requests.get(url, headers=headers)
    print(f"[GET {r.status_code}] {url} (from_cache={r.from_cache}, elapsed={r.elapsed})")
    if not r.from_cache:
        time.sleep(1)
    return r.content.decode()


# Get the main page and see which assets are loaded.
# This is equivalent to getting the relevant webpack .js files from
# https://coronavirus.1point3acres.com/_next/static/chunks/
main_content = get_content(base_url)

js_content = None
bs = BeautifulSoup(main_content, features="lxml")
for tag in bs.find_all("script"):
    src = tag.get("src", "")
    if not src.startswith("/_next"):
        continue
    if not src.endswith(".js"):
        continue
    if "/chunks/" not in src:
        continue
    hashlen = len(src.rsplit("/", 1)[-1].split(".", 1)[0])
    if hashlen != 40:
        continue
    url = base_url + src

    needle = """JSON.parse('[{"confirmed_date":"""
    haystack = get_content(url)
    # print(len(haystack))
    if len(haystack) < 1e6:
        # the real json is >1MB
        continue
    if needle not in haystack:
        continue
    js_content = haystack
    print(f"Found right script: {url}")
    break

if not js_content:
    raise RuntimeError("Unable to find the .js file with data")

rawjs = (
    (
        """[{"""
        + js_content.split("""JSON.parse('[{""", 2)[-1].split("""}]')}""", 1)[0]
        + """}]"""
    )
    .replace("\\'", "'")
    .replace('\\\\"', "")
    .replace("\\x", "")
)
js = json.loads(rawjs)

data_deaths = []
data_cases = []
for irow,row in enumerate(js):
    # As of Mar 24 need to make separate API call to get links, and comments. THANKS.
    # As of Mar26 API doesn't work, and ids are not in the rows
    # f"https://instant.1point3acres.com/v1/coronavirus/cases/{id}?country=US"
    d = dict(
        date=row["confirmed_date"] + "/20",
        state=row["state_name"],
        county=row["county"],
        # links=row["links"],
        # description=row.get("comments_en", ""),
        gender=row.get("gender", "").replace("女", "F").replace("男", "M"),
        age=row.get("age_range", None),
    )

    deaths = row.get("die_count", 0)
    for _ in range(deaths):
        data_deaths.append(dict(**d, is_death=True, ngroup=deaths))
    cases = row["people_count"]
    for _ in range(cases):
        data_cases.append(dict(**d, is_death=False, ngroup=cases))

df_total = pd.DataFrame(data_deaths + data_cases)

nrows = len(df_total)
ndeaths = df_total["is_death"].sum()
ncases = nrows - ndeaths
print(f"Total rows: {nrows} ({ndeaths} deaths, {ncases} cases)")

os.system("mkdir -p data/")
output_name = "data/cases_and_deaths.json.gz"
df_total.to_json(output_name, orient="records", indent=4)
print(f"Wrote {output_name}")
