from bs4 import BeautifulSoup
from flask import Flask, request
from selenium import webdriver
from clean_tickets_list import clean_tickets_list

from convert_url import convert_url
from find_perfect_match import find_perfect_match
from get_ticket_list import get_ticket_list
from open_matches_url import open_matches_url

#from search_stubhub import search_stubhub

def create_app():
    app = Flask(__name__)
    print('print test')
    return app

app = create_app()

@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'

@app.route('/search-stubhub/')
def search():
    #url='https://www.stubhub.com/olivia-rodrigo-new-york-tickets-4-26-2022/event/105133478/'
    
    args = request.args.to_dict()
    print(args)
    return 'done'
    # soup, driver = convert_url(url)

    # tickets = get_ticket_list(soup)

    # tickets = clean_tickets_list(tickets)

    # return find_perfect_match('3rd Mezzanine 4', 'D', 1, 700, driver, tickets)[0]
   # return result[0]

@app.route('/search')
def search_url():
    args = request.args.to_dict()
    event = args['event']
    location = args['location']
    date = args['date']

    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    driver.get(f'https://www.stubhub.com/find/s/?q={event}+{location}+{date}')
    html = driver.page_source
    soup = BeautifulSoup(html)

    event = soup.find('div', class_='EventRedirection')
    if event is None:
        return 'No Events Found'
    link = event.find('a', href=True)
    href = link['href']
    url = f'https://www.stubhub.com{href}'
    soup, driver = convert_url(url)

    tickets = get_ticket_list(soup)

    tickets = clean_tickets_list(tickets)

    matches = find_perfect_match('3rd Mezzanine 4', 'D', 1, 700, driver, tickets)

    driver.quit()
    
    url_list = open_matches_url(matches)

    url_list_to_return = ', '.join([str(elem) for elem in url_list])

    return url_list_to_return
