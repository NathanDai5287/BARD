from moviepy.editor import *
from pydub import AudioSegment
from scipy.io import wavfile

narration = AudioSegment.from_wav('outputs/narration/section_0.wav')
music = AudioSegment.from_wav('outputs/music/section_0.wav')

combined = narration.overlay(music, format='wav')
combined.export('outputs/combined/section_0.wav', format='wav')

image = ImageClip('outputs/images/section_0.png')
audio = AudioFileClip('outputs/combined/section_0.wav')

video = CompositeVideoClip([image.set_duration(audio.duration).set_audio(audio)])

video.write_videofile('outputs/videos/section_0.mp4', codec='libx264', audio_codec='aac', fps=24)
