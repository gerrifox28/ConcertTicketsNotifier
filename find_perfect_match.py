from service.find_filtered_matches import find_filtered_matches


def find_perfect_match(section, row, num_tickets, price, driver, tickets):
    filters = {'section':section, 'row':row, 'num_tickets':num_tickets, 'price': price}
    result = find_filtered_matches(tickets, filters, driver, True)
    if len(result) > 0:
        return [result[0]]
    return len(result) > 0