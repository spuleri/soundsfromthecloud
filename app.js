var request = require('request');
var http = require('http');
var fs = require('fs');

// var myUserID;
// request('http://api.soundcloud.com/resolve.json?url=http://soundcloud.com/ximsergio&client_id=c585c5f24b092caec68984885cf2b0db',
// 	function (error, response, body) {
//    if (!error && response.statusCode == 200) {
//        myUserID = body.id;
//        console.log('ur userid is: ' + myUserID);
//        console.log(body);
//    }
// })


// request('http://api.soundcloud.com/users/myUserID/favorites', function(error,response, body){

//    if (!error && response.statusCode == 200) {
//        console.log(body) 
       
//    }

// })






var url = "http://api.soundcloud.com/tracks/13158665.json?client_id=c585c5f24b092caec68984885cf2b0db";

var download = function(url, dest, cb) {
  var file = fs.createWriteStream(dest);
  var request = http.get(url, function(response) {
    response.pipe(file);
    file.on('finish', function() {
      file.close(cb);
    });
  });
}