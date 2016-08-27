# R1D2 [![Build Status](https://travis-ci.org/kdungs/R1D2.svg?branch=master)](https://travis-ci.org/kdungs/R1D2)
A robot that extracts the menus of the CERN restaurants (R1, R2, R3) for you.


## API
`GET`-only API using [Flask](http://flask.pocoo.org). There are three types of
commands that can be composed to query the menu.

Specify the date
```
/week
/today
/tomorrow
/monday
/…
/friday
```

Specify the restaurant
```
/r1
/r2
/r3
```

Specify the type of dish
```
/menu1
/menu2
/menu3
/vegetarian
/speciality
/grill
/pasta
/pizza
```

There is an example version running on
[r1d2.herokuapp.com](https://r1d2.herokuapp.com). Test it via `curl
https://r1d2.herokuapp.com/today/r1/vegetarian`.

Please note that due to the super simple way this API is implemented the order
of the parameters does not matter but using two mutually exclusive parameters
together will result in an empty menu.

The server uses `shelve` to store the menu on the server and thus reduce the
number of times the data needs to be extracted from the Novae website.


## Telegram bot
In addition to the simple API, this app also runs a primitive bot for the
[Telegram mesenger](https://telegram.org/). It's name is
[@r1d2_bot](https://telegram.me/r1d2_bot), click on the link to chat with it.
