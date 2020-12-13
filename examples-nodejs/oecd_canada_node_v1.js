// -*- coding: utf-8 -*-
// This file is part of https://github.com/26fe/jsonstat.py
// Copyright (C) 2016-2021 gf <gf@26fe.com>
// See LICENSE file

// this nodejs script create a cvs file and store it to
// the fixture file
// the created file contains a to_table trasformation
// so it is possible to compare output of nodejs
// and python library

// to use this file on command line execute
// cd <thisdir>
// npm install
// nodejs oecd_canada_node_v1.js

// stdlib
var fs        = require('fs');
var path      = require('path');

// modules
var JSONstat = require('jsonstat');
// csv library http://csv.adaltas.com/csv/examples/
var csv       = require('csv');

var common = require("./common");

var fixtures_dir      = path.join(__dirname, "..", "tests", "fixtures")
var json_pathname     = path.join(fixtures_dir, "json-stat.org", "oecd-canada.json");
var to_table_pathname = path.join(fixtures_dir, "output_from_nodejs", "oecd-canada-to_table.csv");


if(! fs.existsSync(json_pathname)) {
    console.log("file not exists");
} else {
    console.log("reading file '" + json_pathname + "'")
    var json_string = fs.readFileSync(json_pathname).toString();

    var json_data = JSON.parse(json_string);
    var J         = JSONstat(json_data);
    var oecd   = J.Dataset(0);
    var canada = J.Dataset(1);

    console.log("category: " + J.Dataset(0).Dimension(0).label);

    common.jsonstat_to_table(json_string, to_table_pathname);
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

