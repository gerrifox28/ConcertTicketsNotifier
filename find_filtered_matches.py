def find_filtered_matches(tickets, filters, driver, all=True):
    matches = []
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
                    element = driver.find_element_by_class_name(ticket['className'])
                    driver.execute_script("arguments[0].scrollIntoView(true);", element);  
                    element.click()
                    url = driver.current_url
                    ticket['url'] = url
                    driver.execute_script("window.history.go(-1)")
                    matches.append(ticket)
                    added = True
        if all and match == len(filters): 
            element = driver.find_element_by_class_name(ticket['className'])
            driver.execute_script("arguments[0].scrollIntoView(true);", element);  
            element.click()
            url = driver.current_url
            ticket['url'] = url
            driver.execute_script("window.history.go(-1)")
            matches.append(ticket)
    return matches