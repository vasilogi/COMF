#!/bin/bash

# A bash script to run COMF

blim="0.01"
ulim="0.99"
conv="0.98"

python3.7 areg.py ${blim} ${ulim}
python3.7 greg.py ${blim} ${ulim}
python3.7 freg.py ${blim} ${ulim}
python3.7 ranking_models.py ${blim} ${ulim}
