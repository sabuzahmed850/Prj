import fitz  # PyMuPDF
import pyttsx3
import tkinter as tk
from tkinter import filedialog

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

def read_text_aloud(text):
    """Read text aloud using pyttsx3."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Change voice if needed
    engine.setProperty('rate', 150)  # Adjust speech rate
    engine.say(text)
    engine.runAndWait()

def select_pdf_and_read():
    """Open file dialog to select a PDF and read its content aloud."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if pdf_path:
        text = extract_text_from_pdf(pdf_path)
        read_text_aloud(text)
    else:
        print("No file selected.")

if __name__ == "__main__":
    select_pdf_and_read()
