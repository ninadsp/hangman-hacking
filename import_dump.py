import dbconfig
import pymongo
from pymongo import Connection
import re
import codecs

DATA_DIR = "./imdb_data/";
MOVIES_LIST = "movies.list";
RATINGS_LIST = "ratings.list";
LANGUAGE_LIST = "language.list";

MOVIES_START = "===========";

connection = Connection(dbconfig.host, dbconfig.port);
db = connection[dbconfig.database];
collection = db[dbconfig.collection];

collection.ensure_index([("title", pymongo.ASCENDING), ("year", pymongo.ASCENDING)], unique=True);


def dump_movies():
	# movies_fp = open(DATA_DIR + MOVIES_LIST, 'r');
	movies_fp = codecs.open(DATA_DIR + MOVIES_LIST, 'r', encoding="cp1252");
	movies_lines = movies_fp.readlines();
	movies_fp.close();

	print "Read " + str(len(movies_lines)) + " line from file " + DATA_DIR + MOVIES_LIST;

	for i in range(0, len(movies_lines)):
		i+=1;
		if(MOVIES_START in movies_lines[i]):
			break;
	i +=2 ;
	movies_list = movies_lines[i:-1];

	movies_lines = [];

	print "Found " + str(len(movies_list)) + " movies";

	movies = [];

	reg_ex1 = re.compile("\(\d{4}\)");
	reg_ex2 = re.compile("(\d{4})$");

	for movie in movies_list:
		parts1 = reg_ex1.split(movie);
		title = parts1[0].strip('"').lstrip('"');
		parts2 = reg_ex2.split(movie);

		# Handle lines where IMDb does not know the year of the title
		try:
			year = parts2[1];
		except IndexError:
			year = "0";
			continue;

		insert = {"ttle" : title, "year" : year};
		movies.append(insert);
		if(len(movies) > 100):
			collection.insert(movies);
			movies[:] = [];
	
	collection.insert(movies);

	print "Inserted " + str(collection.count()) + " unique entries into the movies table";


def clean_movies():
	collection.remove();

def dump_language():
	pass;

def dump_ratings():
	pass;

dump_movies();
# clean_movies();
