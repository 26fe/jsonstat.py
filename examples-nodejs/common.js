
var fs        = require('fs');
var JSONstat = require('jsonstat');
var csv       = require('csv');

exports.jsonstat_to_table = function jsonstat_to_table(json_string, to_table_pathname) {
    var json_data = JSON.parse(json_string);
    var J         = JSONstat(json_data);
    var oecd   = J.Dataset(0);
    var canada = J.Dataset(1);

    var ret = oecd.toTable();
    console.log("write oecd dataset in file '" + to_table_pathname + "'")

    csv.stringify(ret, function(err, output){
    var fd = fs.openSync(to_table_pathname, "w");
      fs.writeSync(fd, output);
      fs.closeSync(fd);
    });
}
