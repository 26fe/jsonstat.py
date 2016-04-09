# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file


def lst2html(lst):
    html = "<table>"
    for r in lst:
        html += "<tr>"
        for c in r:
            html += "<td>{}</td>".format(c)
        html += "</tr>"
    html += "</table>"
    return html
