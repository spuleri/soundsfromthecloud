from urllib2 import urlopen, URLError, HTTPError
import json
import os
import re


from mutagen.mp3 import MP3, HeaderNotFoundError
from mutagen.id3 import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER,USLT, APIC, error

from dialog import Ui_Status


YOUR_CLIENT_ID = "c585c5f24b092caec68984885cf2b0db"
resolveUrl = "http://api.soundcloud.com/resolve.json?url="
usersUrl = "http://api.soundcloud.com/users/"

class Sounds:

    def __init__(self, url, path, likes=False, set=False, song = False, user = False):
        self.url = url
        self.likes = likes
        self.set = set
        self.song = song
        self.user = user
        self.errors = []
        #path to make new dir in
        self.path = path
        #split url at /'s, returns a list
        urlsplitted = self.url.split("/")

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
        elif "sets" in self.url:
            self.set = True

        #if the 2nd to last item in the split list is soundcloud.com
        #assume it is a user         
        elif (urlsplitted[-2] == "soundcloud.com"):
            self.user = True

        #else, it is a song
        else: self.song = True

    def dlfile(self, url,track, folder):        

        title = track["title"]
        description = track["description"]
        art_url = track["artwork_url"]
        #to get 500x500 art insteasd of 100x100
        if art_url is not None:
            art_url = art_url.replace("large", "t500x500")
            has_art = True
        else:
            has_art = False
        #title = re.sub(r"[\\\/:\*\?""'<>|]", "_", title)
        title = re.sub(r"(<|>|:|/|\\|\||\?|\*|\"|\.)", " ", title)
        artist = track["user"]["username"]
        
        #removing special char's from file name
        #filetitle = re.sub('[^A-Za-z0-9]+', '', title)
        file = folder+"/"+title+".mp3" 
        #convert from utf-8 to unicode, instead of default ascii
        #file.decode('utf-8')
        


        
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
                    
                    updateString = "Downloading... " + artist + " - " + title 
                    self.dialog.statusUpdate.emit(updateString)
                    #printing some titles fux up some ascii encoding
                    # print updateString
                    # Open our local file for writing
                    with open(file, "wb") as local_file:
                        local_file.write(f.read())

                        try:
                            mp3 = MP3(file, ID3=ID3)
                        except HeaderNotFoundError:
                            print "not an mp3, but thats ok cuz it has data??????"
                            return
                        try:
                            mp3.add_tags(ID3=ID3)
                        except error:
                            print("has tags")



                        #good thred: http://stackoverflow.com/questions/14369366/assign-album-artwork-with-mutagen-mac-vs-pc
                        if has_art:
                            art = urlopen(art_url)
                            mp3.tags.add( APIC( encoding=3, mime='image/jpeg', type=2, desc=u'Cover', data=art.read() ) )
                            art.close()

                        mp3['TIT2'] = TIT2(encoding=3, text=title) #title
                        mp3['TPE1'] = TPE1(encoding=3, text=artist) #artist
                        mp3['USLT'] = USLT(encoding=3, desc=u'description', text=description) #lyrics, putting SC description in here


                        mp3.save(v2_version=3, v1=2)


                except IOError, e:
                    #if get this error, means invalid file name
                    #LAST RESORT..
                    #remove everything except letters and numbers.
                    print 'got a damn io error'
                    print e
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

    def download(self, dialog):
        #if playlist, gives you info with playlist info, "track_count" and array "tracks" with all tracks
        #if likes, gives only array with 50 likes
        #if track, gives track lol

        res = urlopen(resolveUrl + self.url + "&client_id=" + YOUR_CLIENT_ID)
        resolved = json.load(res)
        res.close()

        #setting dialog box as class property
        self.dialog = dialog



        
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
                    self.dlfile(like["download_url"] + "?client_id=" + YOUR_CLIENT_ID, like, folder)
                
                elif "stream_url" not in like:
                    like["error"] = "doesn't have a stream url"
                    self.errors.append(like)
                #else, dl streaming file @ 128kbps
                else:
                    self.dlfile(like["stream_url"] + "?client_id=" + YOUR_CLIENT_ID, like, folder)
            return True

        #if playlist
        elif self.set:
            set_tracks = resolved["tracks"]

            
            #remove illegal characters
            set_title = re.sub(r"(<|>|:|/|\\|\||\?|\*|\"|\.)", "", resolved["title"])
            #make new dir
            if re.search(r"(<|>|:|/|\\|\||\?|\*|\"|\.)", resolved["user"]["username"]) == None:
                artist_title = resolved["user"]["username"]

            else: artist_title = resolved["user"]["permalink"]
            folder = self.path + "/" + artist_title + "-" + set_title
            try:
                os.mkdir(folder)
            except OSError, e:
                print e
                print "alrdy haz dir"

            for index, track in enumerate(set_tracks):
                #if downloadable, get the higher quality, artist provided dl
                if track["downloadable"]:
                    self.dlfile(track["download_url"] + "?client_id=" + YOUR_CLIENT_ID, track, folder)
                elif "stream_url" not in track:
                    track["error"] = "doesn't have a stream url"
                    self.errors.append(track)
                #else, dl streaming file @ 128kbps
                else:
                    self.dlfile(track["stream_url"] + "?client_id=" + YOUR_CLIENT_ID,track, folder) 
            return True

        #if artist acc
        elif self.user:
            print 'im an artist'

            if resolved["kind"] == "user":
                userid = resolved["id"]
                artistRes = urlopen(usersUrl + str(userid) +"/tracks" + "?client_id=" + YOUR_CLIENT_ID)
                artistData = json.load(artistRes)
                artistRes.close()

                #list of artists public uploaded tracks
                artists_tracks = artistData

                if re.search(r"(<|>|:|/|\\|\||\?|\*|\"|\.)", str(resolved["username"])) == None:
                    artist_title = resolved["username"]

                else: artist_title = resolved["permalink"]
                #make new dir
                folder = self.path + "/" + artist_title + "-" + "uploads"

                try:
                    os.mkdir(folder)
                except OSError, e:
                    print e
                    print "alrdy haz dir"

                for index, track in enumerate(artists_tracks):
                    #if downloadable, get the higher quality, artist provided dl
                    if track["downloadable"]:
                        self.dlfile(track["download_url"] + "?client_id=" + YOUR_CLIENT_ID, track, folder)
                    elif "stream_url" not in track:
                        track["error"] = "doesn't have a stream url"
                        self.errors.append(track)
                    #else, dl streaming file @ 128kbps
                    else:
                        self.dlfile(track["stream_url"] + "?client_id=" + YOUR_CLIENT_ID,track, folder)
                return True


            else: return False


        #if single track
        elif self.song:
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
                self.dlfile(track["download_url"] + "?client_id=" + YOUR_CLIENT_ID, track, folder)
            #else, dl streaming file @ 128kbps
            else:
                self.dlfile(track["stream_url"] + "?client_id=" + YOUR_CLIENT_ID, track, folder )
            return True

