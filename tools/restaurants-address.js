const fs = require("fs");
const getGeoCode = require("./address-from-gmap").getGeoCode;


let restaurants = fs.readFileSync("resources/menu/menu.am/Restaurants.txt", 'UTF-8');
const patternStr = `(\\d+)[\\s\\t](.+)[\\s\\t]+(\\w+)$`;
const pattern = new RegExp(patternStr, 'gim');
const matchs = restaurants.match(pattern);
const data = [];
const errors = [];

function done() {
  console.log('ID,street,city,lat,lng');
  data.forEach(_ => console.log(`${_[0]},${_[1]},${_[2]},${_[3]},${_[4]}`));
}
console.log('ID,street,city,lat,lng');
function syncData(matchs, i) {
  if (matchs.length <= i) {
    // done();
    console.log("========================ERRORS======================");
    console.log(JSON.stringify(errors));
    return;
  }
  const pattern = new RegExp(patternStr, 'gi');
  const res = pattern.exec(matchs[i]);

  function next(res, geocode) {
    try {
      const _ = [
        res[1],
        geocode.results[0].geometry.location.lat,
        geocode.results[0].geometry.location.lng,
        geocode.results[0].formatted_address,
      ];
      data.push(_);
      console.log(`${_[0]},${_[1]},${_[2]},${_[3]}`);
    } catch(err) {
      errors.push({str:matchs[i], geocode:geocode, error: err});
    }
    syncData(matchs, ++i);
  }

  getGeoCode(`${res[2]},${res[3]}`).then(geocode => {
    if (geocode.status === "ZERO_RESULTS") {
      getGeoCode(`${res[2]} str,${res[3]}`).then(geocode => {
        next(res, geocode);
      });
    } else {
      next(res, geocode);
    }
  });
}
syncData(matchs, 0);
