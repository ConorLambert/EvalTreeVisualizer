from flask import Flask, render_template, request, flash, redirect, url_for, abort
from sqlparser import Parser
from buchheim import buchheim

app = Flask(__name__)
app.config['SECRET_KEY'] = '~t\x86\xc9\x1ew\x8bOcX\x85O\xb6\xa2\x11kL\xd1\xce\x7f\x14<y\x9e'
app.config['DEBUG'] = True

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
	query=request.form['query']
	parser = Parser()	
	tree = parser.execute(query)
	drawTree = buchheim(tree)
	return render_template('query.html', tree=drawTree)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
	
if __name__ == '__main__':
  app.run(host="127.0.0.1",port=int("5000"))
  #app.run()


