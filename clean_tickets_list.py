   # clean list of tickets to remove 'Row', 'ticket' and $ from price and create list of number of tickets available

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