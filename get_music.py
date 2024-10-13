from transformers import MusicgenForConditionalGeneration, AutoProcessor
import os
import torch
import scipy
import numpy as np

from dotenv import load_dotenv

from context import context as CONTEXT

from openai import OpenAI

import warnings
warnings.filterwarnings('ignore')

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

def get_music_prompt(section):
	prompt = f'Given a section of the text from the book, generate an effective SINGLE-LINE prompt that would be used as input to the MusicGen model. This should generate music that\'s good to play in the background as the images display. \n\n' + section

	client = OpenAI(api_key=api_key)
	completion = client.chat.completions.create(
		model='gpt-4o-mini',
		messages=[
			{'role': 'system', 'content': CONTEXT},
			{
				'role': 'user',
				'content': prompt
			},
		],
	)

	return completion.choices[0].message.content

def get_music(section, seconds):
	prompt = get_music_prompt(section)

	model = MusicgenForConditionalGeneration.from_pretrained('facebook/musicgen-small')
	# device = 'cuda' if torch.cuda.is_available() else 'cpu'
	device = 'cpu'
	model.to(device)

	processor = AutoProcessor.from_pretrained('facebook/musicgen-small')

	inputs = processor(
		text=[prompt],
		padding=True,
		return_tensors='pt',
	)

	audio_values = model.generate(**inputs.to(device), do_sample=True, guidance_scale=3, max_new_tokens=(256 // 5) * seconds)
	sampling_rate = model.config.audio_encoder.sampling_rate

	return audio_values, sampling_rate
