import webbrowser

def open_matches_url(matches):
    for match in matches:
        webbrowser.open(match["url"])