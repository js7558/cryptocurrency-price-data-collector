# cryptocurrency-price-data-collector
Python script that pulls pricing data for various combinations of exchange and cryptocoin from cryptowat.ch and stores them in csv for analysis later.

This script runs out of cron and collects pricing and volume data from cryptowat.ch for the combination of exchanges and coins you specify.  Storage is currently in .csv but this could easily be adapted to store data in a database.  

Requires pandas.  Perhaps helpful to upgrade them on your system before you start with 
pip install --upgrade pandas

Installation:
1) Install and upgrade pandas as above
2) Put script and config.ini on your system
3) Adjust config.ini for the exchanges and coins you are interested in. Instructions are in the file.
4) Schedule in cron. Here is how I configured it on my system for a 5 minute interval:
    */5 * * * * /home/jason/python/coin/collect.py >> /tmp/collect.out 2>&1

Find information about the cryptowat.ch api at https://cryptowat.ch/docs/api
