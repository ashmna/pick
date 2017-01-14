const execSync = require('child_process').execSync;

let index = 0;

for(i = 3500; i <= 7000; i+= 200 ) {

  for(j = 2500; j >= 1000; j-= 100 ) {
      if(index > 275) {
        execSync(`wget http://api.openstreetmap.org/api/0.6/map?bbox=44.${i},40.${j},44.${i+200},40.${i-100} -O map/map_${index++}.osm`);
      } else {
        index++
      }
  }
}


console.log('done' , index);
