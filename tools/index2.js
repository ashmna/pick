var fs = require('fs'),
    xml2js = require('xml2js'),
    csvjson = require('csvjson');

var data = fs.readFileSync('addressies.csv', { encoding : 'utf8'});


data = csvjson.toObject(data);

var BUILDINGS = {};

data.forEach(_ => {
    key = `${_.country}-${_.city}-${_.street}-${_.housenumber}`;
    BUILDINGS[key] = _;
});

var BUILDINGS_ARRAY = [];
var keys = Object.keys(BUILDINGS);
keys.sort();

keys.forEach(key => {
    BUILDINGS_ARRAY.push(BUILDINGS[key]);
});

console.log(BUILDINGS_ARRAY.length);


try {
    var json2csv = require('json2csv');
    var fields = ['country', 'city', 'street', 'housenumber'];

    var csv = json2csv({data: BUILDINGS_ARRAY, fields: fields});

    fs.writeFile('addressies.csv', csv, function (err) {
        if (err) throw err;
        console.log('file saved');
    });
} catch (err) {
    // Errors are thrown for bad options, or if the data is empty and no fields are provided.
    // Be sure to provide fields if it is possible that your data array will be empty.
    console.error(err);
}
console.log(BUILDINGS.length);
console.log('Done');

