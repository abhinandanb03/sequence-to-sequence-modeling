import os
from flask import Flask, flash, request, redirect, render_template, url_for
from pydantic import FilePath
from werkzeug.utils import secure_filename
from speechToText import transcribe_streaming
from videoConverter import convert_video_to_audio_ffmpeg
from summarizer import summarize
import sys
from flask import Flask, flash, request, redirect, url_for, render_template
import os
import urllib.request

app = Flask(__name__)
  
UPLOAD_FOLDER = 'static/uploads/'
 
app = Flask(__name__)
app.secret_key = "cairocoders-ednalan"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
  
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif','mp4','wav'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
@app.route('/')
def upload_form():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_video():
    if 'files[]' not in request.files:
        flash('No file part')
        return redirect(request.url)
    files = request.files.getlist('files[]')
    file_names = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_names.append(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(request.url)

        file_path = "static/uploads" +'/'+ filename
        convert_video_to_audio_ffmpeg(file_path)
        file_path = file_path[ : file_path.index('.')]
        file_path = file_path + ".wav"
        
        text = transcribe_streaming(file_path)
        
        file = open("transcribed_data.txt", "w")  
        file.write(text)
        file.write("\n")
        file.close()

    f = open("transcribed_data.txt", "r")
    transcribed_text = f.read()
    summary = summarize(transcribed_text)
    flash(summary)

    return render_template('index.html', filenames=file_names)
    

@app.route('/display/<filename>')
def display_video(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
  
if __name__ == "__main__":
    app.run()