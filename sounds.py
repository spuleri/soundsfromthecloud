from urllib2 import urlopen, URLError, HTTPError
import json
import os
import re
import eyed3
import eyed3.id3

from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import mutagen.id3

YOUR_CLIENT_ID = "c585c5f24b092caec68984885cf2b0db"
resolveUrl = "http://api.soundcloud.com/resolve.json?url="
usersUrl = "http://api.soundcloud.com/users/"

class Sounds:

    def __init__(self, url, path, likes=False, set=False, song = False):
        self.url = url
        self.likes = likes
        self.set = set
        self.song = song
        self.errors = []
        #path to make new dir in
        self.path = path

        if "likes" in self.url:
            self.likes = True
            self.user = self.url.rsplit("/", 2)[1] 
            if self.user == "you":
                print "I dunno who the user you is..."
            else:
                #setting self.userid to the user's id from the url
                res = urlopen(resolveUrl + "https://soundcloud.com/" + self.user + "&client_id=" + YOUR_CLIENT_ID)
                self.userid = json.load(res)["id"]
                res.close()
        #if its a playlist
        if "sets" in self.url: self.set = True
        #else, it is a song
        else: self.song = True

    def dlfile(self, url,track, folder, textBox):        

        title = track["title"]
        
        #title = re.sub(r"[\\\/:\*\?""'<>|]", "_", title)
        title = re.sub(r"(<|>|:|/|\\|\||\?|\*|\"|\.)", "_", title)
        artist = track["user"]["username"]
        
        #removing special char's from file name
        #filetitle = re.sub('[^A-Za-z0-9]+', '', title)
        file = folder+"/"+title+".mp3" 
        


        
        try:
            f = urlopen(url)
            
            #http://stackoverflow.com/questions/862173/how-to-download-a-file-using-python-in-a-smarter-way
            #if track provides download link that redirects and isnt mp3
            #actually it downloads them with correct extension but some arent working o_O -->maybe cuz i cancelled in the middle?
            #mnek - wrote a song about u has no stream url lol, it has streamable = false??
            if f.info().has_key('Content-Disposition'):
                # If the response has Content-Disposition, we take file name from it
                file = f.info()['Content-Disposition'].split('filename=')[1]
                if file[0] == '"' or file[0] == "'":
                    file = folder+"/"+file[1:-1]

            
            #if file already exsists, dont download it!
            if os.path.isfile(file):
                return

            #while loop just in case to catch file-name errors if they slip by.
            while True:
                try:
                    # Open our local file for writing
                    with open(file, "wb") as local_file:
                        local_file.write(f.read())
                        print "downloading " + url
                        textBox.statusTextEdit.appendPlainText("Downloading " + title + " - " + artist )

                        try:
                            mp3 = MP3(file, ID3=EasyID3)
                        except mutagen.mp3.HeaderNotFoundError:
                            print "not an mp3, but thats ok cuz it has data??????"
                            print title
                            return

                        try:
                            mp3.add_tags(ID3=EasyID3)
                        except mutagen.id3.error:
                            print("has tags")

                        mp3['title'] = title
                        mp3['author'] = artist
                        mp3['artist'] = artist
                        mp3.save()
                        # mp3 = eyed3.load(file)
                        # if mp3.tag is None:
                        #     print "tag is none"
                        #     mp3.tag = eyed3.id3.Tag()
                        #     mp3.tag.file_info = eyed3.id3.FileInfo(file)
                        # mp3.tag.artist = artist
                        # mp3.tag.title = title 
                        # mp3.tag.track_num = index + 1
                        # mp3.tag.save()

                except IOError:
                    #if get this error, means invalid file name
                    #LAST RESORT..
                    #remove everything except letters and numbers.
                    title = re.sub('[^a-zA-Z0-9\n\.]', "", title)
                    file = folder+"/"+title+".mp3"
                    continue
                break 


        #handle errors
        except HTTPError, e:
            track["error"] = "HTTP Error:" + str(e.code) + " " +  url
            self.errors.append(track)  
        except URLError, e:
            track["error"] = "URL Error:" +  str(e.reason) + " " + url
            self.errors.append(track)

    def download(self, textBox):
        #if playlist, gives you info with playlist info, "track_count" and array "tracks" with all tracks
        #if likes, gives only array with 50 likes
        #if track, gives track lol

        res = urlopen(resolveUrl + self.url + "&client_id=" + YOUR_CLIENT_ID)
        resolved = json.load(res)
        res.close()
        
        if self.likes:
            likes = []
            offset = 0
            offset_offset = 50
            is_done = False
            
            while not is_done:
                res = urlopen(usersUrl + str(self.userid) + "/favorites.json?client_id="+YOUR_CLIENT_ID+"&limit=50&offset="+str(offset))
                arr = json.load(res)
                if arr == []:
       
                    offset_offset /= 2
                    if offset_offset == 0:
                        is_done = True
                        offset -= offset_offset
                else:
                    likes.extend(arr)
                    res.close()
                    offset += offset_offset
            
            #downloading likes
            #make new dir called "likes" in currentdir
            folder = self.path + "/" + self.user + "-" + "likes"
            try:
                os.mkdir(folder)
            except OSError, e:
                print "alrdy haz dir"

            #must find way to do this async-ly, HELLA slow. grequests?
            for index, like in enumerate(likes):
            

                #if downloadable, get the higher quality, artist provided dl
                if like["downloadable"]:
                    self.dlfile(like["download_url"] + "?client_id=" + YOUR_CLIENT_ID, like, folder, textBox)
                
                elif "stream_url" not in like:
                    like["error"] = "doesn't have a stream url"
                    self.errors.append(like)
                #else, dl streaming file @ 128kbps
                else:
                    self.dlfile(like["stream_url"] + "?client_id=" + YOUR_CLIENT_ID, like, folder, textBox)
            return True

        #if playlist
        if self.set:
            set_tracks = resolved["tracks"]

            
            #make new dir 
            folder = self.path + "/" + resolved["user"]["username"] + "-" + resolved["title"]
            try:
                os.mkdir(folder)
            except OSError, e:
                print "alrdy haz dir"

            for index, track in enumerate(set_tracks):



                #if downloadable, get the higher quality, artist provided dl
                if track["downloadable"]:
                    self.dlfile(track["download_url"] + "?client_id=" + YOUR_CLIENT_ID, track, folder, textBox)
                elif "stream_url" not in track:
                    track["error"] = "doesn't have a stream url"
                    self.errors.append(track)
                #else, dl streaming file @ 128kbps
                else:
                    self.dlfile(track["stream_url"] + "?client_id=" + YOUR_CLIENT_ID,track, folder, textBox) 
            return True

        #if single track
        if self.song:
            print 'hi'

            track = resolved
            #make new dir 
            folder = self.path + "/" + "soundcloud-downloads"
            try:
                os.mkdir(folder)
            except OSError, e:
                print "alrdy haz dir"
            
            #if downloadable, get the higher quality, artist provided dl
            if track["downloadable"]:
                self.dlfile(track["download_url"] + "?client_id=" + YOUR_CLIENT_ID, track, folder, textBox)
            #else, dl streaming file @ 128kbps
            else:
                self.dlfile(track["stream_url"] + "?client_id=" + YOUR_CLIENT_ID, track, folder, textBox)
            return True

