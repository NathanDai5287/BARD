import os
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

def get_narration(prompt):
	client = OpenAI(api_key=api_key)
	response = client.audio.speech.create(
		model='tts-1',
		voice='onyx',
		input=prompt,
		response_format='wav',
	)

	return response.content
