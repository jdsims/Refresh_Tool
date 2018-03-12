#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright © 2017 - 2018 Acumen Solutions, Inc. The Sandbox Refresh Tool was
# created by Acumen Solutions. Except for the limited rights to use and make
# copies of the Software as provided in a License Agreement, all rights are
# reserved.

from bottle import get, run, default_app, response
import controller as controller_

app = application = default_app()

@get('/refreshtool/oncompleterefresh/<org_name>/<server>')
def on_complete_refresh(org_name, server):
    controller_.RefreshMethods.on_complete_refresh(org_name, server)
    response.status = 200
    return response

if __name__ == '__main__':
	run(host='172.31.32.57', port=8000, debug=True)
