#!/usr/bin/env python3
'''
Python Script to download audio of all videos matching keyword and to convert to wav
'''
import os
#Enter a keyword(e.g. gun,gunshots,etc.)
k=input("Keyword: ")
#Download first 100(20*5) audios with the keyword
for i in range(5):
	os.system("youtube-dl -f 140 https://www.youtube.com/results?search_query="+k+"&page="+str(i))

#Sample Sound video
#os.system("youtube-dl -f 140 https://www.youtube.com/watch?v=lZJoKI3A6uI -o ./noise/'%(title)s-%(id)s.%(ext)s'")


#takes care of special char in file name
def removeSpecialChar( filename ):
	return filename.translate ({ord(c): "\\"+c for c in "!@#$%^&*()[]{};:,/<>?\|`~-=+ "})
       

#Convert all m4a to wav
for file in os.listdir("."):
	if file.endswith(".m4a"):		
		os.system("avconv -i ../noise/"+removeSpecialChar(file)+" -ac 1 ../noise/"+removeSpecialChar(file).replace(".m4a",".wav"))


