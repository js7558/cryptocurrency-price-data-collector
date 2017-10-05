#!/usr/bin/python
#
##################################################################################
# MIT License
# 
# Copyright (c) 2017 Jason Shaw
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 
##################################################################################
# Discover and collect pricing data from cryptowat.ch for a given list of exchanges and coins and store in csv 
#
# ### Configure config.ini before you start ###
# exchanges: The exchange(s) we want to collect data from
# basecoins: The coin being compared to. For example, lots of cryptocurrencies are denominated in USD or BTC 
#               so it may make sense to use these as the basis for comparison.
# altcoins:  The coin being compared to basecoin.  
# collection_path: The path to write your data to
# 
# Run this in cron every minute (or 5 minutes) to build up a body of pricing data that can be used to 
# perform some data analysis on to help formulate coin trading strategies.
#       */5 * * * * /home/jason/python/coin/collect.py >> /tmp/collect.out 2>&1
#
# version 0.1
#       - initial release

import requests
import time
import pandas as pd
import ConfigParser
import os
import sys

def readConfig():
        # read in configuration
        config = ConfigParser.ConfigParser()
        # this makes it work via cron
        scriptDirectory = os.path.dirname(os.path.realpath(__file__))
        settingsFilePath = os.path.join(scriptDirectory, "config.ini")
        config.readfp(open(settingsFilePath, "r"))

        exchanges = [e.strip() for e in config.get('DEFAULT','exchanges').split(',')]
        basecoins = [e.strip() for e in config.get('DEFAULT','basecoins').split(',')]
        altcoins  = [e.strip() for e in config.get('DEFAULT','altcoins').split(',')]
        path      = config.get('DEFAULT','collection_path')

        # create a timestamp for this run
        timestamp       = str(time.time())

        return exchanges, basecoins, altcoins, path, timestamp


def checkCollectionPath():
        # check collection path, exit if there is a problem
        try:
            os.makedirs(path)
        except OSError:
            if not os.path.isdir(path):
                raise


def getTargetPairs(exchanges = [], basecoins = [], altcoins = []):
        # Build a dataframe containing valid combinations of exchange, basecoin, and altcoin we're interested in.
        # The data here comes from cryptowat.ch and is based on how their API is structured.
        url = 'https://api.cryptowat.ch/markets'        # this is the markets list on cryptowat.ch
        r = requests.get(url).json()
        pairs = pd.DataFrame()
        for exchange in exchanges:
                for basecoin in basecoins:
                        for altcoin in altcoins:
                                targetroute = 'https://api.cryptowat.ch/markets/'+exchange+'/'+altcoin+basecoin
                                # see if this route exists in the list
                                for i in r['result']:
                                        if i['route'] == targetroute:
                                                s = pd.Series({'EXCHANGE': exchange,
                                                        'BASECOIN': basecoin,
                                                        'ALTCOIN': altcoin,
                                                        'COINPAIR': altcoin+basecoin,
                                                        'URL': targetroute})
                                                pairs = pairs.append(s,ignore_index=True)
                                                break
        return pairs

        # to do
        #       - for invalid coinpair we should log an informational message
        
        def getCoinpairPrice(pairs, coinpair):

        # check to see if any valid targets exist for the coinpair, print an error message if not
        if pairs['COINPAIR'].str.contains(coinpair).any():
                # get the URL targets for a given coinpair
                targets = pairs.where(pairs['COINPAIR']  == coinpair).dropna()

                # open the data file that stores data for the coinpair (append)
                filename = path + '/' + coinpair + ".csv"
                outfile = open(filename,"a")

                for index, row in targets.iterrows():
                        r = requests.get(row['URL']+"/summary").json()  # append /summary to the target URL 
                        try:
                                #print timestamp + "," + row['COINPAIR'] + "," + row['EXCHANGE'] + "," +  \
                                #       str(r['result']['price']['last']) +  "," + str(r['result']['volume']) 

                                outfile.write(timestamp + "," + row['COINPAIR'] + "," + row['EXCHANGE'] + "," + \
                                        str(r['result']['price']['last']) +  "," + str(r['result']['volume']) + "\n") 
                        except:
                                print "some error with " + row['EXCHANGE'] + " at " + timestamp + "\n"

                outfile.close()
                return 0
        else:
                print coinpair + " not found in the list"
                return 1

################################################################
# MAIN PROGRAM
################################################################

# read config and verify output path
exchanges, basecoins, altcoins, path, timestamp = readConfig()
checkCollectionPath()

# Identify valid targets for the coin combinations we are interested in. The coinpairs may or may not have valid targets
# for the list of exchanges we have provided so we check all combinations and return a dataframe called pairs
# that contains valid targets for markets covered by cryptowat.ch
pairs = getTargetPairs(exchanges, basecoins, altcoins)

# Get pricing per coin pair
for coinpair in pairs['COINPAIR'].unique():
        getCoinpairPrice(pairs, coinpair)
        
        
