# IP GeoHawk

* A package that translates ip addresses using the ipgeolocation api. 

## Dragons Beware

* This was built and tested on Ubuntu 20. 
* Make sure you have C++11, C11, >= Python 3.9, and the packages listed below.
* sudo apt-get install -y python3-pyfiglet
* sudo apt-get install -y toilet

## Main Program

* `python3 ipAwareness.py`: Runs the program at the command line.

## Key Files

* `ip_addresses.txt`: Can be populated to do a bulk IP lookup.
* `key.txt`: Necessary to leverage the API. Populate with you key.

## Command Line Options

* Take IP addresses from a file: -f --f --file. 
* The default delimiter is a comma: ,
* Change the default delimiter: -d --d.
* An example is ./geohawk -f ip_addresses.txt -d \t. 
* Check your current client connection with -n or n or netstat.
