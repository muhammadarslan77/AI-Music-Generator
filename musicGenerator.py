import streamlit as st
import pretty_midi
import numpy as np

# Set up the Streamlit app interface
st.title('AI Music Generator 🎵')
st.write("Generate random melodies using AI and download them as MIDI files!")

# Sidebar options for user input
st.sidebar.header("Melody Settings")
num_notes = st.sidebar.slider('Number of Notes', 5, 50, 10)
tempo = st.sidebar.slider('Tempo (BPM)', 60, 180, 120)

# Function to generate a random melody
def generate_melody(num_notes, tempo):
    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)  # Acoustic Grand Piano

    # Generate random notes
    for i in range(num_notes):
        note_number = np.random.randint(60, 72)  # Random note between C4 and B4
        start_time = i * (60.0 / tempo)  # Space notes based on tempo (seconds per note)
        end_time = start_time + (60.0 / tempo) * 0.75  # Duration of each note
        note = pretty_midi.Note(velocity=100, pitch=note_number, start=start_time, end=end_time)
        instrument.notes.append(note)

    midi.instruments.append(instrument)
    return midi

# Button to trigger melody generation
if st.button('Generate Melody'):
    melody = generate_melody(num_notes, tempo)

    # Save the generated melody as a MIDI file
    midi_file = 'random_melody.mid'
    melody.write(midi_file)

    # Success message and audio player
    st.success('Melody generated!')
    st.audio(midi_file, format='audio/midi')
    st.download_button('Download MIDI', data=open(midi_file, 'rb').read(), file_name='generated_melody.mid', mime='audio/midi')
