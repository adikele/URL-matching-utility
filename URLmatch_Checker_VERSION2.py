#Program checks automatically at intervals of 15 seconds if configured URLs match against sepecified Regex patterns.
#python 3.7
#@Aditya

#FORMAT OF URL DATA TO BE PROVIDED FOR VALIDATION:
#The data of configured URLs and corresponding Regex to be checked should be
#provided in a file named inputURLdata.jsonl as dictionaries in jsonlines format.
#New data can be provided by adding it/overwriting it on the existing data in the file inputURLdata.jsonl
#In the dictionaries, keys are Regex and values are lists of URL strings.

#Results of URLs that were not successfully matched with the regex are stored in results_faultyURLs.jsonl

#Program flow
#step 1: Program reads the dictionary from the saved file and uses matchwalaURL function to check if configured URLs match with given Regex
#step 2: Program saves the results of the check in jsonline form. Following data is saved: the wrong URLs, and time of performing the check
#step 3: Program loads the results in the cloud (AWS S3) at 30 second intervals. 

from pathlib import Path

import re
import json
import jsonlines
#The convenience function jsonlines.open() takes a file name and returns either a reader or writer

import datetime
import threading
import time as t

import boto3

import logging
import concurrent.futures

from concurrent.futures import ThreadPoolExecutor


def thread_storing_in_cloud():
    while True:
        s3 = boto3.client('s3')
        filename = 'results_faultyURLs.jsonl'  #Comment 1: Replace results_faultyURLs_demo.jsonl with name of file you create in #comment 5
        bucket_name = 'bucketaalto'  #Comment 2: Replace bucketaalto with name of a bucket in your S3 account
        s3.upload_file(filename, bucket_name, filename)
        t.sleep(30)
    

def matchURL_Wala(dicto):
    '''
    Function takes a dict with key, value pairs and for every pair checks if:
    --> the value, which is a list of one or more configured urls
    matches with the 
    --> respective key, a given Regex     
    '''
    dicto_results_faultyURLs = {}
    for key in dicto:
        text = dicto[key] #this is the list of URLs to be checked
        for URL_text in text:
            x = re.search(key, URL_text)
            if x:
                print ("OK! URL matches with Regex pattern!")
            else:
                print ("Not OK! URL not matching with Regex pattern!")
                # following code is for saving faultyURL in dicto_results_faultyURLs 
                if key in dicto_results_faultyURLs:  # if key exists, add faultyURL
                    dicto_results_faultyURLs[key].append(URL_text) 
                else:  # if key does not exist, first create an empty list, then add faultyURL
                    dicto_results_faultyURLs[key] = []
                    dicto_results_faultyURLs[key].append(URL_text)
    return dicto_results_faultyURLs
    

def thread_myPeriodicFunction():  
    while True:
        t.sleep(15)
        print("Program checks if configured URLs match with a given Regex ")
        print("------------------------------------------------------")
        with jsonlines.open('/Users/bajya/Documents/08demos/01URL_checker/inputURLdata.jsonl') as reader: #Comment 3: Replace given path and file name with your own.
            with open('results_faultyURLs.jsonl', 'a') as outfile:  #Comment 4: Replace given file name with file you create in #comment 5. 
                time = str((datetime.datetime.now()))
                json.dump( time, outfile)
                outfile.write('\n')
                for obj in reader:
                    results_faultyURLs = matchURL_Wala(obj)
                    json.dump(results_faultyURLs, outfile)
                    outfile.write('\n')  
                
                
if __name__ == "__main__":
    
    Path('/Users/bajya/Documents/08demos/01URL_checker/results_faultyURLs.jsonl').touch() 
    #Comment 5: Replace given path and file name with your own. File should be in .jsonl
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(thread_myPeriodicFunction)
        executor.submit(thread_storing_in_cloud)

