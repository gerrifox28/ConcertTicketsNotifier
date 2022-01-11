from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
import smtplib

def get_website(url):
    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    driver.get(url)
    return driver

def scroll_to_all_events(driver):
    
    t_end = time.time() + 60 * 10 #load results for 10 mins

    while time.time() < t_end:
        
        try:
            element = driver.find_element(By.CSS_SELECTOR,"button.noFocus")
        except NoSuchElementException:
            return driver
            
        driver.execute_script("arguments[0].scrollIntoView(true);", element);  
        element.click()
        
    return driver

def get_events(soup):
    events = []
    all_events = soup.find_all('div', class_="event-listing__item")
    
    for e in all_events:
        event = {}
        
        url = e.find('a', class_="event-list__header-wrapper", href=True)['href']
        event['url'] = url
        
        title = e.find('div', class_="event-title__title")
        event['title'] = title
        
        subtitle = e.find('div', class_="event-title__sub-title")
        event['subtitle'] = subtitle
        
        events.add(event)
    return events

def send_email(response):

    gmail_user = '28foxg@gmail.com'
    gmail_password = GMAIL_PASSWORD


    sent_from = gmail_user
    to = ['28foxg@gmail.com']
    subject = 'Daily Ticketmaster Just Added Concerts!'
    body = f'Here are the urls and ticket information for newly announced concerts: {response} Happy Concert Going!'
    print(body)

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
    except:
        print('Something went wrong...')
