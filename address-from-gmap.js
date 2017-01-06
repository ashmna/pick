const http = require("http");
const cache = {};

function wait(ms) {
   var start = new Date().getTime();
   var end = start;
   while(end < start + ms) {
     end = new Date().getTime();
  }
}

function getGeoCode(address) {
  return new Promise((resolve, reject) => {
    if (cache[address]) {
      resolve(cache[address]);
      return;
    }
    const url = `http://maps.google.com/maps/api/geocode/json?address=${address},Armenia`;

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
