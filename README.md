# URL-matching-utility
Program checks automatically at intervals of 15 seconds if configured URLs match against specified Regex patterns.

Requirements:
1. Install python 3.7
2. Install jsonlines
3. The data for checking (configured URLs and corresponding Regex) should be provided in a file named inputURLdata.jsonl as dictionaries in jsonlines format. In the dictionaries, keys are Regex and values are lists of URL strings.

Example of the data format is given below:
{"https://networkx.github.io/documentation/(.+)": ["https://marktwain.github.io/documentation/stable/reference/classes/index.html", "https://networkx.github.io/documentation/unstable.html"]}
{"https://networkxy.github.io/documentation/(.+)": ["https://tomsawyer.github.io/documentation/stable/reference/classes/index.html", "https://networkxyz.github.io/documentation/unstable.html"]}

Meaning of the above data:
In the data file provided, there are 4 website names to be tested: two of them against a particular website name format and the other two against another format.
1. https://marktwain.github.io/documentation/stable/reference/classes/index.html  test against 
https://networkx.github.io/documentation/(.+)
2.  https://networkx.github.io/documentation/unstable.html   test against 
https://networkx.github.io/documentation/(.+)
3. https://tomsawyer.github.io/documentation/stable/reference/classes/index.html test against https://networkxy.github.io/documentation/(.+)
4. https://networkxyz.github.io/documentation/unstable.html test against https://networkxy.github.io/documentation/(.+)

New data can be provided by adding it/overwriting it on the existing data in the file inputURLdata.jsonl

Results of URLs that were not successfully matched with the regex are stored in results_faultyURLs.jsonl

Program flow:
Step 1: Program reads the dictionary from the saved file and uses matchwalaURL function to check if configured URLs match with given Regex

Step 2: Program saves the results of the check in jsonline form. 
The following data is saved: 
(i) the wrong URLs, and 
(ii) time of performing the check

Scope:
The program skeleton can be used for similar tasks, for example, for checking if names from a database match a certain name string.

