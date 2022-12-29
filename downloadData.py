import os
import numpy as np
from copy import copy, deepcopy

from PIL import Image
import matplotlib.pyplot as plt
from scipy import spatial

import pygrib
import eumdac
import datetime
import shutil
import zipfile
import xml.etree.ElementTree as ET
from dateutil.parser import isoparse



'''#################################################################################
# SPECIFY ARGUMENTS
#################################################################################'''

# EUMETSAT website API credentials for data download
consumer_key = '<YOUR CONSUMER KEY HERE>'
consumer_secret = '<YOUR CONSUMER SECRET HERE>'

# Collection/product to download
collection_name = '<YOUR COLLECTION NAME HERE>'

# Specify start and end timestamps during which data is required (yyyy, mm, dd, hh, mn)
start = datetime.datetime(2015, 1, 1, 0, 0)
end = datetime.datetime(2020, 1, 1, 0, 0)

# Specify data directory where downloaded datafiles are required to be stored
DATA_DIR = "./data/"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Specify if product retrieval is needed to be done in parallel
pFLAG = True
if pFLAG:
    from joblib import Parallel, delayed
    nProcesses = int(os.cpu_count()/2) - 1 # Can change the number of processes if required

# Specify number of days for which data will be gathered with 1 access token
# (too small number == more time but more reliability)
# (too big number == less time but also low reliability)
numDaysPerAT = 1



'''#################################################################################
# UTILITY FUNCTION(S)/SUB-ROUTINE(S)
#################################################################################'''

# Utility function to download the EUMETSAT product
def downloadNsave (product, tempDirExt):
    # Create a temporary directory to download and extract zipped files
    tempDir = DATA_DIR + tempDirExt + "/"
    if not os.path.exists(tempDir):
        os.makedirs(tempDir)
    
    # For each product, download and extract the files - remove zipped file after unzipping
    try:
        with product.open() as fsrc, open(tempDir+'temp.zip', mode='wb') as fdst:
            shutil.copyfileobj(fsrc, fdst)
            fdst.close()
            with zipfile.ZipFile(tempDir+'temp.zip', 'r') as zip_ref:
                zip_ref.extractall(tempDir)
    except Exception as e:
        return
    
    # Parse the EOPMetadata.xml to find the timestamp of the product
    if os.path.exists(DirToUse+'EOPMetadata.xml'):
        tree = ET.parse(DirToUse+'EOPMetadata.xml')
    else:
        raise AssertionError('Error - EOPMetadata.xml file not found!')
    
    # Get the root of the XML tree
    root = tree.getroot()
    # For all children of the root, if the child is about "resultTime", find time
    timeStamps = list()
    for child in root:
        if "resultTime" in child.tag:
            for timeData in root.findall(child.tag):
                timeStamps.append(timeData[0][0].text)
            break

    if (not len(timeStamps) == 1):
        raise AssertionError("Error - Multiple timestamps encountered with tag 'resultTime'")
    
    timeStamp = isoparse(timeStamps[0])
    
    os.rename(tempDir+'temp.zip', DATA_DIR+timeStamp.strftime('%Y%m%dT%H%M%S')+'.zip')
    
    for f in os.listdir(tempDir):
        if os.path.exists(tempDir+f):
            os.remove(tempDir+f)
    try:
        os.rmdir(tempDir)
    except OSError as error:
        print(error)
        print("Directory '% s' can not be removed" % tempDir)



'''#################################################################################
# MAIN SCRIPT STARTS HERE
#################################################################################'''

# Make sure to use 1 token for not more than numDaysPerAT day(s) of data
while start-end<datetime.timedelta(seconds=0):
    if end-start > datetime.timedelta(days=numDaysPerAT):
        temp_end = start + datetime.timedelta(days=numDaysPerAT)
    else:
        temp_end = end
    print("\nWorking between", start, "and", temp_end, "timestamps...\n")
    credentials = (consumer_key, consumer_secret)
    print("Creating New Access Token")
    token = eumdac.AccessToken(credentials)
    
    # Open datastore
    print('Trying to open EUMETSAT datastore...')
    datastore = eumdac.DataStore(token)
    print('Datastore Opened!')
    
    # Select dataset collection
    print('Trying to access the specified collection...')
    selected_collection = datastore.get_collection(collection_name)
    print('Collection Found!')
    
    # Retrieve datasets that match our filter
    print('Trying to retrieve datasets that fall in the specified time range...')
    products = selected_collection.search(
        dtstart=start,
        dtend=temp_end)
    print(len(products), 'datasets retrieved!')
    start = copy(temp_end)
    
    
    # Start downloading the retrieved products
    if pFLAG:
        Parallel(n_jobs=nProcesses, verbose=10)(delayed(EUMETSATproductToImage)(product, str(pid)) for pid,product in enumerate(products))
    else:
        for product in products:
            EUMETSATproductToImage(product)
