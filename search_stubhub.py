import sys

from clean_tickets_list import clean_tickets_list
from convert_url import convert_url
from find_perfect_match import find_perfect_match
from get_ticket_list import get_ticket_list

def search_stubhub():

    url='https://www.stubhub.com/olivia-rodrigo-new-york-tickets-4-26-2022/event/105133478/'
    #url='https://www.stubhub.com/billie-eilish-boston-tickets-2-20-2022/event/104853773/'

    #print(sys.argv)
    #url = sys.argv[1]
    soup, driver = convert_url(url)

    tickets = get_ticket_list(soup)

    tickets = clean_tickets_list(tickets)

    return find_perfect_match('3rd Mezzanine 4', 'D', 1, 700, driver, tickets)

search_stubhub()
