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
