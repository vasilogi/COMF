#!/bin/bash

# A bash script to run COMF

blim="0.85"
ulim="0.95"
conv="0.98"

python3.6 areg.py ${blim} ${ulim}
python3.6 greg.py ${blim} ${ulim}
python3.6 freg.py ${blim} ${ulim}
python3.6 ranking_models.py ${blim} ${ulim}
