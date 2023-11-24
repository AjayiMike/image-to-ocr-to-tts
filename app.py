from flask import Flask, url_for, render_template, request, send_from_directory
from gtts import gTTS
import tempfile
import os
from PIL import Image
import pytesseract
from flask_uploads import UploadSet, configure_uploads, IMAGES, TEXT, DOCUMENTS

import random
from pdf import saveToPDF
from flask_socketio import SocketIO, emit


app = Flask(__name__)


# Path for current location
project_dir = os.path.dirname(os.path.abspath(__file__))
audio_directory = os.path.join(os.getcwd(), 'audio_output')
pdf_directory = os.path.join(os.getcwd(), 'audio_pdfs')


photos = UploadSet('photos', IMAGES)
app.config["UPLOADED_PHOTOS_DEST"] = "images"
configure_uploads(app, photos)



# WebSocket Configs and handlers
socketio = SocketIO(app, logger=True, engineio_logger=True)
TaskByIdStore: dict[int, str] = dict();


@socketio.on('connect')
def connect():
    print("connection received from client id:", request.sid);
    return request.sid;


@socketio.on('status')
def status(data):
    try:
        task_id = data.get('_task_id');
        print("[STATUS-TASKID]: ", data.get('_task_id'));

        image_filename = TaskByIdStore.get(task_id);

        if ( not image_filename ):
            emit('status', {'_task_id': task_id, 'error': 'true', 'message':'invalid task id'});
            return;

        # Class instance 
        textObject = GetText(image_filename);
        text_result = textObject.file;

        pdf_filename = saveToPDF(text_result)
        pdf_file_url = url_for('download_pdf', pdf_filename=pdf_filename);
        print("[PDF FILE URL]: ", pdf_file_url);

        print(text_result);
        emit('status', {'_task_id': task_id, 'done': 'false', 'payload': { 'message':text_result, 'pdf_url': pdf_file_url },  'progress': 65});

        # Mimicking long running job
        # from time import sleep
        # sleep(8);

        audio_result = GetAudio(text_result)
        audio_file_name=os.path.basename(audio_result.file_name)

        print(audio_file_name)
        audio_file_url = url_for('download_file', filename=audio_file_name)

        emit('status', {'_task_id': task_id, 'error': 'false', 'message':audio_file_url , 'done': 'true'});
    except Exception as err:
        print(err);
        emit('status', {'_task_id': task_id, 'error': 'true', 'message':'Error Translating Audio, Please Try Again ... ' , 'done': 'true'});



# Class for Image to Text
class GetText(object):
    def __init__(self, file):
        self.file = pytesseract.image_to_string(Image.open(project_dir + '/images/' + file))


# Class for Text to Audio
    # Languages code:['en', 'fr', 'zh-CN', 'zh-TW', 'pt', 'es']
    # Top-level domain: []
class GetAudio(object):
    def __init__(self, text, lang = "en", tld='com.au'):

        # Create a subdirectory named 'audio_output' (if it does not exist yet) in the current working directory
        # audio_directory = os.path.join(os.getcwd(), 'audio_output')
        os.makedirs(audio_directory, exist_ok=True)

        # create a temp audio file with random name
        self.file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False, dir=audio_directory)
        self.file_name = self.file.name

        # generate the audio
        tts = gTTS(text=text, lang=lang, tld=tld) 

        # save the audio output into the audio file created up here
        tts.save(self.file_name)



# Home page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Check if the form is empty
        if 'photo' not in request.files:
            return 'there is no photo in form'
        
        photo = request.files['photo']
        path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], photo.filename)

        # Save the photo in the upload folder
        photo.save(path)
        
        task_id = random.randbytes(32).hex()
        TaskByIdStore[task_id] = photo.filename
        
        print("[Task Created]: ", task_id);
        return render_template('index.html', image_task_id=task_id)
    return render_template('index.html')


@app.route('/audio/<filename>')
def download_file(filename):
    return send_from_directory(audio_directory, filename, as_attachment=True);


@app.route('/pdf/<pdf_filename>')
def download_pdf(pdf_filename):
    return send_from_directory(pdf_directory, pdf_filename, as_attachment=True);


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port= 8000, debug=True);