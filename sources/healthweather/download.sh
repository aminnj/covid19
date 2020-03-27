#!/usr/bin/env sh

mkdir -p data/states/


(cd data / && curl -O https://static.kinsahealth.com/weather_data.json)
(cd data / && curl -O https://static.kinsahealth.com/anomaly_map.json)
(cd data / && curl -O https://static.kinsahealth.com/zip_mapping.json)
(cd data / && curl -O https://static.kinsahealth.com/US_data.json)

states="
AL
AZ
AR
CA
CO
CT
DE
FL
GA
ID
IL
IN
IA
KS
KY
LA
ME
MD
MA
MI
MN
MS
MO
MT
NE
NV
NH
NJ
NM
NY
NC
ND
OH
OK
OR
PA
RI
SC
SD
TN
TX
UT
VT
VA
WA
WV
WI
WY
"
for state in $states ; do
    echo $state
    (cd data/states/ && curl -O -s https://static.kinsahealth.com/${state}_data.json)
done
