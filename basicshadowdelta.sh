#!/bin/sh

python basicShadowDeltaListener.py -e a105md1y3ymvwb-ats.iot.us-east-1.amazonaws.com -r  certificates/root-ca.pem -k certificates/macDesktopThingprivate.pem -c certificates/macDesktopThing.pem -n macDesktopThing -t "auto/platedata"
