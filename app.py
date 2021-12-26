from bs4 import BeautifulSoup
from flask import Flask, json, request
from selenium import webdriver
from clean_tickets_list import clean_tickets_list

from convert_url import convert_url
from find_filtered_matches import find_filtered_matches
from find_perfect_match import find_perfect_match
from get_ticket_list import get_ticket_list
from open_matches_url import open_matches_url


def create_app():
    app = Flask(__name__)
    return app

app = create_app()

@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'

@app.route('/search-stubhub')
def search_url():
    args = request.args.to_dict()
    event = args['event']
    location = args['location']
    date = args['date']
    filters = json.loads(json.dumps(request.form))
    all = bool(filters.pop('all'))
    filters['price'] = int(filters['price'])
    filters['num_tickets'] = int(filters['num_tickets'])

    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    driver.get(f'https://www.stubhub.com/find/s/?q={event}+{location}+{date}')
    html = driver.page_source
    soup = BeautifulSoup(html)

    event = soup.find('div', class_='EventRedirection')
    if event is None:
        driver.quit()
        return 'No Events Found'
    link = event.find('a', href=True)
    href = link['href']
    url = f'https://www.stubhub.com{href}'
    soup, driver = convert_url(url)

    tickets = get_ticket_list(soup)

    tickets = clean_tickets_list(tickets)

    if len(filters) > 0:
        matches = find_filtered_matches(tickets, filters, driver, all)
        url_list = open_matches_url(matches)
        url_list_to_return = ', '.join([str(elem) for elem in url_list])
        driver.quit()
        return url_list_to_return
    
    driver.quit()
    return 'Add filters to search tickets by'

