#!/usr/bin/env bash
pip freeze | egrep "numpy|pandas|requests|click|terminaltables"
pip freeze | egrep "httpretty|sure|runipy|jsonschema"
