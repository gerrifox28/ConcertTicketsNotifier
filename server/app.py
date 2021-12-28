from flask import Flask, json, request
from bs4 import BeautifulSoup
from selenium import webdriver
import ast
from functions import convert_url, get_ticket_list, clean_tickets_list, find_filtered_matches, open_matches_url

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
    driver.close()
    soup, driver = convert_url(url)
    tickets = get_ticket_list(soup)
    tickets = clean_tickets_list(tickets)

    if len(filters) > 0:
        open_url = False
        all = ast.literal_eval(filters.pop('all'))
        if 'price' in filters.keys():
            filters['price'] = int(filters['price'])
        if 'num_tickets' in filters.keys():
            filters['num_tickets'] = int(filters['num_tickets'])
        if 'open_url' in filters.keys():
            open_url = ast.literal_eval(filters.pop('open_url'))
        matches, url_list = find_filtered_matches(tickets, filters, driver, all)
        if open_url:
            open_matches_url(matches)
        url_list_to_return = ', '.join([str(elem) for elem in url_list])
        driver.close()
        return url_list_to_return
    
    driver.close()
    return 'Add filters to search tickets by'

