import webbrowser

def open_matches_url(matches):
    urls = []
    for match in matches:
        url = match['url']
        webbrowser.open(url)
        urls.append(url)
    return urls