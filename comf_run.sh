#!/bin/bash

# A bash script to run COMF

blim="0.05"
ulim="0.15"
conv="0.98"

python3.6 areg.py ${blim} ${ulim}
python3.6 greg.py ${blim} ${ulim}
python3.6 freg.py ${blim} ${ulim}
