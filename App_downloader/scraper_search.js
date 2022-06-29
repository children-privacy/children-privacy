// scraper_search.js

var gplay = require('google-play-scraper');

// var appID = process.argv[2];
// var folder = process.argv[3];
// var num = process.argv[3];
// var path = process.argv[4] + "Reviews\\"

var term = process.argv[2];
var path = "C:\\Age_Rating\\App_downloader\\Downloads\\";

gplay.search({
    term: term,
    num: 1,
    fullDetail: true
  })
.then((result)=>{
  // fs = require('fs');
  // if(!fs.existsSync(path)){
  //   fs.mkdirSync(path);
  // }
  // fs.writeFile(path + term + '.json', JSON.stringify(result), function (err) {
  //   if (err) return console.log(err);
  //   console.log(term + ' is generated.');
  // });
  console.log(result);
});