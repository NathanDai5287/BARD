import os
from dotenv import load_dotenv

from PIL import Image
from io import BytesIO
import requests

from context import context as CONTEXT

from openai import OpenAI

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

def get_image_prompt(section):
	prompt = 'Given this section of the text from the book, generate an effective prompt that would be used to generate an image that best capture the visual elements of that section. \n\n' + section

	client = OpenAI(api_key=api_key)
	completion = client.chat.completions.create(
		model='gpt-4o-mini',
		messages=[
			{'role': 'system', 'content': CONTEXT},
			{
				'role': 'user',
				'content': prompt,
			},
		],
	)

	return completion.choices[0].message.content

def get_image(section, model='dall-e-3', size='1024x1024'):
	prompt = get_image_prompt(section)

	client = OpenAI(api_key=api_key)
	response = client.images.generate(
		model=model,
		prompt=prompt,
		size=size,
		quality='standard',
		n=1,
	)

	url = response.data[0].url
	image = Image.open(BytesIO(requests.get(url).content))

	return image

# get_image('In a hole in the ground there lived a hobbit.', model='dall-e-2', size='256x256')
