import streamlit as st
from magenta.models.music_vae import TrainedModel
from magenta.models.music_vae import configs
from magenta.protobuf import music_pb2
import pretty_midi
import numpy as np
import tensorflow as tf

# Set up Streamlit page
st.title('AI Music Generator 🎵')
st.write('Generate melodies using a pre-trained MusicVAE model.')

# Sidebar for input parameters
st.sidebar.header("Input Options")
temperature = st.sidebar.slider('Temperature (Diversity of the music)', 0.1, 2.0, 1.0)
num_bars = st.sidebar.slider('Number of Bars', 2, 16, 4)
num_steps_per_bar = 16

# Initialize the MusicVAE model
config = configs.CONFIG_MAP['cat-mel_2bar_small']
model = TrainedModel(config, batch_size=4, checkpoint_dir_or_path='https://storage.googleapis.com/magentadata/models/music_vae/cat-mel_2bar_small.tar')

# Button to trigger music generation
generate = st.button('Generate Music')

if generate:
    with st.spinner('Generating melody...'):
        # Sample latent vectors and generate music sequences
        z = np.random.randn(1, model.z_size)
        music_sequence = model.sample(n=1, z=z, length=num_bars * num_steps_per_bar, temperature=temperature)

        # Convert to PrettyMIDI object
        midi = pretty_midi.PrettyMIDI()
        instrument = pretty_midi.Instrument(program=0)  # Acoustic Grand Piano
        for note in music_sequence.notes:
            midi_note = pretty_midi.Note(velocity=100, pitch=note.pitch, start=note.start_time, end=note.end_time)
            instrument.notes.append(midi_note)
        midi.instruments.append(instrument)

        # Save to a MIDI file
        midi_file_name = 'generated_music.mid'
        midi.write(midi_file_name)

        # Display download button
        st.success("Melody generated successfully!")
        st.audio(midi_file_name, format='audio/midi')
        st.download_button('Download MIDI file', data=open(midi_file_name, 'rb').read(), file_name='generated_music.mid', mime='audio/midi')
