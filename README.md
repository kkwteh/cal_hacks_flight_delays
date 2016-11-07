# cal_hacks_flight_delays
Code for "Adding Predictive Machine Learning to your Hackathon Project"

Data obtained from http://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236

Setup
-----

To get your environment setup for training: run

Download and install Python3.5 if you don't already have it https://www.python.org/downloads/
Download and install Anaconda for Python3.5 https://www.continuum.io/downloads
$ conda create --name calhacks --file conda-requirements.txt
$ source activate calhacks


To run the api locally:

$ conda create --name calhacksapi pip
$ pip install -r requirements.txt
$ python wsgi.py    # server will be running locally on http://localhost:5000
