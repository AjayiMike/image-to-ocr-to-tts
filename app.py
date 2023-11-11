from flask import Flask, url_for, render_template, request, send_from_directory
from gtts import gTTS
import tempfile
import os
from PIL import Image
import pytesseract
from flask_uploads import UploadSet, configure_uploads, IMAGES

# Path for current location
project_dir = os.path.dirname(os.path.abspath(__file__))
audio_directory = os.path.join(os.getcwd(), 'audio_output')

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)
app.config["UPLOADED_PHOTOS_DEST"] = "images"
configure_uploads(app, photos)

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
        audio_directory = os.path.join(os.getcwd(), 'audio_output')
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
        
        # Class instance 
        textObject = GetText(photo.filename)
        text_result = textObject.file
        print(text_result)

        audio_result = GetAudio(text_result)

        audio_file_name=os.path.basename(audio_result.file_name)

        print(audio_file_name)
        
        audio_file_url = url_for('download_file', filename=audio_file_name)
        return render_template('index.html', audio_file_url=audio_file_url)
    return render_template('index.html')


@app.route('/audio/<filename>')
def download_file(filename):
    return send_from_directory(audio_directory, filename, as_attachment=True)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 8000, debug=True)
