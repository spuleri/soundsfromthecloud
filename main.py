#!flask/bin/python
from sounds import Sounds
import json
import os


    
#url to test resolver
# #http://api.soundcloud.com/resolve.json?url=https://soundcloud.com/jamkins/sets/theabyss&client_id=c585c5f24b092caec68984885cf2b0db
# res = urlopen("http://api.soundcloud.com/resolve.json?url=http://soundcloud.com/ximsergio&client_id="+YOUR_CLIENT_ID)
# user = json.load(res)
# res.close()
# userID = str(user["id"])
# print userID
# #url to test in browser http://api.soundcloud.com/users/31175757/favorites.json?client_id=c585c5f24b092caec68984885cf2b0db&limit=50&offset=0

def main():
    
    url = raw_input("Hello, please paste your soundcloud url below (only support favorites atm)" + os.linesep)
    path = raw_input("Paste the path on your computer to download files to" + os.linesep)

    sound = Sounds(url, path)
    sound.download()

    print "finished, but there were " + str(len(sound.errors)) + " errors. Check the log file" + os.linesep

    f = open('log.txt', 'wb')

    for error in sound.errors:
        f.write(error["title"].decode('utf-8') +" -> " + error["permalink_url"] + "\n")
        f.write(error["error"])
        f.write("\n\n")

    #write to file permalink_url and error



if __name__ == "__main__":
    main()