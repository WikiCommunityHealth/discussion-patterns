#! /bin/bash

DB_FOLDER="dataset"
IT_FOLDER="wikiconv-it"
URL_DB="mongodb://localhost:27017/discussions"
DB_COLLECTION="wiki-conv"

mkdir -p $DB_FOLDER && cd $DB_FOLDER && mkdir -p $IT_FOLDER && cd $IT_FOLDER

echo "Downloading files"
curl https://s3-eu-west-1.amazonaws.com/pfigshare-u-files/22889003/20200401itjsonlines00000of00005.gz --output wikiconv-it-0.gz
curl https://s3-eu-west-1.amazonaws.com/pfigshare-u-files/22889771/20200401itjsonlines00001of00005.gz --output wikiconv-it-1.gz
curl https://s3-eu-west-1.amazonaws.com/pfigshare-u-files/22888340/20200401itjsonlines00002of00005.gz --output wikiconv-it-2.gz
curl https://s3-eu-west-1.amazonaws.com/pfigshare-u-files/22889936/20200401itjsonlines00003of00005.gz --output wikiconv-it-3.gz
curl https://s3-eu-west-1.amazonaws.com/pfigshare-u-files/22887563/20200401itjsonlines00004of00005.gz --output wikiconv-it-4.gz

echo "Decompressing files"
gzip -d wikiconv-it-0.gz
gzip -d wikiconv-it-1.gz
gzip -d wikiconv-it-2.gz
gzip -d wikiconv-it-3.gz
gzip -d wikiconv-it-4.gz

echo "Importing in mongodb"
mongoimport --uri $URL_DB -c=$DB_COLLECTION --type=json --file="wikiconv-it-0"
mongoimport --uri $URL_DB -c=$DB_COLLECTION --type=json --file="wikiconv-it-1"
mongoimport --uri $URL_DB -c=$DB_COLLECTION --type=json --file="wikiconv-it-2"
mongoimport --uri $URL_DB -c=$DB_COLLECTION --type=json --file="wikiconv-it-3"
mongoimport --uri $URL_DB -c=$DB_COLLECTION --type=json --file="wikiconv-it-4"

echo "Done"
