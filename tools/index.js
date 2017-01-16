var fs = require('fs'),
    xml2js = require('xml2js');

var parser = new xml2js.Parser();
var BUILDINGS = [];
var k = 0;
function getBuildings(index) {
    fs.readFile(`${__dirname}/map/map_${index}.osm`, function (err, data) {
        parser.parseString(data, function (err, result) {
            const buildings = result.osm.way
                .filter(_ => _.tag && _.tag.reduce((r, tag) => {
                    if (tag['$'].k == "building") return true;
                }, 0))
                .map(_ => _.tag.reduce((r, tag) => {
                    const k = tag['$'].k.split(':')
                    if (k[0] == "addr") {
                        r[k[1]] = tag['$'].v;
                    }
                    return r;
                }, {}))
                .filter(_ => Object.keys(_).length !== 0)
                .filter(_ => _.street)
                .filter(_ => _.housenumber)

            BUILDINGS = BUILDINGS.concat(buildings);
            k++;
            console.log(`${k}/288`);
            if (k == 288) {
                main();
            }
        });
    });
}

for (let i = 0; i < 288; i++) {
    getBuildings(i);
}

function main() {
    var json2csv = require('json2csv');
    var fields = ['country', 'city', 'street', 'housenumber'];

    try {
        var csv = json2csv({data: BUILDINGS, fields: fields});

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


}
