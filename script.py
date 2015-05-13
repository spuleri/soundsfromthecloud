#!flask/bin/python
from flask import Flask, jsonify, request, Response
from urllib2 import urlopen, URLError, HTTPError
import json
import os

#HN dl soundcloud https://news.ycombinator.com/item?id=3668301
#just dl the media stream link....
#Soundcloud API returns less items than the given limit (although there are more):
#http://stackoverflow.com/questions/24063192/soundcloud-api-returns-less-items-than-the-given-limit-although-there-are-more

YOUR_CLIENT_ID = "c585c5f24b092caec68984885cf2b0db"

# Setup Flask app.
app = Flask(__name__, static_folder='public', static_url_path='')

@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/downloads', methods=['GET','POST'])
def get_downloads():

    print 'shit'

    # if not request.json or not 'title' in request.json:
    #     print 'in here'
    #     abort(400)

    if request.method == 'POST':
        print 'impossible'
        dlinfo = {
            'url': request.json['url'],
            'limit': request.json['limit']
        }
        res = urlopen("http://api.soundcloud.com/resolve.json?url=http://soundcloud.com/ximsergio&client_id="+YOUR_CLIENT_ID)
        user = json.load(res)
        res.close()
        userID = str(user["id"])
        print userID
        #url to test in browser http://api.soundcloud.com/users/31175757/favorites.json?client_id=c585c5f24b092caec68984885cf2b0db&limit=50&offset=0

        likes = []
        offset = 0
        offset_offset = 50
        is_done = False
        print is_done
        while not is_done:
            print 'in loop'
            res = urlopen("http://api.soundcloud.com/users/" + userID + "/favorites.json?client_id="+YOUR_CLIENT_ID+"&limit=50&offset="+str(offset))
            arr = json.load(res)
            if arr == []:
                print 'has empty arr'
                offset_offset /= 2
                if offset_offset == 0:
                    is_done = True
                    offset -= offset_offset
            else:
                likes.extend(arr)
                res.close()
                print len(likes)
                offset += offset_offset


        #downloading likes
        #make new dir called "likes" in currentdir

        # try:
        #     os.mkdir("likes")
        # except OSError:
        #     print "alrdy haz dir"

        # #must find way to do this async-ly, HELLA slow. grequests?
        # for l in likes:
        #     #if downloadable, get the higher quality, artist provided dl
        #     if l["downloadable"]:
        #         filename = l["user"]["username"] + " - " + l["title"] 
        #         dlfile(l["download_url"] + "?client_id=" + YOUR_CLIENT_ID, filename)
        #     #else, dl streaming file @ 128kbps
        #     else:
        #         filename = l["user"]["username"] + " - " + l["title"] 
        #         dlfile(l["stream_url"] + "?client_id=" + YOUR_CLIENT_ID, filename)
        
    print 'fuk'
    # dlinfo = {'message': 'hai'}
    print dlinfo
    return Response(json.dumps(likes), mimetype='application/json', headers={'Cache-Control': 'no-cache'})


def dlfile(url, name):
    # Open the url
    try:
        f = urlopen(url)
        print "downloading " + url

        # Open our local file for writing
        #TO DO: need to escape /'s in filename, cuz will think is directory lol!
        with open("likes/"+name+".mp3", "wb") as local_file:
            local_file.write(f.read())

    #handle errors
    except HTTPError, e:
        print "HTTP Error:", e.code, url
    except URLError, e:
        print "URL Error:", e.reason, url


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT",3000)))

