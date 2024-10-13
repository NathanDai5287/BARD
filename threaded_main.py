from extract_pdf import extract_text_from_pdf
from get_sections import get_sections, get_slices
from get_narration import get_narration
from get_image import get_image
from get_music import get_music

from scipy.io.wavfile import write as write_wav
from pydub.utils import mediainfo
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

pdf = 'hobbit.pdf'
max_pages = 2
text = extract_text_from_pdf(pdf, max_pages)
words = text.replace('’', "'").replace('“', '"').replace('”', '"').split()

sections = get_sections(words)
def get_narration_duration(file_path):
	"""Get the duration of the narration in seconds."""
	audio_info = mediainfo(file_path)
	return float(audio_info['duration'])

def process_section(i, section):
	# Save section text
	with open(f'outputs/sections/section_{i}.txt', 'w') as f:
		f.write(section)

	# Generate narration first
	narration_path = f'outputs/narration/section_{i}.mp3'
	save_narration(section, i)

	# Get the duration of the narration
	narration_duration = get_narration_duration(narration_path)

	# Generate music with the same duration as the narration
	save_music(section, i, narration_duration)

	# Generate images concurrently
	with ThreadPoolExecutor() as executor:
		futures = []
		# Image generation task
		futures.append(executor.submit(save_image, section, i))

		# Wait for image generation to complete
		for future in as_completed(futures):
			future.result()

def save_narration(section, i):
	"""Generate and save narration."""
	path = f'outputs/narration/section_{i}.mp3'
	narration = get_narration(section)
	with open(path, 'wb') as f:
		f.write(narration)

def save_image(section, i):
	"""Generate and save an image."""
	path = f'outputs/images/section_{i}.png'
	image = get_image(section, model='dall-e-2', size='256x256')
	image.save(path)

def save_music(section, i, duration):
	"""Generate and save music based on narration duration."""
	path = f'outputs/music/section_{i}.mp3'
	music, sampling_rate = get_music(section, seconds=int(duration))
	write_wav(path, rate=sampling_rate, data=music[0, 0].cpu().numpy())

# Create a ThreadPoolExecutor to process sections concurrently
with ThreadPoolExecutor() as executor:
	futures = [executor.submit(process_section, i, section) for i, section in enumerate(sections)]

	# Wait for all sections to be processed
	for future in as_completed(futures):
		future.result()  # Raise exceptions if any occur in a thread
