from flask import Flask, render_template
import os, json
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/shiyanlou'

path = '/home/shiyanlou/files/'
extend = '.json'

db = SQLAlchemy(app)

class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<Category %r>'% self.name

class File(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80))
	created_time = db.Column(db.DateTime)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
	category = db.relationship('Category', backref=db.backref('posts', lazy='dynamic'))
	content = db.Column(db.Text)

	def __init__(self, title, created_time, category, content):
		self.title = title
		self.created_time = created_time
		self.category = category
		self.content = content

	def __repr__(self):
		return '<File %r>' % self.title

@app.route('/')
def index():
	files = File.query.all()
	return render_template('index.html', titles=files)

@app.errorhandler(404)
def nothing(nothing):
	return render_template('404.html'), 404

@app.route('/files/<int:id>')
def file(id):
	fileItem = File.query.filter_by(id=id).first()
	if not hasattr(fileItem, 'title'):
		return render_template('404.html'), 404

	return render_template('file.html', fileObj=fileItem)


def readJsonFile(filePath):
	fileContent = {}
	with open(filePath, 'r') as f:
		fileContent = json.load(f)
	return fileContent

def getPathAllJson(path):
	paths = []
	for root, dirs, files in os.walk(path):
		for itemFile in files:
			if os.path.splitext(itemFile)[1] == '.json':
				paths.append(os.path.join(root, itemFile))
	return paths

def getFilePath(filename):
	return path + filename + extend
if __name__ == '__main__':
	app.run(port=3000)