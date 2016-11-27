const ALL_OBJECTS_COUNT = 403;
const fs = require("fs");
const csvjson = require('csvjson');
const json2csv = require('json2csv');
const execSync = require('child_process').execSync;
const Converter = require("csvtojson").Converter;
const converter = new Converter({});

function getDataSetContent() {

}

function mergeAllDataSets() {

}

function collectPointsForTest() {

}

function saveFile(fileName, data) {
    let csv = json2csv({data: data, fields: fields});
    fs.writeFileSync(`resources/dataset_per_object/${fileName}`, csv);
    console.log(`${fileName} is done`);
}


const fields = [
    "objId", "date", "fog", "rain", "snow", "hail", "thunder", "tornado", "temp", "dewptm", "humidity", "wind", "wisibility", "pressurem", "indexesLength", "indexes"
];

function possessing(file) {
    console.log("# Start", file);
    converter.fromFile(`resources/dataset/${file}`, function (err, result) {
        let datasetPerObjects = {};
        for (let i = 1; i <= ALL_OBJECTS_COUNT; ++i) {
            datasetPerObjects[i] = [];
        }

        let y = 0;
        result.forEach(row => {
            for (let i = 1; i <= ALL_OBJECTS_COUNT; ++i) {
                datasetPerObjects[i].push(Object.assign({}, row));
                datasetPerObjects[i][datasetPerObjects[i].length - 1].indexes = "0";
                datasetPerObjects[i][datasetPerObjects[i].length - 1].objId = i;
            }
            Object.keys(row.indexes).forEach(key => {
                let [index, objId] = key.split("-");
                if (!objId || objId === undefined || objId === "undefined") {
                    // console.log(row.indexes);
                    // console.log(row);
                    return;
                }
                let ind = datasetPerObjects[objId][datasetPerObjects[objId].length - 1].indexes.split(",");
                ind.push(index);
                ind = ind.filter(_ => _ !== "0");
                datasetPerObjects[objId][datasetPerObjects[objId].length - 1].indexes = ind.join(",")
            });

            // console.log("$$$$$", ++y);
        });

        let dataset = [];
        Object.keys(datasetPerObjects).forEach(key => {
            dataset = dataset.concat(datasetPerObjects[key]);
        });
        console.log("----------------------------", file);
        saveFile(file, dataset);
    });
}

function main() {

    if (process.argv.length < 3) {
        let FILES = fs.readdirSync("resources/dataset");
        FILES.forEach(f => {
            // if(f < "20160922.csv") {
            //     return;
            // }
            console.log(`node ${process.argv[1]} ${f}`);
            execSync(`node ${process.argv[1]} ${f}`);
        });
    } else {
        possessing(process.argv[2]);
    }

}

main();