from flask import Flask, render_template
import os, json


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
path = '/home/shiyanlou/files/'
extend = '.json'

@app.route('/')
def index():
	allPath = getPathAllJson(path)
	titles = []
	for p in allPath:
		res = readJsonFile(p)
		print(res['title'])
		titles.append(res['title'])

	return render_template('index.html', titles=titles)

@app.route('/<nothing>')
def nothing(nothing):
	return render_template('404.html'), 404

@app.route('/files/<filename>')
def file(filename):
	filePath = getFilePath(filename)

	if not os.path.exists(filePath):
		return render_template('404.html'), 404

	fileObj = readJsonFile(filePath)

	return render_template('file.html', fileObj=fileObj)


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