# pyfox
A small python script for easy access to firefox bookmarks and browsing history

Usage
=======

`python3 ffs_main.py --bm go` to search bookmarks

`python ffs_main.py --hist localhost` to search history

If you want to search all the bookmarks which have the word go somewhere

This script started as a way of getting pythonic access to firefox history, the main intention was to analyze what I do in the internet, since I don't use Google Chrome & Firefox is my primary browser, I needed to find a way to objectively analyze if I wasted my time or I did something fruitful. I found some plugins which work on Google Chrome, but I didn't like them so I decided to write a python script!

My eventual plan is to create a webapp in angular and add the super powers that angular provides and create graphs, charts etc on the browsing activity on various intervals of time. Till then this will be a script that has two options, either print it on terminal or get the output on json.
