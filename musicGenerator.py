import streamlit as st
import numpy as np
import pretty_midi
from io import BytesIO
from pydub import AudioSegment
import os
import tempfile
AudioSegment.converter = "ffmpeg"
AudioSegment.ffmpeg = "ffmpeg"
AudioSegment.ffprobe = "ffprobe"

# Set the paths to ffmpeg and ffprobe
AudioSegment.converter = r'C:\Path\To\ffmpeg.exe'  # Update with the actual path to ffmpeg
AudioSegment.ffmpeg = r'C:\Path\To\ffmpeg.exe'  # Same path for ffmpeg
AudioSegment.ffprobe = r'C:\Path\To\ffprobe.exe'  # Update with the actual path to ffprobe

# Function to generate a random MIDI melody
def generate_melody():
    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)
    
    for i in range(8):
        note = pretty_midi.Note(velocity=100, pitch=np.random.randint(60, 72),
                                start=i * 0.5, end=(i + 1) * 0.5)
        instrument.notes.append(note)
    
    midi.instruments.append(instrument)
    return midi

# Function to convert MIDI to WAV using pydub
def midi_to_wav(midi_data):
    with tempfile.TemporaryDirectory() as tmpdirname:
        midi_file_path = os.path.join(tmpdirname, 'temp_midi.mid')
        
        # Save the MIDI data to a temporary file
        midi_data.write(midi_file_path)
        print(f"MIDI file written to: {midi_file_path}")  # Debug statement
        
        try:
            sound = AudioSegment.from_file(midi_file_path, format="mid")
        except Exception as e:
            st.error(f"Error converting MIDI to WAV: {e}")
            return None
        
        wav_file_path = os.path.join(tmpdirname, 'temp_audio.wav')
        sound.export(wav_file_path, format='wav')
        
        return wav_file_path

# Streamlit app
st.title("AI Music Generator 🎵")
st.write("Generate random melodies using AI and download them as MIDI or listen as WAV files!")

# Button to generate melody
if st.button('Generate Melody'):
    melody = generate_melody()
    st.success('Melody generated!')

    midi_file = BytesIO()
    melody.write(midi_file)
    midi_file.seek(0)

    wav_file_path = midi_to_wav(melody)
    
    if wav_file_path:
        with open(wav_file_path, 'rb') as f:
            wav_audio = BytesIO(f.read())

        st.audio(wav_audio, format='audio/wav')

        st.download_button(
            label="Download MIDI",
            data=midi_file,
            file_name="melody.mid",
            mime="audio/midi"
        )
