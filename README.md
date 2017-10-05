# cryptocurrency-price-data-collector
Python script that pulls pricing data for various combinations of exchange and cryptocoin from cryptowat.ch and stores them in csv for analysis later.

This script runs out of cron and collects pricing and volume data from cryptowat.ch for the combination of exchanges and coins you specify.  Storage is currently in .csv but this could easily be adapted to store data in a database.  

REQUIREMENTS:
Requires pandas.  Perhaps helpful to upgrade them on your system before you start with 
pip install --upgrade pandas

INSTALLATION:
1) Install and upgrade pandas as above
2) Put script and config.ini on your system
3) Adjust config.ini for the exchanges and coins you are interested in. Instructions are in the file.
4) Schedule in cron. Here is how I configured it on my system for a 5 minute interval:
    */5 * * * * /home/jason/python/coin/collect.py >> /tmp/collect.out 2>&1

OUTPUT: 
Output is csv delimited as follows:
TIMESTAMP, COINPAIR, EXCHANGE, PRICE, VOLUME
1507244702.66,ethbtc,bitfinex,0.068182,30078.979
1507244702.66,ethbtc,gdax,0.06819,4308.9624
1507244702.66,ethbtc,bitstamp,0.06833975,2486.6814
1507244702.66,ethbtc,kraken,0.06817,10156.437
1507244702.66,ethbtc,gemini,0.06824,1814.0734
1507245002.51,ethbtc,bitfinex,0.068076,30087.805
1507245002.51,ethbtc,gdax,0.06818,4327.4053
1507245002.51,ethbtc,bitstamp,0.0683,2485.305
1507245002.51,ethbtc,kraken,0.06808,10159.6875

Perhaps extraneous to write the coinpair to the .csv since the filename has it also, but it is easy enough to filter out or ignore.

Working on other tools to make use of these data (i.e. figure out trading strategies), so check back or feel free to send me ideas/requests. 

Find information about the cryptowat.ch api at https://cryptowat.ch/docs/api
