#!usr/bin/python3.4
# -*- coding: utf-8 -*-

import sqlite3
import os
#import json
from datetime import datetime

def history(cursor, today=False):
    sql="""select url, title, last_visit_date  from moz_historyvisits natural join moz_places where url  like '%http%' and last_visit_date is not null
 order by last_visit_date desc; """
    cursor.execute(sql)
    if today:
        for row in cursor:
            last_visit = datetime.fromtimestamp(row[2]/1000000).strftime('%Y-%m-%d %H:%M:%S')
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if current_time[:10]==last_visit[:10]:
                print("%s %s"%(row[0],last_visit))
    else:
        for row in cursor:
            print("%s %s"%(row[0],last_visit))

def bookmarks(cursor, json=False):
    cursor.execute ("""select url, moz_places.title, rev_host, frecency, last_visit_date from moz_places  join  moz_bookmarks on moz_bookmarks.fk=moz_places.id
where moz_places.url  like 'http%' and visit_count>0 order by last_visit_date desc;""")

    string=""
    title_bookmarks=['url', 'title', 'rev_host', 'frecency', 'last_visit_date']
    bookmarks_json=""
    bookmarks=[]

    for row in cursor:
        print("%s; %s"%(row[0], datetime.fromtimestamp(row[4]/1000000).strftime('%Y-%m-%d %H:%M:%S')))
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


if __name__=="__main__":
    home_dir = os.environ['HOME']
    firefox_path = home_dir + "/.mozilla/firefox/"
    profiles = [i for i in os.listdir(firefox_path) if i.endswith('.default')]
    sqlite_path = firefox_path+ profiles[0]+'/places.sqlite'
    print(sqlite_path)

    connection = sqlite3.connect(sqlite_path)

    cursor = connection.cursor()
    history(cursor, today=True)
    bookmarks(cursor, json=True)
    cursor.close()

