#!/usr/bin/env sh

# https://www.cdc.gov/nchs/nvss/vsrr/covid19/excess_deaths.htm

mkdir -p data/
curl -s "https://data.cdc.gov/api/views/xkkf-xrst/rows.csv?accessType=DOWNLOAD&bom=true&format=true%20target=" | gzip -c > data/data.csv.gz

