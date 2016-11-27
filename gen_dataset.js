const fs = require('fs');
const json2csv = require('json2csv');

Date.prototype.yyyymmdd = function () {
    var mm = this.getMonth() + 1; // getMonth() is zero-based
    var dd = this.getDate();
    mm = mm < 10 ? '0' + mm : mm;
    dd = dd < 10 ? '0' + dd : dd;
    return [this.getFullYear(), mm, dd].join(''); // padding
};

function hh(HH) {
    return HH < 10 ? '0' + HH : '' + HH;
}

function mm(MM) {
    return MM < 10 ? '0' + MM : '' + MM;
}

const AVERAEG_DAY_COUNT = 300;
const WEEKS = [24, 26, 33, 30, 28, 20, 11];
const HOURS = [
    0,  // 00
    0,  // 01
    0,  // 02
    0,  // 03
    0,  // 04
    0,  // 05
    0,  // 06
    3,  // 07
    25, // 08
    27, // 09
    13, // 10
    3,  // 11
    28, // 12
    50, // 13
    48, // 14
    20, // 15
    10, // 16
    4,  // 17
    30, // 18
    32, // 19
    4,  // 20
    0,  // 21
    0,  // 22
    0,  // 23
];
const MINUTES = [
    100, // 05
    100, // 10
    95,  // 15
    92,  // 20
    90,  // 25
    85,  // 30
    90,  // 35
    96,  // 40
    99,  // 45
    100, // 50
    95,  // 55
    100, // 60
];

function getWeatherData(date, hour, min) {
    function modifyWeatherData(prev, next) {
        let weatherData = {
            fog:     parseInt(prev.fog),
            rain:    parseInt(prev.rain),
            snow:    parseInt(prev.snow),
            hail:    parseInt(prev.hail),
            thunder: parseInt(prev.thunder),
            tornado: parseInt(prev.tornado),

            temp:       parseFloat(prev.tempm),
            dewptm:     parseFloat(prev.dewptm),
            humidity:   parseFloat(prev.hum),
            wind:       parseFloat(prev.wdird),
            wisibility: parseFloat(prev.vism),
            pressurem:  parseFloat(prev.pressurem),
        };
        return weatherData;
    }

    let data = fs.readFileSync(`resources/weather/history_${date.yyyymmdd()}.json`, { encoding : 'utf8'});
    data = JSON.parse(data);
    let prev;
    let next;
    for (let item of data.history.observations) {
        if (item.date.hour <= hh(hour) && item.date.min <= mm(min)) {
            prev = item;
        } else {
            if (!prev) {
                prev = item;
            }
            next = item;
            break;
        }
    }

    return modifyWeatherData(prev, next);
}

function normalWeatherData(weatherData) {
    // console.log(weatherData);
    weatherData.temp        = (273 + weatherData.temp) / 500;
    weatherData.dewptm      = (5+ weatherData.dewptm) / 50;
    weatherData.humidity    = weatherData.humidity / 100;
    weatherData.wind        = (500 + weatherData.wind) / 1500;
    weatherData.wisibility  = weatherData.wisibility / 20;
    weatherData.pressurem   = (weatherData.pressurem - 1000) / 300;
    // console.log(weatherData);
    return weatherData;
}

function getPercentByWeatherData(weatherData) {
    let percent = 40 * weatherData.temp;
    percent += 5*weatherData.humidity;
    percent += 5*weatherData.dewptm;
    percent += 20*weatherData.wind;
    percent += 5*weatherData.wisibility;
    percent += 5*weatherData.pressurem;
    if (weatherData.fog || weatherData.rain || weatherData.snow) {
        percent += 20;
    }
    return percent;
}

function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min)) + min;
}

//
// let groups = {};
//
// groups['45'] = [];
// for (let i = 0; i< 40; ++i) {
//     let n = getRandomInt(1, 7000);
//     groups['45'].push([n, n+1]);
// }
//
// groups['20'] = [];
// for (let i = 0; i< 20; ++i) {
//     let n = getRandomInt(1, 7000);
//     groups['20'].push([n, n+1, n+2, n+3]);
// }
//
// groups['10'] = [];
// for (let i = 0; i< 10; ++i) {
//     let n = getRandomInt(1, 7000);
//     groups['10'].push([n, n+1, n+2, n+3, n+4, n+5]);
// }
//
// groups['5'] = [];
// for (let i = 0; i< 10; ++i) {
//     let n = getRandomInt(1, 7000);
//     groups['5'].push([n, n+1, n+2, n+3, n+4, n+5, n+6, n+7, n+8, n+9]);
// }
//
// console.log(JSON.stringify(groups));

