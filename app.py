import os
import fitz  # PyMuPDF
from flask import Flask, request, render_template_string, send_file, redirect, url_for
from gtts import gTTS

app = Flask(__name__)

# Configure upload and audio directories
UPLOAD_FOLDER = 'uploads'
AUDIO_FOLDER = 'audio'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            return "No file part", 400
        file = request.files['pdf_file']
        if file.filename == '':
            return "No file selected", 400
        if file:
            pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(pdf_path)

            # Extract text from the PDF
            text = extract_text_from_pdf(pdf_path)

            # Convert text to speech using gTTS
            tts = gTTS(text)
            audio_filename = file.filename.rsplit('.', 1)[0] + ".mp3"
            audio_path = os.path.join(AUDIO_FOLDER, audio_filename)
            tts.save(audio_path)

            # Redirect to a page where the user can play/download the audio
            return redirect(url_for('play_audio', filename=audio_filename))
    # Simple HTML form for file upload
    html = '''
    <!doctype html>
    <html>
      <head>
        <title>PDF to Speech</title>
      </head>
      <body>
        <h1>Upload a PDF to Listen to Its Content</h1>
        <form method="post" enctype="multipart/form-data">
          <input type="file" name="pdf_file" accept=".pdf" required>
          <input type="submit" value="Upload">
        </form>
      </body>
    </html>
    '''
    return render_template_string(html)


@app.route('/audio/<filename>')
def play_audio(filename):
    # HTML page to play the audio file
    html = f'''
    <!doctype html>
    <html>
      <head>
        <title>Listen to Audio</title>
      </head>
      <body>
        <h1>Your PDF has been converted to Speech!</h1>
        <audio controls>
          <source src="/download/{filename}" type="audio/mpeg">
          Your browser does not support the audio element.
        </audio>
        <br>
        <a href="/download/{filename}">Download Audio</a>
      </body>
    </html>
    '''
    return render_template_string(html)


@app.route('/download/<filename>')
def download_file(filename):
    audio_path = os.path.join(AUDIO_FOLDER, filename)
    return send_file(audio_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
