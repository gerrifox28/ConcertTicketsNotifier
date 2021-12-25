import time

def scroll_to_bottom(driver):
    last_list = driver.find_element_by_css_selector("ul.RoyalTicketList__container")
    last_list_length = len(last_list.find_elements_by_tag_name("li"))

    while True:

            # Scroll down to the bottom.
            scrolling_element = driver.find_element_by_css_selector("div.RoyalTicketList__container");
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrolling_element)
            
            # Wait to load the page.
            time.sleep(2)

            # Calculate new scroll height and compare with last scroll height.
            new_list = driver.find_element_by_css_selector("ul.RoyalTicketList__container");
            new_list_length = len(new_list.find_elements_by_tag_name("li"))
            #print(new_list_length)

            if new_list_length == last_list_length:

                break

            last_list_length = new_list_length
    return driver