const GROUPS = {
    "45": [[2690, 2691], [1967, 1968], [66, 67], [5558, 5559], [4734, 4735], [977, 978], [3181, 3182], [1259, 1260], [2661, 2662], [1806, 1807], [4692, 4693], [749, 750], [6479, 6480], [4496, 4497], [6891, 6892], [3168, 3169], [822, 823], [1094, 1095], [2845, 2846], [1205, 1206], [795, 796], [4155, 4156], [1280, 1281], [3274, 3275], [1283, 1284], [1651, 1652], [2746, 2747], [4272, 4273], [3684, 3685], [3764, 3765], [5373, 5374], [5231, 5232], [5477, 5478], [2951, 2952], [147, 148], [1339, 1340], [4620, 4621], [3519, 3520], [6098, 6099], [5079, 5080]],
    "65": [[6358, 6359, 6360, 6361], [6844, 6845, 6846, 6847], [4629, 4630, 4631, 4632], [3448, 3449, 3450, 3451], [611, 612, 613, 614], [2093, 2094, 2095, 2096], [2213, 2214, 2215, 2216], [2566, 2567, 2568, 2569], [1381, 1382, 1383, 1384], [6501, 6502, 6503, 6504], [6944, 6945, 6946, 6947], [4104, 4105, 4106, 4107], [6400, 6401, 6402, 6403], [749, 750, 751, 752], [20, 21, 22, 23], [2688, 2689, 2690, 2691], [6742, 6743, 6744, 6745], [2118, 2119, 2120, 2121], [3258, 3259, 3260, 3261], [983, 984, 985, 986]],
    "75": [[4067, 4068, 4069, 4070, 4071, 4072], [3057, 3058, 3059, 3060, 3061, 3062], [1013, 1014, 1015, 1016, 1017, 1018], [3622, 3623, 3624, 3625, 3626, 3627], [369, 370, 371, 372, 373, 374], [4304, 4305, 4306, 4307, 4308, 4309], [1986, 1987, 1988, 1989, 1990, 1991], [1949, 1950, 1951, 1952, 1953, 1954], [2949, 2950, 2951, 2952, 2953, 2954], [3237, 3238, 3239, 3240, 3241, 3242]],
    "80": [[4186, 4187, 4188, 4189, 4190, 4191, 4192, 4193, 4194, 4195], [5547, 5548, 5549, 5550, 5551, 5552, 5553, 5554, 5555, 5556], [2593, 2594, 2595, 2596, 2597, 2598, 2599, 2600, 2601, 2602], [406, 407, 408, 409, 410, 411, 412, 413, 414, 415], [2668, 2669, 2670, 2671, 2672, 2673, 2674, 2675, 2676, 2677], [1742, 1743, 1744, 1745, 1746, 1747, 1748, 1749, 1750, 1751], [277, 278, 279, 280, 281, 282, 283, 284, 285, 286], [4680, 4681, 4682, 4683, 4684, 4685, 4686, 4687, 4688, 4689], [4815, 4816, 4817, 4818, 4819, 4820, 4821, 4822, 4823, 4824], [1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936]],
};
const GROUPS_KEYS = Object.keys(GROUPS);
const OBJECTS = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,330,331,332,333,334,335,336,337,338,339,340,341,342,343,344,345,346,347,348,349,350,351,352,353,354,355,356,357,358,359,360,361,362,363,364,365,366,367,368,369,370,371,372,373,374,375,376,377,378,379,380,381,382,383,384,385,386,387,388,389,390,391,392,393,394,395,396,397,398,399,400,401,402,403];


function getIndex() {
    let n = getRandomInt(0, 100);
    let index = "100";
    for(key of GROUPS_KEYS) {
        if (n < key && index < key) index = key;
    }
    if(index == "100") return getRandomInt(1, 7000);


    let index1 = getRandomInt(0, GROUPS[index].length-1);
    let index2 = getRandomInt(0, GROUPS[index][index1].length-1);
    return GROUPS[index][index1][index2];
}

function getObject(index) {
    let n = getRandomInt(0, 100);
    if(n > 80) return OBJECTS[getRandomInt(0, OBJECTS.length -1)];
    return OBJECTS[getRandomInt(index -2, index +2)%OBJECTS.length];
}

let now = new Date(2016, 10, 10);


const fields = [
    "date", "fog", "rain", "snow", "hail", "thunder", "tornado", "temp", "dewptm", "humidity", "wind", "wisibility", "pressurem", "indexesLength", "indexes"
];

function saveFile(date, data) {
    let csv = json2csv({data: data, fields: fields});
    // console.log(csv);
    fs.writeFileSync(`resources/dataset/${date.yyyymmdd()}.csv`, csv);

    console.log(`resources/dataset/${date.yyyymmdd()}.csv file saved`);
}

function pad(number) {
    if ( number < 10 ) {
        return '0' + number;
    }
    return number;
}

for (let d = new Date(2016, 7, 1); d <= now; d.setDate(d.getDate() + 1)) {
    let date = new Date(d);
    let percent = getRandomInt(WEEKS[(date.getDay() + 1)%7] - 5, WEEKS[(date.getDay() + 1)%7] + 5);
    let count = getRandomInt(AVERAEG_DAY_COUNT * 0.95, AVERAEG_DAY_COUNT * 1.05) / 100 * percent;
    let dayCount = 0;
    let dataset = [];
    for (let h = 0; h < 24; ++h){
        let countH = count * HOURS[h] / 100;
        for(let m = 0; m < 60; m+= 5) {
            let indexes = {};
            let indexesLength = 0;
            let countM = countH * MINUTES[m/5] / 100;
            countM = getRandomInt(countM * 0.9, countM * 1.1);
            let weatherData = normalWeatherData(getWeatherData(date, h, m));
            let percent = getPercentByWeatherData(weatherData);
            countM = Math.round(countM * percent / 100);
            dayCount += countM;
            for(let i = 0; i< countM; ++i) {
                let index = getIndex();
                let object = getObject(index);
                if(!indexes[index + "-" + object]) {
                    indexes[index + "-" + object] = 1;
                } else {
                    indexes[index + "-" + object] += 1;
                }
                indexesLength++;
            }
            let ds = date.getFullYear()+'-'+pad(date.getMonth()+1)+'-'+pad(date.getDate())+' '+pad(h)+':'+pad(m)+':00';
            dataset.push(Object.assign({
                date: ds,
            }, weatherData, {indexesLength: indexesLength, indexes: JSON.stringify(indexes)}));
            //console.log(indexes);
            // console.log(date.yyyymmdd(), h, m, countM, normalWeatherData(getWeatherData(date)));
        }
    }
    saveFile(date, dataset);
    console.log("===========================");
    console.log("===========", dayCount);
    // console.log("===========", indexes);
}
