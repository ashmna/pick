const http = require("http");
const cache = {};

function wait(ms) {
   var start = new Date().getTime();
   var end = start;
   while(end < start + ms) {
     end = new Date().getTime();
  }
}
var exec = require('child_process').exec;

function getGeoCode1(address) {
  return new Promise((resolve, reject) => {
    if (cache[address]) {
      resolve(cache[address]);
      return;
    }
    const url = `https://maps.google.com/maps/api/geocode/json?address=${address},Armenia&key=AIzaSyDbq14dexsSRDS-IForZzAKtD3_RnhkOrw`
    exec(`curl -X GET "${url}"`, function(error, body, stderr){

          const data = JSON.parse(body);
          if (data.status === "OVER_QUERY_LIMIT") {
            wait(1000);
            getGeoCode(address).then(resolve);
          } else {
            cache[address] = data;
            resolve(data);
          }


    });
  });
}
function getGeoCode(address) {
  return new Promise((resolve, reject) => {
    if (cache[address]) {
      resolve(cache[address]);
      return;
    }
    const url = `http://maps.google.com/maps/api/geocode/json?address=${address},Armenia` //&key=AIzaSyDbq14dexsSRDS-IForZzAKtD3_RnhkOrw


    http.get(url, function(res){
      let body = '';

      res.on('data', function(chunk){
          body += chunk;
      });

      res.on('end', function(){
          const data = JSON.parse(body);
          if (data.status === "OVER_QUERY_LIMIT") {
            wait(1000);
            getGeoCode(address).then(resolve);
          } else {
            cache[address] = data;
            resolve(data);
          }
      });
    }).on('error', function(e){
      reject(e);
    });
  });
}

exports.getGeoCode = getGeoCode;
