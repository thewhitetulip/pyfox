#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import sqlite3
import os
#import json
from datetime import datetime
import sys
import argparse

def executeQuery(cursor, query):
    ''' Takes the cursor object and the query, executes it '''
    try:
        cursor.execute(query)
    except:
        print("There is something wrong, probably with the query\n\n"+query)

def history(cursor, today=False):
    ''' Function which extracts history from the sqlite file '''

    sql="""select url, title, last_visit_date,rev_host  from moz_historyvisits natural join moz_places where url  like '%http%' and last_visit_date is not null
 order by last_visit_date desc;"""

    executeQuery(cursor,sql)

    if today:
        for row in cursor:
            last_visit = datetime.fromtimestamp(row[2]/1000000).strftime('%Y-%m-%d %H:%M:%S')
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if current_time[:10]==last_visit[:10]:
                print("%s %s"%(row[0],last_visit))
    else:
        for row in cursor:
            last_visit = datetime.fromtimestamp(row[2]/1000000).strftime('%Y-%m-%d %H:%M:%S')
            print("%s %s"%(row[0],last_visit))

def bookmarks(cursor, json=False, pattern=None):
    ''' Function to extract bookmark related information '''

    theQuery = """select url, moz_places.title, rev_host, frecency, last_visit_date from moz_places  join  moz_bookmarks on moz_bookmarks.fk=moz_places.id
where visit_count>0 """

    if pattern==None:
        theQuery+=" and moz_places.url  like 'http%'"
    else:
        theQuery+="and moz_places.url like '%"+pattern+"%'"

    theQuery+=" order by dateAdded desc;"
    executeQuery(cursor,theQuery)

    string=""
    title_bookmarks=['url', 'title', 'rev_host', 'frecency', 'last_visit_date']
    bookmarks_json=""
    bookmarks=[]

    for row in cursor:
        #print("%s; %s"%(row[0], datetime.fromtimestamp(row[4]/1000000).strftime('%Y-%m-%d %H:%M:%S')))
        print("%s"%(row[0]))
        if json==True:
            title_bookmarks=['url', 'title', 'rev_host', 'frecency', 'last_visit_date']
            string=""

            for row in cursor:
                blist = dict(zip(title_bookmarks,row))
                bookmarks.append(blist)

            for b in bookmarks:
               string+=str(b)+','

            bookmarks_json=string
    if bookmarks_json: print(bookmarks_json)

def getPath():
    '''Gets the path where the sqlite3 database file is present'''
    home_dir = os.environ['HOME']
    if sys.platform.startswith('win') == True:
        firefox_path = home_dir + '\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\'
    elif sys.platform.startswith('linux')==True:
        firefox_path = home_dir + "/.mozilla/firefox/"
    elif sys.platform.startswith('darwin')==True:
        firefox_path = home_dir+'Library/Application Support/Firefox/Profiles/'

    return firefox_path

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Extract information from firefox's internal database")
    parser.add_argument('--bkmrk', default="")
    parser.add_argument('--history', default=0)
    args = parser.parse_args()

    try:
        firefox_path = getPath()
        profiles = [i for i in os.listdir(firefox_path) if i.endswith('.default')]
        sqlite_path = firefox_path+ profiles[0]+'/places.sqlite'
        connection = sqlite3.connect(sqlite_path)
    except:
        print('Something went wrong with places.sqlite')
        exit(1)

    cursor = connection.cursor()
    if args.bkmrk is not None:
        bookmarks(cursor,pattern=args.bkmrk)
    elif args.history is not None:
        history(cursor)

    cursor.close()
