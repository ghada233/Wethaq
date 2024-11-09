# tts_utils.py
import torch
from TTS.api import TTS
import os

# Get device (GPU or CPU)
device = "cuda" if torch.cuda.is_available() else "cpu"

# Initialize a global variable for the TTS model
tts = None

def init_tts_model():
    """
    Initialize the TTS model. This should be called only once.
    """
    global tts
    if tts is None:
        try:
            print("Initializing the TTS model...")
            tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
            print("TTS model loaded successfully.")
        except Exception as e:
            print(f"Error loading TTS model: {e}")

def text_to_speech(text, output_filename="output.wav", language="ar"):
    """
    Convert text to speech and save to an output file.
    
    Args:
    - text: Text to be converted to speech.
    - output_filename: Output file name to save the generated audio.
    - language: Language for speech generation (default is Arabic "ar").
    
    Returns:
    - path to the saved audio file.
    """
    # Ensure the model is initialized
    if tts is None:
        init_tts_model()

    # Define the full path for the output file
    file_path = os.path.join(os.getcwd(), output_filename)

    # Convert the text to speech and save to the file
    tts.tts_to_file(text=text, speaker_wav=file_path, language=language)
    print(f"Speech saved to {file_path}")
    return file_path

