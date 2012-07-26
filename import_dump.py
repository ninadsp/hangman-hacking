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
LANGUAGE_START = "=============";
RATINGS_START= "";

connection = Connection(dbconfig.host, dbconfig.port);
db = connection[dbconfig.database];
collection = db[dbconfig.collection];

collection.ensure_index([("title", pymongo.ASCENDING), ("year", pymongo.ASCENDING)], unique=True);


def dump_movies():
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

	print "Found " + str(len(movies_list)) + " movies";

	movies = [];

	reg_ex = re.compile("^\"?(.+)\"?\s*\((\d{4})\)(?:\t*)([?0-9]{4})$");

	for movie in movies_list:
		
		match = reg_ex.search(movie);
		if(match):
			parts = match.groups();
			title = parts[0].strip('" ');
			year = parts[1];
		else:
			continue;

		insert = {"title" : title, "year" : year};
		movies.append(insert);
		if(len(movies) > 100):
			collection.insert(movies);
			movies[:] = [];
	
	collection.insert(movies);

	print "Inserted " + str(collection.count()) + " unique entries into the movies table";

	# Clean up before we leave
	movies[:] = [];
	movies_lines[:] = [];
	movies_list[:] = [];


def clean_movies():
	collection.remove();

def dump_language():
	language_fp = codecs.open(DATA_DIR + LANGUAGE_LIST, 'r', encoding='cp1252');
	language_lines = language_fp.readlines();
	language_fp.close();

	print "Read " + str(len(language_lines)) + " lines from file " + DATA_DIR + LANGUAGE_LIST;

	for i in range(0, len(language_lines)):
		i += 1;
		if(LANGUAGE_START in language_lines[i]):
			break;
	i +=1;
	language_list = language_lines[i:-1];

	print "Found " + str(len(language_list)) + " language lines";
	update_count = 0;

	reg_ex = re.compile("^\"?(.+)\"?\s*\((\d{4})\)(?:\t*)([-a-zA-Z ]+)\s*(?:\(.*\))?$");

	for lang in language_list:
		match_obj = reg_ex.search(lang);
		if(match_obj):
			parts = match_obj.groups();
			title = parts[0].strip('" ');
			year = parts[1];
			language = parts[2];

		else:
			continue;

		collection.update( {"title" : title, "year" : year}, { "$set" : {"language" : language} } );
		update_count += 1;

	print "Updated " + str(update_count) + " entries of movies with language data";

	language_list[:] = [];
	language_lines[:] = [];



def dump_ratings():
	pass;

dump_movies();
dump_language();
#dump_ratings();
#clean_movies();
