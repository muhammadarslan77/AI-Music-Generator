import streamlit as st
import numpy as np
import pretty_midi
from io import BytesIO
from pydub import AudioSegment
import os

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
    # Save the MIDI data to a temporary file
    midi_file_path = 'temp_midi.mid'
    midi_data.write(midi_file_path)
    
    # Convert the MIDI to WAV using pydub
    sound = AudioSegment.from_file(midi_file_path, format="mid")
    
    # Export the sound to a WAV file
    wav_file_path = 'temp_audio.wav'
    sound.export(wav_file_path, format='wav')
    
    return wav_file_path

# Streamlit app
st.title("AI Music Generator 🎵")
st.write("Generate random melodies using AI and download them as MIDI or listen as WAV files!")

# Button to generate melody
if st.button('Generate Melody'):
    melody = generate_melody()
    st.success('Melody generated!')

    # Convert the generated melody to a MIDI file
    midi_file = BytesIO()
    melody.write(midi_file)
    midi_file.seek(0)

    # Convert MIDI to WAV for playback
    wav_file_path = midi_to_wav(melody)
    
    # Read the WAV file back into a BytesIO object for Streamlit
    with open(wav_file_path, 'rb') as f:
        wav_audio = BytesIO(f.read())

    # Streamlit audio playback for WAV
    st.audio(wav_audio, format='audio/wav')

    # Allow user to download the MIDI file
    st.download_button(
        label="Download MIDI",
        data=midi_file,
        file_name="melody.mid",
        mime="audio/midi"
    )

    # Clean up the temporary files after usage
    os.remove(midi_file_path)
    os.remove(wav_file_path)
