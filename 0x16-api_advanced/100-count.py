#!/usr/bin/python3
"""
Function that queries the Reddit API and prints
the top ten hot posts of a subreddit
"""
import re
import requests

def count_words(subreddit, word_list, after=None, counts=None):
    """
    Recursively queries the Reddit API, parses the title of all hot articles, and prints a sorted count of given keywords.

    Args:
    subreddit (str): The name of the subreddit to search.
    word_list (list): A list of keywords to count.
    after (str, optional): The ID of the post to start after. Defaults to None.
    counts (dict, optional): A dictionary to store the counts of each keyword. Defaults to None.

    Returns:
    None

    Raises:
    None
    """
    if counts is None:
        counts = {}
    if after is None:
        url = 'https://www.reddit.com/r/{}/hot.json'.format(subreddit)
    else:
        url = 'https://www.reddit.com/r/{}/hot.json?after={}'.format(subreddit, after)
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code == 200:
        data = response.json()
        posts = data['data']['children']
        for post in posts:
            title = post['data']['title'].lower()
            for word in word_list:
                if ' {} '.format(word.lower()) in ' {} '.format(title):
                    if word.lower() in counts:
                        counts[word.lower()] += 1
                    else:
                        counts[word.lower()] = 1
        after = data['data']['after']
        if after is not None:
            # Recursive call with a new "after" parameter
            count_words(subreddit, word_list, after=after, counts=counts)
        else:
            # Print the sorted counts when we've reached the end of the posts
            sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
            for word, count in sorted_counts:
                print('{}: {}'.format(word, count))
    else:
        print('Error: {}'.format(response.status_code))
