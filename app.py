from flask import *
import time

from pythonscripts.english import *
from pythonscripts.extract import *

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

@app.route('/editor')
def display_editor():
    return render_template('editor.html')

@app.route('/evaluation', methods = ['POST'])
def evaluate():
    text = request.form['it']
    open('document.txt', 'w', encoding='utf-8').write(text)
    return render_template('evaluator.html')

@app.route('/secret')
def evaluation_secret():
    text = open('document.txt', 'r', encoding='utf-8').read()
    doc = Document(text)
    doc.evaluate()
    return '<h1>Analysis of your document: </h1>'+doc.returnHTML()

@app.route('/sources')
def show_search():
    return render_template('search.html')

@app.route('/results', methods = ['POST'])
def show_results():
    text = request.form['query']
    open('document.txt', 'w', encoding='utf-8').write(text)
    return render_template('results.html')

@app.route('/secretrequest')
def search_secret():
    text = open('document.txt', 'r', encoding='utf-8').read()
    return '<h1>Sources</h1>' + return_html(text)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
