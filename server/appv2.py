from selenium import webdriver
from flask import request, Response

import ast

def get_event_url_from_search():
    args = request.args.to_dict()
    event = args['event']
    location = args['location']
    date = args['date']
    if 'result_num' in args.keys():
        result_num = int(args['result_num'])
    else:
        result_num = 0

    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    driver.get(f'https://www.stubhub.com/find/s/?q={event}+{location}+{date}')
    html = driver.page_source
    soup = BeautifulSoup(html)

    events = soup.findAll('div', class_='EventRedirection')
    if result_num >= len(events):
        return "No More Events Found"
    if events[result_num] is None:
        return "No Events Found"
    
    event = events[result_num]
    link = event.find('a', href=True)
    href = link['href']
    url = f'https://www.stubhub.com{href}'
    driver.close()
    return url

def get_tickets_matching_filters():
    args = request.args.to_dict()
    url = args.pop('url')

    soup, driver = convert_url(url)
    tickets = get_ticket_list(soup)
    tickets = clean_tickets_list(tickets)

    if len(args) > 0:
        open_url = False
        all = ast.literal_eval(args.pop('all'))
        if 'open_url' in args.keys():
            open_url = ast.literal_eval(args.pop('open_url'))
        if 'num_tickets' in args.keys():
            args['num_tickets'] = int(args['num_tickets'])
        if 'price' in args.keys():
            args['price'] = int(args['price'])
        # filters = {}
        # if 'section' in args.keys():
        #     section = args['section']
        #     filters['section'] = section
        # if 'row' in args.keys():
        #     row = args['row']
        #     filters['row'] = row
        # if 'num_tickets' in args.keys():
        #     num_tickets = int(args['num_tickets'])
        #     filters['num_tickets'] = num_tickets
        # if 'price' in args.keys():
        #     price = int(args['price'])
        #     filters['price'] = price
        # if 'open_url' in args.keys():
        #     open_url = ast.literal_eval(args.pop('open_url'))
        matches, url_list = find_filtered_matches(tickets, args, driver, all)
        if open_url:
            open_matches_url(matches)
        url_list_to_return = ', '.join([str(elem) for elem in url_list])
        driver.close()
        return url_list_to_return
    
    driver.close()
    return 'Add filters to search tickets by'
