#!/usr/bin/env sh

# https://data.cdc.gov/Case-Surveillance/COVID-19-Case-Surveillance-Public-Use-Data/vbim-akqf

mkdir -p data/
# curl -s "https://data.cdc.gov/api/views/vbim-akqf/rows.csv?accessType=DOWNLOAD&bom=true&format=true%20target=" | gzip -c > data/data.csv.gz
curl "https://data.cdc.gov/api/views/vbim-akqf/rows.csv?accessType=DOWNLOAD&bom=true&format=true%20target=" | gzip -c > data/data.csv.gz


# Column Name	Description	Type
# cdc_report_dt Initial case report date to CDC Date & Time
# pos_spec_dt Date of first positive specimen collection Date & Time
# onset_dt Symptom onset date, if symptomatic Date & Time
# current_status Case Status: Laboratory-confirmed case; Probable case Plain Text
# sex Sex: Male; Female; Unknown; Other Plain Text
# age_group Age Group: 0 - 9 Years; 10 - 19 Years; 20 - 39 Years; 40 - 49 Years; 50 - 59 Years; 60 - 69 Years; 70 - 79 Years; 80 + Years Plain Text
# Race and ethnicity (combined) Race and ethnicity (combined): Hispanic/Latino; American Indian / Alaska Native, Non-Hispanic; Asian, Non-Hispanic; Black, Non-Hispanic; Native Hawaiian / Other Pacific Islander, Non-Hispanic; White, Non-Hispanic; Multiple/Other, Non-Hispanic Plain Text
# hosp_yn Hospitalization status Plain Text
# icu_yn ICU admission status Plain Text
# death_yn Death status Plain Text
# medcond_yn Presence of underlying comorbidity or disease Plain Text

