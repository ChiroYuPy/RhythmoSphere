import numpy as np
import librosa

y, sr = librosa.load("songs/astronomia.mp3")

hop_length = 12

y_harmonic, y_persecutive = librosa.effects.hpss(y)

tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

print('Estimated tempo: {:.2f} beats per minute'.format(tempo))

beat_times = librosa.frames_to_time(beat_frames, sr=sr)
