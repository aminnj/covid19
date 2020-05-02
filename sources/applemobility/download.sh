#!/usr/bin/env sh

mkdir -p data/
# curl -s "https://covid19-static.cdn-apple.com/covid19-mobility-data/2007HotfixDev20/v2/en-us/applemobilitytrends-2020-04-27.csv" | gzip -c > data/data.csv.gz
# curl -s "https://covid19-static.cdn-apple.com/covid19-mobility-data/2007HotfixDev43/v2/en-us/applemobilitytrends-2020-04-29.csv" | gzip -c > data/data.csv.gz
curl -s "https://covid19-static.cdn-apple.com/covid19-mobility-data/2007HotfixDev44/v2/en-us/applemobilitytrends-2020-04-30.csv" | gzip -c > data/data.csv.gz

