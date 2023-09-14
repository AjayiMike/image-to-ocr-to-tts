from flask import Flask, request, jsonify
from gtts import gTTS
import tempfile
import PIL.Image
import cv2
from pytesseract import Output
import pytesseract
import pyttsx3

app = Flask(__name__)


'''
def assure_path_exists(path):
  try:
      dir = os.path.dirname(path)
      if not os.path.exists(dir):
          os.makedirs(dir)
  except:
      print('Error has occured')

# Your OCR functionality should be implemented here
def perform_ocr(img, config=2):
    
    ocr_result = ocreg(img, config=2)
    return ocr_result

def speak_t(text):
    t = speak_text(text)
    return t

@app.route('/ocr/<str:image>/<int:config>', methods=['GET','POST'])
def ocr_endpoint():
    if request.method == 'POST':
        try:
            image1 = request.files['image1']
            path = 'image/jpeg/'
            assure_path_exists(path)
            image1.save(path+image1.filename)
            image = path+image1.filename

            if not image:
                return jsonify({'error': 'No input'}), 400
            
            ocr_result = perform_ocr(image, config=2)

            speak = speak_t(ocr_result)
            
            # Generate audio from OCR result
            audio_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
            tts = gTTS(text=ocr_result, lang='en')
            tts.save(audio_file.name)
            
            return jsonify({'ocr_result': ocr_result, 'audio_url': audio_file.name, 'rt_speak': speak})
        except Exception as e:
            return jsonify({'error': str(e)}), 500'''

# Initialize the engine
engine = pyttsx3.init()

"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female


# Function to convert text to speech
def speak_text(command):
    engine.say(command)
    engine.runAndWait()

def ocreg(img, config = 2):
    if not isinstance(img, str):
        return ValueError("Input must be a jpg file")
    if not isinstance(config, int):
        return ValueError("Interger value required")
    
    if config == 1:
        myconfig = r"--psm 4 --oem 3"
    elif config == 2:
        myconfig = r"--psm 5 --oem 3"
    elif config == 3:
        myconfig = r"--psm 6 --oem 3"
    elif config == 4:
        myconfig = r"--psm 7 --oem 3"
    elif config == 5:
        myconfig = r"--psm 8 --oem 3"
    elif config == 6:
        myconfig = r"--psm 9 --oem 3"
    else:
        myconfig = r"--psm 6 --oem 3"


    # data = pytesseract.image_to_data(img, config=myconfig, output_type=Output.DICT)
    data = pytesseract.image_to_string(PIL.Image.open(img), config = myconfig)
    return data


@app.route('/sum', methods=['POST'])
def hello():
        try:
            req_j = request.get_json()
            img = req_j["image"]
            config = req_j["config"]
            
            txt = ocreg(img, config=config)

            # speak = speak_text(txt)
            
            # Generate audio from OCR result
            audio_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
            
            # Languages code:['en', 'fr', 'zh-CN', 'zh-TW', 'pt', 'es']
            # Top-level domain: []
            tts = gTTS(text=txt, lang='en', tld='com.au') 
            tts.save(audio_file.name)
            
            return {"result": txt, 
                    "audio_url":audio_file.name,}
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 50100, debug=True)
