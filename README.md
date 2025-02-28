# log-tagger
This repository is for tagging a AWS vpc logs against a lookup table
The output of the program will be a csv file with the tag counts and port protocol counts in the same directory as the input file.

## Input:
* The input file is a txt file with the flow logs from AWS VPC. in the same directory. The program expects it to be with the name "flow_logs.txt"
* The tag list is a csv file with the tag list. The program expects it to be with the name "tag_list.csv"
* The protocol numbers is a csv file with the protocol numbers. The program expects it to be with the name "protocol_numbers.csv". It can be downloaded from https://www.iana.org/assignments/protocol-numbers/protocol-numbers-1.csv

## Assumptions:
* The program only works for default format VPC flow logs version 2.
* The flow logs are in the format of txt file unlike the log.gz format.
* The program knows the name of the file and it is hardcoded in the program.
* If there exists a port protocol combination that isn't in the tag list then it will be tagged as "Unknown"
* For the port protocol counts I am considering the dstport as the port number. We can also use the srcport for the same purpose.

## How to run the code:
* Clone the repository
* Make sure you have python3 installed in your system
* Run the following command:
```
python3 log_tagger.py
```

## Alternative design:
* The same program can be moved to a lambda function and can be triggered by a cloudwatch event periodically with the log file as the input.

