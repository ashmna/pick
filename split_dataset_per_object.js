const ALL_OBJECTS_COUNT = 403;
const fs = require("fs");
const csvjson = require('csvjson');
const json2csv = require('json2csv');
const execSync = require('child_process').execSync;
const Converter = require("csvtojson").Converter;

function saveFile(fileName, data) {
    let csv = json2csv({data: data, fields: fields});
    fs.writeFileSync(`resources/dataset_per_object/${fileName}`, csv);
    console.log(`${fileName} is done`);
}


const fields = [
    "objId", "date", "fog", "rain", "snow", "hail", "thunder", "tornado", "temp", "dewptm", "humidity", "wind", "wisibility", "pressurem", "indexesLength", "indexes"
];

function possessing(file, objectId) {
    return new Promise((resolve, reject) => {
        const converter = new Converter({});
        converter.fromFile(`resources/dataset/${file}`, function (err, result) {
            let datasetPerObjects = [];

            result.forEach(row => {
                datasetPerObjects.push(Object.assign({}, row));
                datasetPerObjects[datasetPerObjects.length - 1].indexes = "0";
                datasetPerObjects[datasetPerObjects.length - 1].objId = objectId;
                // for (let i = 1; i <= ALL_OBJECTS_COUNT; ++i) {
                //     datasetPerObjects[i].push(Object.assign({}, row));
                //     datasetPerObjects[i][datasetPerObjects[i].length - 1].indexes = "0";
                //     datasetPerObjects[i][datasetPerObjects[i].length - 1].objId = i;
                // }
                Object.keys(row.indexes).forEach(key => {
                    let [index, objId] = key.split("-");
                    if (!objId || objId === undefined || objId === "undefined") {
                        // console.log(row.indexes);
                        // console.log(row);
                        return;
                    }
                    if (objId != objectId) {
                        return;
                    }
                    let ind = datasetPerObjects[datasetPerObjects.length - 1].indexes.split(",");
                    ind.push(index);
                    ind = ind.filter(_ => _ !== "0");
                    datasetPerObjects[datasetPerObjects.length - 1].indexes = ind.join(",")
                });

                // console.log("$$$$$", ++y);
            });

            resolve(datasetPerObjects);
            // let dataset = [];
            // Object.keys(datasetPerObjects).forEach(key => {
            //     dataset = dataset.concat(datasetPerObjects[key]);
            // });
            // console.log("----------------------------", file);
            // saveFile(file, dataset);
        });
    });
}

function main() {

    if (process.argv.length < 3) {
        for (let o=1; o<=ALL_OBJECTS_COUNT; ++o) {
            console.log(`node ${process.argv[1]} ${o}`);
            execSync(`node ${process.argv[1]} ${o}`);
        }
    } else {
        let FILES = fs.readdirSync("resources/dataset");
        let dataset = [];
        let i = 0;

        function gen() {
            possessing(FILES[i], process.argv[2]).then(data => {
                dataset = dataset.concat(data);
                i++;
                if (FILES.length === i) {
                    saveFile(`dataset_${process.argv[2]}.csv`, dataset);
                } else {
                    gen()
                }
            });
        }
        gen();
    }

}

main();