import os
from flask import Flask, render_template, redirect, url_for, request, flash, send_from_directory
from azure.storage.blob import BlockBlobService
from werkzeug.utils import secure_filename

app = Flask(__name__)

# azure blob storage key
app.config['ACCOUNT'] = 'offsetpressurefiles'
app.config['STORAGE_KEY'] = 'lZ7pAwQhPRZ+SaTUGoN9I7uLVxFEDm9OxDOhMDXLUzUgDpaMKZs+2VrAa/ea4MFwCBV9YbKTANXtGMQw3+kJpA=='
app.config['CONTAINER'] = 'raw-file-landings'
blob_service = BlockBlobService(account_name=app.config['ACCOUNT'], account_key=app.config['STORAGE_KEY'])


@app.route('/welcome')
def welcome():
    return render_template('profile.html')

# login route
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credentials. Please try again.'
        else:
            return redirect('/upload')
    return render_template('login.html', error=error)


ALLOWED_EXTENSIONS = {'pdf', 'png', 'csv'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_api(api):
    return len(api) == 14 and api.isdigit()


def append_filename(filename, api, timezone):
    parts = filename.split('.')
    return "".join(parts[:-1]) + '_' + api + '_' + timezone + '.' + parts[-1]


# upload file route
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    error = None
    if request.method == 'POST':
        file = request.files['file']
        api = request.form['wellAPI']
        timezone = request.form['timezone']
        if file.filename == '':
            error = 'No selected file'
        if file and allowed_file(file.filename) and allowed_api(api):
            filename = secure_filename(file.filename)
            filename = append_filename(filename, api, timezone)
            try:
                blob_service.create_blob_from_stream(app.config['CONTAINER'], filename, file)
                error = 'file successfully saved in azure blob storage'
            except Exception:
                error = 'Exception=' + Exception
            return render_template('upload.html', error=error)
        elif not allowed_file(file.filename):
            error = 'Please select a file and allowed file is txt, csv and png'
        elif not allowed_api(api):
            error = 'Please enter an API number and allowed API length is 14'
    return render_template('upload.html', error=error)


@app.route('/upload_form')
def upload_form():
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
