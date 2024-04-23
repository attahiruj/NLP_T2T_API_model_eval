import requests
import json
import argparse

api_endpoint = 'http://10.10.45.1:1405/multilang-translate'


text_data = ['Citizens are demanding accountability from their leaders and an end to corruption.',
				'I\'m thinking of simplifying my life.']
def batch_translate(text_data: list, from_lang: str='english', to_lang: str='pigin') -> list:
	"""
	Translates a list of text strings from one language to another using the multilang-translate API.

	Args:
		text_data (list): a list of text strings to be translated
		from_lang (str, optional): the language of the input text, defaults to 'english'
		to_lang (str, optional): the language to which the text should be translated, defaults to 'pigin'

	Returns:
		list: a list of translated text strings

	Raises:
		ValueError: if the input language or output language is not supported
	"""
	translations = []
	languages = ['english', 'pigin', 'hausa', 'igbo', 'yoruba']
	headers = {
		'content-type' : 'application/json',
	}
	assert from_lang in languages and to_lang in languages, \
		f'lang must be english, pigin, hausa, igbo or yoruba, got {from_lang, to_lang}'

	assert type(text_data) == list, f'text_data must be a list'

	for i in range(len(text_data)):
		line = text_data[i]
		payload = dict(text = line, from_ = from_lang, to_ = to_lang)
		response = requests.post(api_endpoint, json=payload, headers=headers)
		if response.status_code == 200:
			try:
				response = json.loads(response.text)
				translations.append(response['translated'])
			except Exception as e:
				print(f'An exception occured {e}')
		else:
			print(f'Cant reach API, error code-> {response.status_code}')
	print(f'Translation Completed')
	return translations

translated_text = batch_translate(text_data, 'english', 'pigin')
print(translated_text)