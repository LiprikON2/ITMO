import pymorphy2
import gensim
import pyLDAvis.gensim
import nltk
import requests
from string import ascii_lowercase
import re
import argparse

import pandas as pd
import textwrap

from pandas.io.json import json_normalize
from string import Template
from tqdm import tqdm

from api import get, get_ids
from bcolors import bcolors
import config


def get_wall(
    owner_id: int = None,
    domain: str = '',
    offset: int = 0,
    count: int = 10,
    filter: str = 'owner',
    extended: int = 0,
    fields: str = '',
    v: str = '5.103'
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.

    @see: https://vk.com/dev/wall.get 

    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param v: Версия API.
    """
    # Convert screen name to id
    if owner_id != '':
        owner_id = get_ids([owner_id])[0]
    
    code = f"""
        return API.wall.get({{
        "owner_id": '{owner_id}',
        "domain": '{domain}',
        "offset": '{offset}',
        "count": '{count}',
        "filter": '{filter}',
        "extended": '{extended}',
        "fields": '{fields}',
        "v": '{v}'
    }});
    """

    response = requests.post(
        url="https://api.vk.com/method/execute",
            data={
                "code": code,
                "access_token": config.VK_CONFIG['access_token'],
                "v": "5.103"
            }
    )
    
    if 'error' in response.json():

        error_msg = response.json()['error']['error_msg']
        print(response.json())
        print(f'{bcolors.FAIL}{error_msg}{bcolors.ENDC}')
        raise SystemExit(0)

    return pd.DataFrame(response.json()['response']['items'])


def build_model(wall: pd.DataFrame, num_topics: int = 4) -> None:
    # Generate string of russian alphabet including 'ё'
    a = ord('а')
    rus_lowercase = ''.join([chr(i) for i in range(
        a, a+6)] + [chr(a+33)] + [chr(i) for i in range(a+6, a+32)])

    # Add letters of rus and eng alphabet to set
    letters = set()
    for c in ascii_lowercase:
        letters.add(c)
    for c in rus_lowercase:
        letters.add(c)

    stopwords = nltk.corpus.stopwords.words("russian")
    morph = pymorphy2.MorphAnalyzer()

    posts = []
    for post in wall['text']:

        # Remove punctuatiion from post
        text = re.sub(r'[^\w\s]', '', post)

        nouns = []
        for word in text.split():
            word = morph.parse(word)[0]

            # Check if word is noun
            if 'NOUN' in word.tag:
                if not word.normal_form in stopwords:
                    nouns.append(word.normal_form)
        posts.append(nouns)

    # Create a corpus from a list of texts
    dictionary = gensim.corpora.Dictionary(posts)
    # Convert texts into the bag-of-words (BoW) format
    # list of (token_id, token_count) tuples.
    corpus = [dictionary.doc2bow(post) for post in posts]

        
    lda_model = gensim.models.ldamodel.LdaModel(
        corpus=corpus,
        num_topics=3,
        id2word=dictionary,
        update_every=1,
        chunksize=100,
        passes=5,
        alpha='auto',
        random_state=100,
        per_word_topics=False
    )

    model = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary)
    pyLDAvis.show(model)

    # lda_model ref: https://radimrehurek.com/gensim/models/ldamodel.html


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--id", type=str, help="VK user id or screen name")
    
    # args = parser.parse_args()
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--owner_id',
        nargs='+',
        type=str,
        help="""
            ID of the user or community that owns the wall. 
            By default, current user ID. 
            Use a negative value to designate a community ID
        """
    )
    parser.add_argument(
        '--domain',
        nargs='+',
        type=str,
        help="User or community short address"
    )
    args = parser.parse_args()

    # Check if user provided VK group owner id
    if args.owner_id:

        owner_ids = get_ids(args.owner_id)
        for owner_id in owner_ids:

            # Check if wall is already created
            if not 'wall' in locals():
                wall = get_wall(owner_id=owner_id)
            else:
                wall.append(get_wall(owner_id=owner_id), ignore_index=True)
    
    # Check if user provided VK groups domains      
    if args.domain:

        domains = args.domain
        for domain in domains:

            # Check if wall is already created
            if not 'wall' in locals():
                wall = get_wall(domain=domain)
            else:
                wall = wall.append(get_wall(domain=domain), ignore_index=True)

    # Check if user provided CLI arguments
    if not 'wall' in locals():
        print(f'{bcolors.WARNING}Looks like you have not provided VK group id. Type `{bcolors.ENDC}python model.py -h{bcolors.WARNING}` for help.{bcolors.ENDC}')
        raise SystemExit(0)

    if args.num_topics:
        build_model(wall, num_topics=args.num_topics)
    else:
        build_model(wall)
