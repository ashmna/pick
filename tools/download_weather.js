const execSync = require('child_process').execSync;
Date.prototype.yyyymmdd = function() {
  var mm = this.getMonth() + 1; // getMonth() is zero-based
  var dd = this.getDate();
  mm = mm < 10 ? '0'+ mm : mm;
  dd = dd < 10 ? '0'+ dd : dd;
  return [this.getFullYear(), mm, dd].join(''); // padding
};

var now = new Date();



for (var d = new Date(2016, 7, 1); d <= now; d.setDate(d.getDate() + 1)) {
    let date = new Date(d);
    execSync(`wget http://api.wunderground.com/api/ae155f8b19bf54f0/history_${date.yyyymmdd()}/q/CA/Yerevan.json -O weather/history_${date.yyyymmdd()}.json`);
}

