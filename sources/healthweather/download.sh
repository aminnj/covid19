#!/usr/bin/env sh


mkdir -p data/states/
function curl_zip() {
    name=$1
    outdir=$2
    curl -s https://static.kinsahealth.com/$name.json | gzip -c > $outdir/$name.json.gz
}


curl_zip weather_data data/
curl_zip anomaly_map data/
curl_zip zip_mapping data/
curl_zip US_data data/

states="AL AZ AR CA CO CT DE FL GA ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY"
for state in $states ; do
    echo $state
    curl_zip ${state}_data data/states/
done
