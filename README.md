# Datamaker #

How to get data and make it useful

## Dependencies ##
### Virtualenv ###
This project should be run in a virtualenv since it is in active development and stuff, see [Here](http://virtualenvwrapper.readthedocs.org/en/latest/) for how to set that up.
### PIP Packages ###
Some of our pip dependencies are awful and won't install unless you install its dependencies first, so install things in the following order

1. First install these apt packages for SciPY, and HDF5 support
```
#!bash
$ sudo apt-get install -y h5utils libhdf5-dev libblas-dev liblapack-dev gfortran

```
Next, install some pyhton packages
```
#!bash
$ pip install numpy==1.8.2 Cython==0.20.2 numexpr==2.4
```
tables and scipy need that stuff, and they don't like being installed at the same time, so now we can do this

```
$ pip install -r requirements.txt
```
Now we can build and run the application


## Building Datamaker ##
    $ ./setup.py install
## Running datamaker ##
###Importing data ###
    $ dm-import path_to_tick_data.csv.gz

## To run tests ##
    $ ./setup.py test

## Getting data for datamaker ##
1. Download the raw bi5 files via the download button in tickstory lite
2. Click the "Export to File" button
3. choose "Custom" in the Output Format
4. Under Header type:
Timestamp,Bid price,Ask price,Bid volume,Ask volume
5. Under Data Format:
{Timestamp:yyyy-MM-ddTHH:mm:sszz},{BidPrice},{AskPrice},{BidVolume},{AskVolume}
6. Select other parameters to your liking

## Miscellaneous Notes: ##
1. The stop_mode argument in the experiment expects "ts" for trailing stop
2. If the user is using trailing stop they should use the should_buy_ts for result

How to Install TA-Lib: https://github.com/mrjbq7/ta-lib