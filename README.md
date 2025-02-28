# log-tagger
This repository is for tagging a AWS vpc logs against a lookup table
The output of the program will be a csv file with the tag counts and port protocol counts in the same directory as the input file.

## Assumptions:
* For the purpose of this assignment I am having the protocol numbers in a small dictionary. In real world scenario, this dictionary can be replaced with a csv file.
* If there exists a port protocol combination that isn't in the tag list then it will be tagged as "Unknown"
* For the port protocol counts I am considering the dstport as the port number. We can also use the srcport for the same purpose.

## How to run the code:
* Clone the repository
* Run the following command:
```
python3 log_tagger.py
```

## Alternative design:
* The same program can be moved to a lambda function and can be triggered by a cloudwatch event periodically with the log file as the input.
* This program can also be run as a cron job in an EC2 instance.
