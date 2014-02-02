""" main.py is the top level script.

Return "Hello World" at the root URL.
"""

import os
import sys
import scrapeTab

# sys.path includes 'server/lib' due to appengine_config.py
from flask import Flask
from flask import render_template, request
app = Flask(__name__.split('.')[0])


@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        return render_template('root.html')
    else:
        list = scrapeTab.scrapeTabroom(request.form['url'])
        return render_template('final.html', list=list)

