import os
from flask import Flask, request, send_from_directory
from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename
from PyPDF2 import PdfFileReader, PdfFileWriter
import glob
import shutil

UPLOAD_FOLDER = './upload_file/pdf/'
ALLOWED_EXTENSIONS = {'pdf'}


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


@app.route('/time')
def get_current_time():
	return {'time': time.time()} 

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
	print(session_id)

	paths = glob.glob(app.config['UPLOAD_FOLDER']+session_id+'/*'+session_id+'*.pdf')

	print(paths)

	merger(app.config['UPLOAD_FOLDER']+session_id+'/'+session_id+'.pdf',paths)

		
	
	return send_from_directory(app.config['UPLOAD_FOLDER']+session_id+'/', session_id+'.pdf', as_attachment=True)


@app.route('/DelSession', methods=['GET', 'POST'])
def DeleteSession():
	session_id = request.form['session_id']
	print(session_id)

	dir_path = '/tmp/img'

	try:
	    shutil.rmtree(app.config['UPLOAD_FOLDER']+session_id+'/')
	except OSError as e:
	    print("Error: %s : %s" % (dir_path, e.strerror))

	return {'status':'ok'}

