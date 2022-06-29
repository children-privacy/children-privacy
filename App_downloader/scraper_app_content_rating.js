// scraper_search.js

var gplay = require('google-play-scraper');
// const { contentRating } = require('google-play-scraper/lib/mappers/details');

// var appID = process.argv[2];
// var folder = process.argv[3];
// var num = process.argv[3];
// var path = process.argv[4] + "Reviews\\"

var term = process.argv[2];
var path = "C:\\Age_Rating\\App_downloader\\Downloads\\";

const countries = ["us", "au", "uk", "fr", "de"]
var ratings = [];

// for (const country of countries) {
//   gplay.search({
//     term: term,
//     num: 1,
//     fullDetail: true,
//     country: country
//   })
//   .then((result)=>{
//     ratings.push(result[0].contentRating)
//     // console.log(ratings)
//   })
//   // console.log(ratings)
  
//   ratings.push(result[0].contentRating)
// }
// console.log(ratings)

async function test(){
  let ratings = [];
  for(const country of countries){
    const result = await gplay.search({
      term: term,
      num: 1,
      fullDetail: true,
      country: country,
      throttle: 20
    })
    if (result[0] != undefined)
      ratings.push(result[0].contentRating);
  }
  
  console.log(ratings.toString());
  // // return ratings

  // // text = term + " " + ratings;
  // text = {
  //   "package_name": term,
  //   "ratings": ratings
  // }

  // fs = require('fs');
  //   if(!fs.existsSync(path)){
  //   fs.mkdirSync(path);
  // }
  // fs.writeFile(path + term + '.json', text, function (err) {
  //   if (err) return console.log(err);
  //   console.log(term + ' is generated.');
  // });
}

try {
  test();
} catch (error) {
  
}


// gplay.search({
//     term: term,
//     num: 1,
//     fullDetail: true,
//     country: country
//   })
// .then((result)=>{
//   console.log(result[0].contentRating)
//   // console.log(result.values("contentRating"))

//   text = term + " " + result[0].contentRating + " " + country

//   fs = require('fs');
//   if(!fs.existsSync(path)){
//     fs.mkdirSync(path);
//   }
//   fs.writeFile(path + term + '.json', text, function (err) {
//     if (err) return console.log(err);
//     console.log(term + ' is generated.');
//   });
// });