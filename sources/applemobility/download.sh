#!/usr/bin/env sh

mkdir -p data/
# curl -s "https://covid19-static.cdn-apple.com/covid19-mobility-data/2007HotfixDev20/v2/en-us/applemobilitytrends-2020-04-27.csv" | gzip -c > data/data.csv.gz
# curl -s "https://covid19-static.cdn-apple.com/covid19-mobility-data/2007HotfixDev43/v2/en-us/applemobilitytrends-2020-04-29.csv" | gzip -c > data/data.csv.gz
# curl -s "https://covid19-static.cdn-apple.com/covid19-mobility-data/2007HotfixDev44/v2/en-us/applemobilitytrends-2020-04-30.csv" | gzip -c > data/data.csv.gz
# curl -s "https://covid19-static.cdn-apple.com/covid19-mobility-data/2007HotfixDev46/v2/en-us/applemobilitytrends-2020-05-02.csv" | gzip -c > data/data.csv.gz
# curl -s "https://covid19-static.cdn-apple.com/covid19-mobility-data/2007HotfixDev51/v2/en-us/applemobilitytrends-2020-05-07.csv" | gzip -c > data/data.csv.gz
# curl -s "https://covid19-static.cdn-apple.com/covid19-mobility-data/2007HotfixDev58/v2/en-us/applemobilitytrends-2020-05-12.csv" | gzip -c > data/data.csv.gz
# curl -s "https://covid19-static.cdn-apple.com/covid19-mobility-data/2008HotfixDev40/v3/en-us/applemobilitytrends-2020-05-22.csv" | gzip -c > data/data.csv.gz
# curl -s "https://covid19-static.cdn-apple.com/covid19-mobility-data/2008HotfixDev43/v3/en-us/applemobilitytrends-2020-05-25.csv" | gzip -c > data/data.csv.gz
# curl -s "https://covid19-static.cdn-apple.com/covid19-mobility-data/2009HotfixDev13/v3/en-us/applemobilitytrends-2020-05-29.csv" | gzip -c > data/data.csv.gz
# curl -s "https://covid19-static.cdn-apple.com/covid19-mobility-data/2009HotfixDev23/v3/en-us/applemobilitytrends-2020-06-06.csv" | gzip -c > data/data.csv.gz

baseurl="https://covid19-static.cdn-apple.com/covid19-mobility-data/current/v3/"
jsoninfo=$(curl -s "$baseurl/index.json")
csvpath=$(echo $jsoninfo | python -c 'import sys; import json; print(json.loads(sys.stdin.readline())["regions"]["en-us"]["csvPath"])')
url="$baseurl/$csvpath"
curl -s "$url" | gzip -c > data/data.csv.gz

# curl -s "https://covid19-static.cdn-apple.com/covid19-mobility-data/current/v3/en-us/applemobilitytrends.json" | gzip -c > data/data.json.gz
