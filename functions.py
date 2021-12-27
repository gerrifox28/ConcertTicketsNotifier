from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import webbrowser

def convert_url(url):
    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    driver.get(url)

    driver = scroll_to_bottom(driver)

    html = driver.page_source
    soup = BeautifulSoup(html)
    return soup, driver

def scroll_to_bottom(driver):
    last_list = driver.find_element(By.CSS_SELECTOR, "ul.RoyalTicketList__container")
    last_list_length = len(last_list.find_elements(By.TAG_NAME, "li"))

    while True:

            # Scroll down to the bottom.
            scrolling_element = driver.find_element(By.CSS_SELECTOR, "div.RoyalTicketList__container")
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrolling_element)
            
            # Wait to load the page.
            time.sleep(2)

            # Calculate new scroll height and compare with last scroll height.
            new_list = driver.find_element(By.CSS_SELECTOR, "ul.RoyalTicketList__container")
            new_list_length = len(new_list.find_elements(By.TAG_NAME, "li"))
            #print(new_list_length)

            if new_list_length == last_list_length:

                break

            last_list_length = new_list_length
    return driver

def get_ticket_list(soup):
    list_items = soup.findAll('li', class_= "RoyalTicketListPanel")
    tickets = []
    for li in list_items:
        ticket = {} # dict to represent ticket info
        className = li['class']
        ticket['className'] = className[1]
        
        # get section of ticket
        section = li.find('div', class_ = "SectionRowSeat__sectionTitle")
        ticket['section'] = section.text 
        
        # get row of ticket
        row = li.find('span', class_ = "SectionRowSeat__row")
        if row is not None: 
            row_text = row.text.replace(u'\xa0', u' ')
            ticket['row'] = row_text
        
        # get number of tickets available
        num_tix = li.find('div', class_ = "RoyalTicketListPanel__SecondaryInfo")
        if num_tix.find('span'): 
            num_tix.find('span').replace_with('')
        num_tix_text = num_tix.text.replace(u'\xa0', u' ') 
        ticket['num_tickets'] = num_tix_text
        
        # get price of ticket
        price = li.find('div', class_ = "AdvisoryPriceDisplay__content")
        ticket['price'] = price.text
        
        tickets.append(ticket)
    return tickets

def clean_tickets_list(tickets):
    for ticket in tickets:

        if 'row' in ticket.keys():
            row = ticket['row']
            ticket['row'] = row.replace('Row ', '')
        
        num_tickets = ticket['num_tickets']
        if '-' in num_tickets:
            num_tickets = num_tickets.replace(' tickets', '')
            start = num_tickets[0]
            end = num_tickets[-1]
            num_tickets = list(range(int(start), int(end)+1))
        elif 'tickets' in num_tickets:
            num_tickets = num_tickets.replace(' tickets', '')
            num_tickets = [int(num_tickets)]
        else:
            num_tickets = num_tickets.replace(' ticket', '')
            num_tickets = [int(num_tickets)]
        ticket['num_tickets'] = num_tickets
        
        price = ticket['price']
        price = price.replace('$', '')
        price = price.replace(',', '')
        price = int(price)
        ticket['price'] = price
    return tickets


def find_filtered_matches(tickets, filters, driver, all=True):
    matches = []
    urls = []
    for ticket in tickets: 
        match = 0
        added = False
        for key,val in filters.items():
            price_filter = False
            if key == 'row' and 'row' not in ticket.keys():
                continue
            act = ticket[key]
            if key == 'num_tickets':
                if val in act: 
                    price_filter = True
            if act == val or price_filter:
                if all:
                    match = match + 1
                elif not added:
                    element = driver.find_element(By.CLASS_NAME, ticket['className'])
                    driver.execute_script("arguments[0].scrollIntoView(true);", element);  
                    element.click()
                    url = driver.current_url
                    ticket['url'] = url
                    driver.execute_script("window.history.go(-1)")
                    urls.append(url)
                    matches.append(ticket)
                    added = True
        if all and match == len(filters): 
            element = driver.find_element(By.CLASS_NAME, ticket['className'])
            driver.execute_script("arguments[0].scrollIntoView(true);", element);  
            element.click()
            url = driver.current_url
            ticket['url'] = url
            driver.execute_script("window.history.go(-1)")
            urls.append(url)
            matches.append(ticket)
    return matches, urls

def open_matches_url(matches):
    urls = []
    for match in matches:
        url = match['url']
        webbrowser.open(url)
        urls.append(url)
    return urls