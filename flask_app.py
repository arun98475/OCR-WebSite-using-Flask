import os
from flask import*
from werkzeug.utils import secure_filename
from ocr import TextExtract

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
DOWNLOAD_FOLDER = 'temp'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.secret_key='wilto'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/')
def index():    
    return render_template("index.html")
       

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part','warning')
            return redirect(url_for('index'))
        file = request.files['file']
        if file.filename == '':
            flash('No selected file','warning')
            return redirect(url_for('index'))
        if not allowed_file(file.filename):
            flash("please upload your file in .png, .jpg, .jpeg, .gif format","warning")
            return redirect(url_for('index'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            result=TextExtract(f'uploads/{filename}')
            new_file=result.output_file_name()
            print(new_file)
            response=make_response(render_template('index.html',filename={"file":new_file}))
            return response
    return redirect(url_for("index"))

@app.route('/download/<filename>',methods = ['GET'])
def download(filename):
    print(filename)
    try:
        return send_from_directory(DOWNLOAD_FOLDER, filename=filename, as_attachment=True)
    except FileNotFoundError:
        print("file not found")      


if __name__ == '__main__':
    app.run()
