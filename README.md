# R1D2
A robot that extracts the CERN R1 menu for you.


## API
`GET`-only API using [Flask](http://flask.pocoo.org). Available commands are

```
/       - Get today's menu
/today  - "
/week   - Get menu for the whole week
/monday - Get menu for Monday
/…      - …
/friday - Get menu for Friday
```

example version running on [r1d2.herokuapp.com](https://r1d2.herokuapp.com).
Test it via `curl https://r1d2.herokuapp.com/week`.

The server uses `shelve` to store the menu on the server and thus reduce the
number of times the data needs to be extracted from the Novae website.


## CLI
In principle, you can build your own apps using the API in whatever language
you like. An example command line app in Python is implemented in `cli.py`.
