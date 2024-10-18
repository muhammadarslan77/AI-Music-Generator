import streamlit as st
import numpy as np
import pretty_midi
import os
from io import BytesIO
from pydub import AudioSegment

# Function to generate a random MIDI melody
def generate_melody():
    # Create a PrettyMIDI object
    midi = pretty_midi.PrettyMIDI()
    
    # Create an instrument (a piano instrument in this case)
    instrument = pretty_midi.Instrument(program=0)  # Program 0 is a piano
    
    # Generate random notes for the melody
    for i in range(8):
        # Create a note with random pitch, velocity, and start/end times
        note = pretty_midi.Note(velocity=100, pitch=np.random.randint(60, 72),
                                start=i * 0.5, end=(i + 1) * 0.5)
        instrument.notes.append(note)
    
    # Add the instrument to the PrettyMIDI object
    midi.instruments.append(instrument)
    
    # Return the PrettyMIDI object
    return midi

# Function to convert MIDI to WAV using pydub (requires ffmpeg)
def midi_to_wav(midi_data):
    # Save the MIDI data to a temporary file
    tmp_midi = BytesIO()
    midi_data.write(tmp_midi)
    tmp_midi.seek(0)
    
    # Convert the MIDI to WAV using pydub (requires ffmpeg to be installed)
    sound = AudioSegment.from_file(tmp_midi, format="mid")
    
    # Export the sound to a WAV file
    tmp_wav = BytesIO()
    sound.export(tmp_wav, format="wav")
    tmp_wav.seek(0)
    
    return tmp_wav

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
    wav_audio = midi_to_wav(melody)

    # Streamlit audio playback for WAV
    st.audio(wav_audio, format='audio/wav')

    # Allow user to download the MIDI file
    st.download_button(
        label="Download MIDI",
        data=midi_file,
        file_name="melody.mid",
        mime="audio/midi"
    )
