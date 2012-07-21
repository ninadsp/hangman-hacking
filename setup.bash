#!/bin/bash
#
# Hangman Hacking setup script
#
# Clones git repo, checks for, downloads and extracts data files from IMDb
#
# Author: Ninad Pundalik
#

GITHUB_REPO="https://github.com/ninadsp/hangman-hacking.git";
HANGMAN_DIR="hangman-hacking";
IMDB_LOCAL_DIR="imdb_data";
IMDB_FTP_ROOT="ftp://ftp.fu-berlin.de/pub/misc/movies/database/";
IMDB_MOVIES_LIST="movies.list.gz";
IMDB_RATINGS_LIST="ratings.list.gz";
IMDB_LANGUAGE_LIST="language.list.gz";
DEBUG=true;
CURL_OPTIONS="--silent";
GUNZIP_OPTIONS="";

clone_github(){
	check_command git;

	debug "Found git. Cloning repo";

	git clone $GITHUB_REPO;
}

get_imdb_files(){
	check_command curl;
	check_command gunzip;

	debug "curl and gunzip found. Downloading data files from IMDb";

	echo "Checking for $IMDB_LOCAL_DIR";
	if [ ! -d $IMDB_LOCAL_DIR ] ; then
		mkdir $IMDB_LOCAL_DIR;
	fi;
	cd $IMDB_LOCAL_DIR;

	if [ ! -f $IMDB_MOVIES_LIST ] ; then
		echo "Downloading the Movies list";
		URL="$IMDB_FTP_ROOT$IMDB_MOVIES_LIST";
		download_file $URL $IMDB_MOVIES_LIST;
		gunzip_file $IMDB_MOVIES_LIST;
	fi;

	if [ ! -f $IMDB_MOVIES_LIST ] ; then
		echo "Downloading the Ratings list";
		URL="$IMDB_FTP_ROOT$IMDB_RATINGS_LIST";
		download_file $URL $IMDB_RATINGS_LIST;
		gunzip_file $IMDB_RATINGS_LIST;
	fi;

	if [ ! -f $IMDB_MOVIES_LIST ] ; then
		echo "Downloading the Language list";
		URL="$IMDB_FTP_ROOT$IMDB_LANGUAGE_LIST";
		download_file $URL $IMDB_LANGUAGE_LIST;
		gunzip_file $IMDB_LANGUAGE_LIST;
	fi;
}

download_file(){
	debug "Downloading $1 to $2 with curl";
	curl $1 -o $2 $CURL_OPTIONS;
}

gunzip_file(){
	debug "Extracting $1";
	gunzip $GUNZIP_OPTIONS $1;
}

check_command(){
	type $1 >/dev/null 2>&1 || { echo "Cannot find $1! Quitting"; exit 1; }
}

debug(){
	if [ $DEBUG ] ; then
		echo $1;
	fi;
}

if [ "$1" = "clone" ] ; then
	clone_github;
elif [ "$1" = "download" ] ; then
	get_imdb_files;
else
	clone_github;
	cd $HANGMAN_DIR;
	get_imdb_files;
fi;
