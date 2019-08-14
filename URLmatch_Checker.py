#Program checks automatically at intervals of 15 seconds if configured URLs
#match against sepecified Regex patterns.

#The data of configured URLs and corresponding Regex to be checked should be
#provided in a file named inputURLdata.jsonl as dictionaries in jsonlines format.
#New data can be provided by adding it/overwriting it on the existing data in the file inputURLdata.jsonl
#In the dictionaries, keys are Regex and values are lists of URL strings.

#Depending on where the inputURLdata.jsonl file is stored, its path in the program (#REPLACE PATH) should be changed

#Results of URLs that were not successfully matched with the regex are stored in results_faultyURLs.jsonl

#date:13.8.2019
#python 3
#@Aditya

#Program flow
#step 1: Program reads the dictionary from the saved file and uses matchwalaURL function to check if configured URLs match with given regex
#step 2: It saves the results of the check in jsonline form. Following data is saved: the wrong URLs, and time of performing the check

import re
import json
import jsonlines
#The convenience function jsonlines.open() takes a file name and returns either a reader or writer

import datetime
import threading
import time


def startTimer():
    interval = 15
    threading.Timer(interval, startTimer).start()
    myPeriodicFunction()


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
    

def myPeriodicFunction():  
    print("Program checks if configured URLs match with a given Regex ")
    print("------------------------------------------------------")
    with jsonlines.open('/Users/bajya/Documents/python programs/05tests/cgi_test_02/inputURLdata.jsonl') as reader:
                with open('results_faultyURLs.jsonl', 'a') as outfile:
                    time = str((datetime.datetime.now()))
                    json.dump( time, outfile)
                    outfile.write('\n')
                    for obj in reader:
                        results_faultyURLs = matchURL_Wala(obj)
                        json.dump(results_faultyURLs, outfile)
                        outfile.write('\n')  


startTimer()

