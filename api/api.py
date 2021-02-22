import os
from flask import Flask, request, send_from_directory, json
from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename
from PyPDF2 import PdfFileReader, PdfFileWriter
import glob
import shutil
from pdf2image import convert_from_path
from zipfile import ZipFile
from os.path import basename

UPLOAD_FOLDER = './upload_file/pdf/'
ALLOWED_EXTENSIONS = {'pdf'}

TARGET_SPLIT_FILE_NAME = 'TARGET_SPLIT_FILE_NAME.pdf'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def merger(output_path, input_paths):
	pdf_writer = PdfFileWriter()
	for path in input_paths:
		pdf_reader = PdfFileReader(path)
		for page in range(pdf_reader.getNumPages()):
			pdf_writer.addPage(pdf_reader.getPage(page))
	with open(output_path,'wb') as fh:
		pdf_writer.write(fh)




def allowed_file(filename):
	return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		session_id = request.form['session_id']
		

		file = request.files['file']

		if file and allowed_file(file.filename):
			filename = session_id + secure_filename(file.filename)

			if not os.path.exists(app.config['UPLOAD_FOLDER']+session_id):
			 	os.makedirs(app.config['UPLOAD_FOLDER']+session_id)

			file.save(os.path.join(app.config['UPLOAD_FOLDER']+session_id, filename))
			
		return {'filename':'f_name'}

@app.route('/joinPdf', methods=['GET', 'POST'])
def JoinPdf():
	session_id = request.form['session_id']
	paths = glob.glob(app.config['UPLOAD_FOLDER']+session_id+'/*'+session_id+'*.pdf')
	merger(app.config['UPLOAD_FOLDER']+session_id+'/'+session_id+'.pdf',paths)

		
	
	return send_from_directory(app.config['UPLOAD_FOLDER']+session_id+'/', session_id+'.pdf', as_attachment=True)


@app.route('/DelSession', methods=['GET', 'POST'])
def DeleteSession():
	session_id = request.form['session_id']
	try:
	    shutil.rmtree(app.config['UPLOAD_FOLDER']+session_id+'/')
	except OSError as e:
	    print("Error: %s : %s" % (app.config['UPLOAD_FOLDER']+session_id+'/', e.strerror))

	return {'status':'ok'}

@app.route('/DelSingleFile', methods=['GET', 'POST'])
def DelSingleFile():
	session_id = request.form['session_id']
	filename = session_id + secure_filename(request.form['file_name'])

	try:
	    os.remove(os.path.join(app.config['UPLOAD_FOLDER']+session_id, filename))
	except OSError as e:
	    print("Error: %s : %s" % (app.config['UPLOAD_FOLDER']+session_id+'/'+file_name, e.strerror))
	    return {'status':'error'}

	return {'status':'ok'}



@app.route('/splitUpload', methods=['GET', 'POST'])
def splitUpload():
	if request.method == 'POST':
		session_id = request.form['session_id']
		

		file = request.files['file']

		if file and allowed_file(file.filename):
			filename = TARGET_SPLIT_FILE_NAME

			if not os.path.exists(app.config['UPLOAD_FOLDER']+session_id):
			 	os.makedirs(app.config['UPLOAD_FOLDER']+session_id)

			folder_name = app.config['UPLOAD_FOLDER']+session_id;
			filePath = os.path.join(folder_name, filename)

			file.save(filePath)

			
			
		return {'status':'ok'}


@app.route('/getImagePages', methods=['GET', 'POST'])
def getImagePages():
	if request.method == 'POST':
		session_id = request.form['session_id']
		filename = TARGET_SPLIT_FILE_NAME
		folder_name = app.config['UPLOAD_FOLDER']+session_id;
		filePath = os.path.join(folder_name, filename)

		

		pages = convert_from_path(filePath, 100)
		result = []
		pages_array = {}
		for i, page in enumerate(pages):
			n = str(i)+'-out.jpg';
			page.save(folder_name+'/'+n, 'JPEG')
			pages_array[int(i+1)] =n
			result.append(n)
		#result['session_id'] = session_id
		#result['pages'] = pages_array

		print(result)
			
		return json.dumps(result)


@app.route('/image', methods=["GET"])
def image():
	session_id = request.args.get('id')
	file_name = request.args.get('n')
	return send_from_directory(app.config['UPLOAD_FOLDER']+session_id+'/', file_name, mimetype='image/jpg')

def splitAllPage(session_id):
	folder_location = app.config['UPLOAD_FOLDER']+session_id+'/'
	file = app.config['UPLOAD_FOLDER']+session_id+'/'+TARGET_SPLIT_FILE_NAME
	inputpdf = PdfFileReader(open(file, "rb"))

	for i in range(inputpdf.numPages):
	    output = PdfFileWriter()
	    output.addPage(inputpdf.getPage(i))
	    with open(folder_location+"document-page-%s.pdf" % i, "wb") as outputStream:
	        output.write(outputStream)

def splitByRange(session_id, str_range):
	
	folder_location = app.config['UPLOAD_FOLDER']+session_id+'/'
	file = app.config['UPLOAD_FOLDER']+session_id+'/'+TARGET_SPLIT_FILE_NAME
	inputpdf = PdfFileReader(open(file, "rb"))

	page_range = str_range.split(',');
	for idx, val in enumerate(page_range):
		page = val.replace(' ','').split('-')
		
		if len(page) == 1:
			output = PdfFileWriter()
			output.addPage(inputpdf.getPage(int(page[0])-1))
			with open(folder_location+"document-page-%s.pdf" % str(idx + 1), "wb") as outputStream:
				output.write(outputStream)
		else:
			output = PdfFileWriter()
			for i in range(int(page[0])-1, int(page[1])):
				output.addPage(inputpdf.getPage(i))
			with open(folder_location+"document-page-%s.pdf" % str(idx + 1), "wb") as outputStream:
					output.write(outputStream)




@app.route('/downloadSplitedPdf', methods=['POST'])
def downloadSplitedPdf():

	session_id = request.form['session_id']
	extract_all = request.form['extract_all']
	page_range = request.form['range']
	if(extract_all == "true"):
		splitAllPage(session_id)
		createZipFile(session_id)
		return send_from_directory(app.config['UPLOAD_FOLDER']+session_id+'/', 'splitedFiles.zip', as_attachment=True)
	else:
		splitByRange(session_id, page_range)
		createZipFile(session_id)
		return send_from_directory(app.config['UPLOAD_FOLDER']+session_id+'/', 'splitedFiles.zip', as_attachment=True)

	


def createZipFile(session_id):
	folder_location = app.config['UPLOAD_FOLDER']+session_id+'/'
	zipObj = ZipFile(folder_location+'splitedFiles.zip', 'w')

	paths = glob.glob(folder_location+'document-page-*.pdf')
	sorted_path = sorted(paths)
	for i in sorted_path:
		zipObj.write(i,  basename(i))

	zipObj.close()



