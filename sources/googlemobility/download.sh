#!/usr/bin/env sh

# https://www.google.com/covid19/mobility/

# mkdir -p pdfs/
# cd pdfs/

# states="Alabama Alaska Arizona Arkansas California Colorado Connecticut Delaware Florida Georgia Hawaii Idaho Illinois Indiana Iowa Kansas Kentucky Louisiana Maine Maryland Massachusetts Michigan Minnesota Mississippi Missouri Montana Nebraska Nevada New_Hampshire New_Jersey New_Mexico New_York North_Carolina North_Dakota Ohio Oklahoma Oregon Pennsylvania Rhode_Island South_Carolina South_Dakota Tennessee Texas Utah Vermont Virginia Washington West_Virginia Wisconsin Wyoming"
# date="2020-03-29"
# for state in $states ; do
#     echo $state
#     curl -s -O https://www.gstatic.com/covid19/mobility/${date}_US_${state}_Mobility_Report_en.pdf
# done
# curl -o ${date}_US_US_Mobility_Report_en.pdf https://www.gstatic.com/covid19/mobility/${date}_US_Mobility_Report_en.pdf

mkdir -p data/
curl -s "https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv" | gzip -c > data/data.csv.gz
