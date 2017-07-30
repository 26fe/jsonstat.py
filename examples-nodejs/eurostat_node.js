// -*- coding: utf-8 -*-
// This file is part of https://github.com/26fe/jsonstat.py
// Copyright (C) 2016-2017 gf <gf@26fe.com>
// See LICENSE file

// this nodejs script create a cvs file and store it to
// the fixture file
// the created file contains a to_table transformation
// so it is possible to compare output of nodejs
// and jsonstat.py python library

// to use this file on command line execute
// cd <thisdir>
// npm install
// nodejs eurostat_node.js

// stdlib
var fs        = require('fs');
var path      = require('path');

// modules
var JSONstat = require('jsonstat');
// csv library http://csv.adaltas.com/csv/examples/
var csv       = require('csv');

var fixtures_dir      = path.join(__dirname, "..", "tests", "fixtures")
var json_pathname     = path.join(fixtures_dir, "eurostat", "eurostat-name_gpd_c-geo_IT.json");
var to_table_pathname = path.join(fixtures_dir, "output_from_nodejs", "eurostat-name_gpd_c-geo_IT-to_table.csv");

function jsonstat_to_table(json_string) {
    var json_data = JSON.parse(json_string);
    var J         = JSONstat(json_data);
    var dataset   = J.Dataset(0);

    var ret = dataset.toTable();
    console.log("write toTable() file '" + to_table_pathname + "'")

    csv.stringify(ret, function(err, output){
    var fd = fs.openSync(to_table_pathname, "w");
      fs.writeSync(fd, output);
      fs.closeSync(fd);
    });
}

if(! fs.existsSync(json_pathname)) {
    console.log("input file do not exist");
} else {
    console.log("reading input file '" + json_pathname + "'")
    var json_string = fs.readFileSync(json_pathname).toString();
    jsonstat_to_table(json_string);
}

// var http     = require('http');
// conf
// var uri="http://json-stat.org/samples/oecd-canada.json";
//function http_get_callback(response) {
//    var str = '';
//
//    //another chunk of data has been received, so append it to `str`
//    response.on('data', function (chunk) {
//        str += chunk;
//    });
//
//    //the whole response has been received
//    response.on('end', function () {
//        // console.log(str);
//        jsonstat_test(str);
//    });
//}
// http.request(uri, http_get_callback).end();

