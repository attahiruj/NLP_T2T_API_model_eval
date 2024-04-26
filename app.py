import requests
import json
# https://pytorch.org/text/stable/data_metrics.html
from torchtext.data.metrics import bleu_score


api_endpoint = 'http://10.10.45.1:1405/multilang-translate'


def batch_translate(text_data: list, from_lang: str = 'english', to_lang: str = 'pigin') -> list:
    """
    Translates a list of text strings from one language to another using th
    multilang-translate API.

    Args:
        text_data (list): a list of text strings to be translated
        from_lang (str, optional): the language of the input text,
        defaults to 'english'
        to_lang (str, optional): the language to which the text should be
        translated, defaults to 'pigin'

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

    assert type(text_data) is list, 'text_data must be a list'

    for i in range(len(text_data)):
        line = text_data[i]
        payload = dict(text=line, from_=from_lang, to_=to_lang)
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


def split_to_words(sentences: list) -> list:
    """
    Splits a list of sentences into a list of words.

    Args:
        sentences (list): a list of sentences

    Returns:
        list: a list of words
    """
    splitted = []
    for line in sentences:
        line = line.replace(",", "")
        line = line.replace(".", "")
        line = line.split(" ")
        splitted.append(line)
    return splitted


# testing
hausa_text = [
    "su ke ciyar da shi su ke shayar da shi har sai yaro ya zama mutum sosai",
    "mutanensa suna binsa, har ya iso kusa da sarki",
    "Asalin hausawa an ce, wadansu mutane ne, wa da kane, suka zo daga kasal larabawa da matan su biu. Su ka zamna wani jeji kusa da kasal barno, sunansa gabi, su ka yi bukoki, su ka yi shimge, su na halbin namun jeji, don su ma-halba ne. Yau, mutane kuwa su na zua daga barno, su na sayasayar nama, kuma su na zua daga wasu gurare, su na sayasaya, har gun nan ya zama gari-gari. Su na nan, har matar kanen nan ta haifi ya, su ka sa ma ta suna fetsima, amma su na yi ma ta lakabi dauratu da larabci, shi ne kewaya, kaman sun ce, su na yin kewayal duniya, har su ka zo gabi su ka haife ta.",
    "idan yaran suka shekara bakwai sai a sa su a makaranta",
    "kowa ya sani cewa duk duniyan nan babu sana'ar da ta fi noma wuya",
    "ina yin kuka saboda gajiya"
]
english_text = [
    "they give him food and drink until the boy is a grown man",
    "his people followed him, as long as he had not approached the emperor",
    "It is said that the origin of the Hausa was thus. Some people, an elder brother and a younger brother, came from Arab countries with their wives. They settled in a wild place not far from the country of Bornu. This place was called Gabi. Here they built huts and put up a fence, They hunted wild animals, because they were hunters. People came from Bornu and from other places and bought meat from them. In the end, the place was turned into a town. They lived there until the wife of the younger brother bore a girl. To this girl they gave the name Fatsima and as well as this, the nickname Daurata which means ‘circle’ in Arabic. They said that they had wandered about in the world until they came to Gabi and this girl was born.",
    "when boys have completed their seventh year, they are sent to school",
    "everyone knows that there is no heavier work on earth than agriculture",
    "I wept for tiredness""they give him food and drink until the boy is a grown man"
]


hausa_text_model = batch_translate(english_text, 'english', 'hausa')
candidate_corpus = split_to_words(hausa_text_model)
references_corpus = split_to_words(hausa_text)

score = bleu_score(candidate_corpus, references_corpus, 1, weights=[1.0])
print('score: ', score)