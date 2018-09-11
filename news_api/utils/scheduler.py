import schedule
import time
from ..models.feed import Feed
import json
from watson_developer_cloud import ToneAnalyzerV3
from goose3 import Goose
import goose3
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def job():
    # an Engine, which the Session will use for connection
    # resources
    my_engine = create_engine('postgres://localhost:5432/news_api')

    # create a configured "Session" class
    Session = sessionmaker(bind=my_engine)

    # create a Session
    session = Session()

    # work with sess
    session.query(Feed).delete()
    session.commit()

    response = requests.get('https://newsapi.org/v2/top-headlines?country=us&apiKey=62d8cce09c5f447ea8d980720d63b3ef')

    articles_list = response.json()['articles']

    list_articles = []

    for el in articles_list:
        single_art = {'title': el['title'], 'url': el['url']}
        list_articles.append(single_art)

    analyzed_articles = []

    for el in list_articles:
        url = el['url']
        g = Goose()
        try:
            article = g.extract(url)
        except goose3.network.NetworkError:
            continue

        tone_analyzer = ToneAnalyzerV3(
            version='2017-09-21',
            username='2ae7d431-a7f3-4a6f-861e-33271c09fa08',
            password='yuEKUQzEVFLm')

        tone_analysis = tone_analyzer.tone(
            {'text': article.cleaned_text},
            'application/json')

        if len(tone_analysis['document_tone']['tones']):
            dom_tone = tone_analysis['document_tone']['tones'][-1]['tone_name']
            article = {'title': el['title'], 'url': el['url'], 'dom_tone': dom_tone}
            analyzed_articles.append(article)

        print(article)
        try:
            article_to_insert = Feed(title=article['title'], url=article['url'], dom_tone=article['dom_tone'])
            session.add(article_to_insert)

        except TypeError:
            continue
    session.commit()

    print(analyzed_articles)











# schedule.every(1).minute.do(job)


# while True:
#     schedule.run_pending()
#     time.sleep(1)
