hangman-hacking
===============

Hacking the good old [Hangman](http://en.wikipedia.org/wiki/Hangman_(game)) game, solving the eternal question of which alphabet to start with.

### Requirements:

* setup.bash requires bash
* curl and gunzip to download data files from [IMDb](http://www.imdb.com/interfaces)
* Python and PyMongo
* MongoDB

### How to use:
* curl -s http://raw.github.com/ninadsp/hangman-hacking/master/setup.bash | bash -s --
* Copy dbconfig_sample.py to dbconfig.py with the appropriate values
* Execute import_dump.py

## Warning:
This project is still a work in progress. As of now, all it does is read the list of movies and insert it into a mongo collection. It does not even read the ratings and language data yet.
