# %%
from extract_pdf import extract_text_from_pdf
from get_sections import get_sections, get_slices
from get_narration import get_narration
from get_image import get_image
from get_music import get_music

from scipy.io import wavfile
from math import ceil
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor, as_completed

# %%
pdf = 'hobbit.pdf'
max_pages = 3
text = extract_text_from_pdf(pdf, max_pages)
words = text.replace('’', "'").replace('“', '"').replace('”', '"').split()

# %%
sections = get_sections(words)

# %%
for i, section in enumerate(sections):
	# sections
	with open(f'outputs/sections/section_{i}.txt', 'w') as f:
		f.write(section)

	# narration
	path = f'outputs/narration/section_{i}.wav'
	narration = get_narration(section)
	with open(path, 'wb') as f:
		f.write(narration)

	# images
	path = f'outputs/images/section_{i}.png'
	image = get_image(section, model='dall-e-3', size='1024x1024')
	image.save(path)

	# music
	path = f'outputs/music/section_{i}.wav'
	duration = len(AudioSegment.from_wav(f'outputs/narration/section_{i}.wav')) / 1000
	music, sampling_rate = get_music(section, seconds=ceil(duration))
	wavfile.write(path, rate=sampling_rate, data=music[0, 0].cpu().numpy())
