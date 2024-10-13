import os
import pickle
from dotenv import load_dotenv

from pydantic import BaseModel
from openai import OpenAI

from context import context as CONTEXT

from process_slices import slices, ensure_length, ensure_end_on_period, ensure_start_at_beginning

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

SHORTEST = 50
LONGEST = 100

def get_prompt(words):
	output = '\n'.join([f'{i} {word}' for i, word in enumerate(words)])
	title = 'The Martian'

	prompt = f'Please look at the chapter below from "{title}" and split the text up into sections such that a new image is generated for each section and will collectively capture the main visual elements of the whole chapter. Make sure to end sections on the end of a sentence. Each section must be between {SHORTEST} and {LONGEST} words. Output a list of indices like [1, 5, 7, 14...], where the first section is words 1 (inclusive) to 5 (exclusive):'

	return prompt, output

class SliceText(BaseModel):
	slices: list[int]

def get_slices(words, api_key=api_key):
	client = OpenAI(api_key=api_key)

	prompt, output = get_prompt(words)

	completion = client.beta.chat.completions.parse(
		model='gpt-4o-mini',
		messages=[
			{'role': 'system', 'content': CONTEXT},
			{'role': 'user', 'content': prompt + '\n' + output}
		],
		response_format=SliceText
	)

	slices = ensure_start_at_beginning(
		ensure_end_on_period(
			words,
			ensure_length(completion.choices[0].message.parsed.slices)
		)
	)

	with open('slices.txt', 'w') as f:
		f.write(str(slices))

	return slices

def get_sections(words):
	slices = get_slices(words)
	return [' '.join(paragraph) for paragraph in [words[slices[i - 1]:slices[i]] for i in range(1, len(slices))]]
