import os
import pickle
from dotenv import load_dotenv

from openai import OpenAI
from youtubesearchpython import VideosSearch
import yt_dlp

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

def get_recommendation(section, api_key=api_key):
	client = OpenAI(api_key=api_key)

	context = f'We are making an app where users can input the text of a book and get visual depictions, real-time narration, and live music throughout each chapter of the book to give a new visual experience to readers.'
	prompt = f'Please generate a music recommendation for the following text. Make sure the song has very little to no words. It does not need to be related to the book in any way (such as a soundtrack from the movie adaptaion). It should just match the mood of the text. Do not provide any context, explanation, or justification for your selection. The only thing in your response should be the name of the song:\n\n{section}'

	completion = client.chat.completions.create(
		model='gpt-4o-mini',
		messages=[
			{'role': 'system', 'content': context},
			{'role': 'user', 'content': prompt}
		]
	)

	return completion.choices[0].message.content

def get_youtube_video(song) -> str:
	search = VideosSearch(song, limit=1)
	video = search.result()['result'][0]

	return video['link']

def download_video(url, output_path):
	ydl_opts = {
		'format': 'bestaudio/best',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
		'outtmpl': output_path
	}

	with yt_dlp.YoutubeDL(ydl_opts) as ydl:
		ydl.download([url])

with open('outputs/sections.pkl', 'rb') as f:
	sections = pickle.load(f)

# a = get_recommendation(sections[0])
# "Arrival of the Birds" by The Cinematic Orchestra
song = '"Arrival of the Birds" by The Cinematic Orchestra'

download_video(get_youtube_video(song), 'outputs/song')
