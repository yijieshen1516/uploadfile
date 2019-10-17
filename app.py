from flask import Flask, render_template, redirect, url_for, request
from azure.storage.blob import BlockBlobService

app = Flask(__name__)

app.config['ACCOUNT'] = 'offsetpressurefiles'
app.config['STORAGE_KEY'] = 'lZ7pAwQhPRZ+SaTUGoN9I7uLVxFEDm9OxDOhMDXLUzUgDpaMKZs+2VrAa/ea4MFwCBV9YbKTANXtGMQw3+kJpA=='
app.config['CONTAINER'] = 'raw-file-landings'


blob_service = BlockBlobService(account_name=app.config['ACCOUNT'], account_key=app.config['STORAGE_KEY'])


@app.route('/')
def home():
    return 'Hello World!'


@app.route('/welcome')
def welcome():
    return render_template('profile.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credentials. Please try again.'
        else:
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['inputFile']
    try:
        blob_service.create_blob_from_stream(app.config['CONTAINER'], file.filename, file)
    except Exception:
        print('Exception=' + Exception)
        pass
    return 'Saved ' + file.filename + ' to azure blob storage'


if __name__ == '__main__':
    app.run(debug=True)
