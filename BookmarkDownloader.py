############################################################################
# This file is used to download all web pages that are bookmarked in Chrome
# to the local folder that runs the program. It works by parsing the 
# Chrome bookmark file for URLs and then uses the wget linux command to 
# download the list of URLs. Downloading web pages is useful so that they
# still be viewed offline.
#
# HOW TO RUN FILE (README):
#	1. Place BookmarkDownloader.py in the directory you want bookmarks to
#	   be downloaded.
#	2. Run file with "pyhon BookmarkDownloader.py" from terminal
############################################################################

# Import os for checking if files exist and making system calls
import os

# Import re for using regular expressions to parse bookmark file for URLs
import re

# Import sys for exiting program when necessary
import sys

#TODO: find a way to update bookmark file
#TODO: adapt for use in windows
#TODO: adapt for use for other browsers
#TODO: streamline installation process. maybe packaging python in installer

# Get the current working directory
cwd = os.getcwd()

# Get the user's home folder path on linux 
home = os.getenv("HOME")

# File where Chrome automatically stores bookmark URLs and metadata in Linux.
# We will use regex to extract only the URLs from this file.
# Note there is no file extension for the bookmarks file.
bookmarkFile = home + "/.config/google-chrome/Default/Bookmarks"

# File for keeping track of all URLs that have been previously downloaded
# We will check to see if a URL already exists in this file before actually 
# writing the URL to our file used for wget.
masterList = cwd + "/bookmarksMaster.txt"

# The file actually used by the wget call. This file will contain only 
# the new URLs that are not already contained in the master list. This 
# is used to prevent re-downloading all previous URLs we have already 
# downloaded. (--no-clobber option for wget is supposed to prevent this
# from happening, but it doesn't seem to work correctly when the 
# --html-option is also used with wget.
newList = cwd + "/bookmarksNew.txt"

# This function is used to rename all files to a format compatible with 
# Windows. The reasoning for this is in case someone runs script from Linux,
# but they want their files to be downloaded to Dropbox to sync on Windows
def renameFilesForWindows():
    for dirpath, dirs, files in os.walk(cwd):
        for oldFilename in files:
            
            if ('?' in oldFilename or '<' in oldFilename or '>' in oldFilename
            or ':' in oldFilename or '"' in oldFilename or '\\' in oldFilename 
            or '*' in oldFilename or '|' in oldFilename):
                
                newFilename = re.sub('[<>:"\\\?|*]', '_', oldFilename)
                
                os.rename(os.path.join(dirpath, oldFilename), 
                          os.path.join(dirpath, newFilename))

# Make sure the bookmark file exists.
bookmarkFileExists = os.path.isfile(bookmarkFile)

# Open file and store contents in data variable.
if (bookmarkFileExists):
    fil = open(bookmarkFile, "r")
    data = fil.read()
    fil.close()   
else: 
    print "\n'" + bookmarkFile + "'" + " does not exist."
    print "This is what was specified as your Chrome bookmark file.\n"
    sys.exit()
    

# Store just the URLs in a URL tuple variable.
urls = re.findall(r"((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)", data)

# Store the descriptions of each URL
desc = re.findall(r'"name": "(.*?)",\n[ ]*"type": "url",', data)

# Make sure the master list bookmark file exists.
masterListExists = os.path.isfile(masterList)

# Store contents of master list of URLs in masterListURLs variable
if (masterListExists):
    mlfil = open(masterList, "r")
    masterListURLs = mlfil.read()
    mlfil.close()
else: 
    mlfil = open(masterList, "w")
    masterListURLs = ""
    mlfil.close()

# Open file for writing new URLs
wrfile = open(newList, "w")

# Open file for containing each description with its associated URL
descriptionFile = open("BookmarkDownloaderDescriptions.txt", "w")

# Variable for cycling through description array
i = 0

# For every URL, index 0 gets just url part of tuple,
# then write it to the new file if it doesn't already exist in master list.
# Also write the information to the description file.
for line in urls:
    line = line[0]
    if (masterListURLs.find(line) < 0):	# Returns < 0 if not found
        wrfile.write(line + "\n")
        with open(masterList, "a") as ml:	# Append new URL to master list
            ml.write(line + "\n")
        print line
    descriptionFile.write(desc[i] + "\n")
    descriptionFile.write(line + "\n\n")
    i = i + 1
    
wrfile.close()
descriptionFile.close()

# Use wget linux command for downloading the web pages
# -i specifies a file to get the urls from
# -P specifies an output folder (no longer used)
# -p specifies downloading the whole web page (images and all)
# --no-clobber specifies ignoring files that have already been downloaded
# --timeout=10 specifies 10 second timeout for trying to connect to page
# --tries=3 specifies max number of tries for a page before skipping
# --html-extension saves the files with an html extension
os.system("wget -i " + newList + " -p --no-clobber --html-extension --timeout=10 --tries=3")

renameFilesForWindows()