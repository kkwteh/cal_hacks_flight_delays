# cal_hacks_flight_delays
Code for "Adding Predictive Machine Learning to your Hackathon Project"

Data downloaded from [Transtats](http://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236)

[Kevin's presentation slides](https://docs.google.com/presentation/d/1z7PFrSZ2pN7LlKYXPEZYXoMJ_w5Uz04aJVkksf9iOek/edit#slide=id.g18f8c18eff_0_63)


Setup
-----

To get your environment setup for training:

* Download and install [Python3.5](https://www.python.org/downloads/) if you don't already have it.
* Download and install [Anaconda](https://www.continuum.io/downloads) for Python3.5

```
$ conda create --name calhacks --file conda-requirements.txt
$ source activate calhacks
```


To run the api locally:
```
$ conda create --name calhacksapi pip
$ pip install -r requirements.txt
$ python wsgi.py    # server will be running locally on http://localhost:5000
```

To deploy the app on Heroku see https://www.heroku.com/
