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
    except Exception as e:
        print("There is something wrong, probably with the query\n\n"+str(e)+"\n "+ query)

def history(cursor, today=False, pattern=None,src=""):
    ''' Function which extracts history from the sqlite file '''
    if src=='firefox':
        sql="""select url, title, last_visit_date,rev_host  from moz_historyvisits natural join moz_places where last_visit_date is not null and """
        if pattern is not None:
            sql+= "url  like '%"+pattern+"%' and url not like '%google%.co%' and url not like '%duckduckgo.co%' and url not like '%live.com%'\
            and url not like '%facebook%.com%' and url not like '%gmail.com%'"
        else:
            sql+= " url  like 'http%'"
        sql+=' order by last_visit_date desc;'

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
    elif src=='chrome':
        sql = "SELECT urls.url, urls.title, urls.visit_count, \
        urls.typed_count, datetime(urls.last_visit_time/1000000-11644473600,'unixepoch','localtime'), urls.hidden,\
        visits.visit_time, visits.from_visit, visits.transition FROM urls, visits\
         WHERE  urls.id = visits.url"

        if pattern is not None:
            sql += " and title like '%"+ pattern+"%'"
        #sql+=" order by last_visit_time desc"

        executeQuery(cursor,sql)

        for row in cursor:

            print("%s %s"%(row[0],row[4]))

def bookmarks(cursor, json=False, pattern=None):
    ''' Function to extract bookmark related information '''

    theQuery = """select url, moz_places.title, rev_host, frecency, last_visit_date from moz_places  join  \
    moz_bookmarks on moz_bookmarks.fk=moz_places.id where visit_count>0 """

    if pattern==None:
        theQuery+=" and moz_places.url  like 'http%'"
    else:
        theQuery+=" and moz_places.title like '%"+pattern+"%' and moz_places.url not like '%google.co%' and moz_places.url not like '%duckduckgo.co%'"

    theQuery+=" order by dateAdded desc;"
    executeQuery(cursor,theQuery)

    string=""
    title_bookmarks=['url', 'title', 'rev_host', 'frecency', 'last_visit_date']
    bookmarks_json=""
    bookmarks=[]

    for row in cursor:
        #print("%s; %s"%(row[0], datetime.fromtimestamp(row[4]/1000000).strftime('%Y-%m-%d %H:%M:%S')))
        print("%s"%(row[0]))
        '''if json==True:
            title_bookmarks=['url', 'title', 'rev_host', 'frecency', 'last_visit_date']
            string=""

            for row in cursor:
                blist = dict(zip(title_bookmarks,row))
                bookmarks.append(blist)

            for b in bookmarks:
               string+=str(b)+','

            bookmarks_json=string

    if bookmarks_json:
        file = open('bookmarks.json','w')
        file.write(bookmarks_json)
        file.close()'''

def getPath(browser):
    '''Gets the path where the sqlite3 database file is present'''
    home_dir = os.environ['HOME']
    if browser=='firefox':
        if sys.platform.startswith('win') == True:
            path = home_dir + '\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\'
        elif sys.platform.startswith('linux')==True:
            path = home_dir + "/.mozilla/firefox/"
        elif sys.platform.startswith('darwin')==True:
            path = home_dir+'Library/Application Support/Firefox/Profiles/'
    elif browser=='chrome':
        if sys.platform.startswith('win') == True:
            path = home_dir + ''
        elif sys.platform.startswith('linux')==True:
            path = home_dir + "/.config/chromium/Default/History"
        elif sys.platform.startswith('darwin')==True:
            path = home_dir+''

    return path

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Extract information from firefox's internal database")
    parser.add_argument('--bm', '-b',default="")
    parser.add_argument('--hist','-y', default="")
    #parser.add_argument('--json',default=False) TODO: Later some time
    args = parser.parse_args()

    try:
        firefox_path = getPath('firefox')
        profiles = [i for i in os.listdir(firefox_path) if i.endswith('.default')]
        sqlite_path = firefox_path+ profiles[0]+'/places.sqlite'
        firefox_connection = sqlite3.connect(sqlite_path)
        #chrome_sqlite_path = '/home/thewhitetulip/.config/chromium/Default/History'
        chrome_sqlite_path = firefox_path = getPath('chrome')
        chrome_connection = sqlite3.connect(chrome_sqlite_path)
    except Exception as e:
        print('Something went wrong with places.sqlite ' + str(e))
        exit(1)

    cursor = firefox_connection.cursor()
    chrome_cursor = chrome_connection.cursor()

    if args.bm is not '':
        bookmarks(cursor,pattern=args.bm)
    if args.hist is not '' :
        print("From firefox")
        history(cursor, pattern=args.hist, src="firefox")
        print("From chrome")
        history(chrome_cursor, pattern=args.hist, src="chrome")

    cursor.close()
    chrome_cursor.close()
