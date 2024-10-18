import streamlit as st
import pretty_midi
import numpy as np
from pydub import AudioSegment
import io
import tempfile

# Set up the Streamlit app interface
st.title('AI Music Generator 🎵')
st.write("Generate random melodies using AI and download them as MIDI and WAV files!")

# Sidebar options for user input
st.sidebar.header("Melody Settings")
num_notes = st.sidebar.slider('Number of Notes', 5, 50, 10)
tempo = st.sidebar.slider('Tempo (BPM)', 60, 180, 120)

# Function to generate a random melody
def generate_melody(num_notes, tempo):
    midi = pretty_midi.PrettyMIDI()
    
    # Select an instrument (Acoustic Grand Piano)
    instrument_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
    instrument = pretty_midi.Instrument(program=instrument_program)
    
    # Generate random notes
    for i in range(num_notes):
        note_number = np.random.randint(60, 72)  # Random note between C4 and B4
        start_time = i * (60.0 / tempo)  # Space notes based on tempo (seconds per note)
        end_time = start_time + (60.0 / tempo) * 0.75  # Duration of each note
        note = pretty_midi.Note(velocity=100, pitch=note_number, start=start_time, end=end_time)
        instrument.notes.append(note)

    # Add instrument to the PrettyMIDI object
    midi.instruments.append(instrument)
    return midi

# Function to convert MIDI to WAV
def midi_to_wav(midi):
    with tempfile.NamedTemporaryFile(delete=False) as tmp_midi:
        midi.write(tmp_midi.name)
        sound = AudioSegment.from_file(tmp_midi.name, format="mid")
        return sound

# Button to trigger melody generation
if st.button('Generate Melody'):
    melody = generate_melody(num_notes, tempo)

    # Save the generated melody as a MIDI file
    midi_file = 'random_melody.mid'
    melody.write(midi_file)

    # Convert MIDI to WAV
    wav_audio = midi_to_wav(melody)
    wav_file = io.BytesIO()
    wav_audio.export(wav_file, format="wav")
    wav_file.seek(0)
    
    # Display success message and play audio
    st.success('Melody generated!')

    # Play the WAV file in the app
    st.audio(wav_file, format='audio/wav')

    # Download buttons for MIDI and WAV
    st.download_button('Download MIDI', data=open(midi_file, 'rb').read(), file_name='generated_melody.mid', mime='audio/midi')
    st.download_button('Download WAV', data=wav_file, file_name='generated_melody.wav', mime='audio/wav')
