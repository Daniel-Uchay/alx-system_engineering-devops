#!/usr/bin/python3
"""
    Reddit API
"""
import requests


def recurse(subreddit, hot_list=[], after=None):
    """ gets the number of subscribers """
    if after is not None:
        url = 'https://api.reddit.com/r/' +\
              '{}/hot.json?after={}'.format(subreddit, after)
    else:
        url = 'https://api.reddit.com/r/{}/hot.json'.format(subreddit)
    header = {'user-agent': 'ianscustomthing'}

    r = requests.get(url,
                     headers=header,
                     allow_redirects=False)
    if r.status_code != 200:
        return None
    try:
        rj = r.json()
    except:
        return None
    if rj.get('message') == 'Not Found':
        return
    chldrn = rj.get('data').get('children')
    hot_list += [chld.get('data').get('title') for chld in chldrn]
    after = rj.get('data').get('after')
    if after is not None:
        return recurse(subreddit, hot_list, after)
    else:
        return hot_list


def print_words(word_list, hot_list):
    """ prints the words all pretty like """
    cnts = {}
    for word in word_list:
        c = 0
        for title in hot_list:
            t = title.lower().split()
            if word.lower().strip() in t:
                c += t.count(word.lower().strip())
            '''
            for w in title.split():
                if word.strip().lower() in word.strip().lower():
                    print("{}, {}".format(word.
                                          strip().lower(), w.strip().lower()))
                    c = c + 1
            '''
        if word.lower() in cnts:
            cnts[word.lower()] += c
        else:
            cnts.update({word.lower(): c})
    '''
    print(hot_list)
    cnts.update({'thing': 17})'''
    for k, v in sorted(cnts.items(), key=lambda x: (-x[1], x[0])):
        if cnts.get(k) != 0:
            print("{}: {}".format(k, v))


def count_words(subreddit, word_list):
    """ counts dem keywords """
    hot_list = recurse(subreddit)
    if hot_list is None:
        return
    f = 0
    if f == 1:
        count_words(subreddit, word_list)
    print_words(word_list, hot_list)
