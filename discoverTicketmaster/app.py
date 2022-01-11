import time
from bs4 import BeautifulSoup
from discoverTicketmaster.functions import get_events, get_website, scroll_to_all_events, send_email

def discover_ticketmaster():

    url='https://www.ticketmaster.com/discover/concerts'
    driver = get_website(url)

    driver = scroll_to_all_events(driver)
    html = driver.page_source
    soup = BeautifulSoup(html)

    events = get_events(soup)

    while True: 
        time.sleep(86400) # wait 24 hours
        
        url='https://www.ticketmaster.com/discover/concerts'
        driver = get_website(url)
        
        driver = scroll_to_all_events(driver)
        html = driver.page_source
        soup = BeautifulSoup(html)
        
        new_events_list = get_events(soup)
        
        new_events = []
        
        for new_event in new_events_list:
            for event in events:
                if new_event['url'] == event['url'] and new_event['title'] == event['title'] and new_event['subtitle'] == event['subtitle']:
                    continue
                else:
                    new_events.add(new_event)

        send_email(new_events)
        
        events = new_events_list 