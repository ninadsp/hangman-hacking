hangman-hacking
===============

Hacking the good old [Hangman](http://en.wikipedia.org/wiki/Hangman_(game\)) game, solving the eternal question of which alphabet to start with.

### Requirements:

* setup.bash requires bash
* curl and gunzip to download data files from [IMDb](http://www.imdb.com/interfaces)
* Python and PyMongo
* MongoDB

### How to use:
* curl -s http://raw.github.com/ninadsp/hangman-hacking/master/setup.bash | bash -s --
* Copy dbconfig_sample.py to dbconfig.py with the appropriate values
* Execute import_dump.py - expected run time of 5-10 minutes and RAM usage of ~500 MB

### TODO:
1 Clean the data being imported
1 Write a script to read through each document, and create a count of each character in the title, update it in the document
1 Dumb map/reduce (or script) over each document and find the count for each character throughout
1 Add some fancy functionality to the import_dump.py script with getopt
1 Make the map/reduce intelligent by adding ratings/language into the picture

## Warning:
This project is still a work in progress. As of now, all it does is read the list of movies, it's language and rating and insert it into a mongo collection. Has not been tested fully as my disk runs out of space :s
