var gplay = require('google-play-scraper');
// var path = "C:\\Age_Rating\\App_downloader\\Downloads\\App_list\\";

var category = process.argv[2];
var collection = process.argv[3];
var num = process.argv[4];
var path = process.argv[5] + "\\App_list\\";

function formatDate(date) {
  if (date !== undefined && date !== "") {
    var myDate = new Date(date);
    var month = [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
    ][myDate.getMonth()];
    var str = myDate.getDate() + month + myDate.getFullYear();
    return str;
  }
  return "";
}

var filename = 'list_' + category + '_' + collection + '_' + formatDate(new Date()) + '_' + num;

gplay.list({
  category: category,
  collection: gplay.collection[collection],
  num: num,
  fullDetail: true,
  country: 'us'
})
.then((result)=>{
  fs = require('fs');
  if(!fs.existsSync(path)){
    fs.mkdirSync(path);
  }
  fs.writeFile(path + filename + '.json', JSON.stringify(result), function (err) {
    if (err) return console.log(err);
    console.log(filename + ' is generated.');
  });
});

// for (let key in gplay.category){
//   gplay.list({
//     category: key,
//     collection: gplay.collection.TOP_FREE,
//     num: 2000
//   })
//   .then((result)=>{
//       fs = require('fs');
//       fs.writeFile('results/results_' + key + '.txt', JSON.stringify(result), function (err) {
//         if (err) return console.log(err);
//         console.log(key + 'done');
//       });
//   });
// }

// gplay.list({
//   category: gplay.category.FAMILY,
//   collection: gplay.collection.TOP_FREE,
//   num: 10,
//   fullDetail: true
// })
// gplay.list({
//     category: gplay.category.GAME_ACTION,
//     collection: gplay.collection.TOP_FREE,
//     num: 2
//   })
  // .then(console.log, console.log);
