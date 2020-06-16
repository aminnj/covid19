#!/usr/bin/env sh

( cd nytimes/ && ./download.py )
( cd googlemobility/ && ./download.sh )
( cd applemobility/ && ./download.sh )
( cd florida/ && ./download.py )
( cd excessdeaths/ && ./download.sh )
