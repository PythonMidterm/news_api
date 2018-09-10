# This is where the timed code execution goes
import schedule
import time
import json
from watson_developer_cloud import ToneAnalyzerV3
from goose3 import Goose
import requests


def job():
    response = requests.get('https://newsapi.org/v2/top-headlines?country=us&apiKey=62d8cce09c5f447ea8d980720d63b3ef')

    articles_list = response.json()['articles']

    list_articles = []

    for el in articles_list:
        single_art = {'title': el['title'], 'url': el['url']}
        list_articles.append(single_art)

    analyzed_articles = {}

    for el in list_articles:
        url = el['url']
        g = Goose()
        article = g.extract(url)

        tone_analyzer = ToneAnalyzerV3(
            version='2017-09-21',
            username='2ae7d431-a7f3-4a6f-861e-33271c09fa08',
            password='yuEKUQzEVFLm')

        tone_analysis = tone_analyzer.tone(
            {'text': article.cleaned_text},
            'application/json')
        dom_tone = json.dumps(tone_analysis['document_tone']['tones'][-1]['tone_name'])

        try:
            analyzed_articles[dom_tone].append({'title': el['title'], 'url': el['url']})
        except KeyError:
            analyzed_articles[dom_tone] = [{'title': el['title'], 'url': el['url']}]

        print(dom_tone)

    print(analyzed_articles)


# schedule.every(1).hour.do(job)


# while True:
#     schedule.run_pending()
#     time.sleep(1)


