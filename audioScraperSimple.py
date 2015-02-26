#!/usr/bin/env python3
'''
Python Script to download audio of a video url and to convert to wav. Run ./noise/audioScraperCollection.py for large collection of audios
'''
import os


#Sample Sound video
os.system("youtube-dl -f 140 https://www.youtube.com/watch?v=lZJoKI3A6uI -o ./noise/'%(title)s-%(id)s.%(ext)s'")


#takes care of special char in file name
def removeSpecialChar( filename ):
	return filename.translate ({ord(c): "\\"+c for c in "!@#$%^&*()[]{};:,/<>?\|`~-=+ "})
       

#Convert all m4a to wav
for file in os.listdir("./noise"):
	if file.endswith(".m4a"):		
		os.system("avconv -i ./noise/"+removeSpecialChar(file)+" -ac 1 ./noise/"+removeSpecialChar(file).replace(".m4a",".wav"))


