import requests

def count_words(subreddit, word_list, after=None, counts=None):
    if counts is None:
        counts = {}
    if after is None:
        url = f'https://www.reddit.com/r/{subreddit}/hot.json'
    else:
        url = f'https://www.reddit.com/r/{subreddit}/hot.json?after={after}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code == 200:
        data = response.json()
        posts = data['data']['children']
        for post in posts:
            title = post['data']['title'].lower()
            for word in word_list:
                if f' {word.lower()} ' in f' {title} ':
                    if word.lower() in counts:
                        counts[word.lower()] += 1
                    else:
                        counts[word.lower()] = 1
        after = data['data']['after']
        if after is not None:
            count_words(subreddit, word_list, after=after, counts=counts)
        else:
            sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
            for word, count in sorted_counts:
                print(f'{word}: {count}')
    else:
        print(f'Error: {response.status_code}')
