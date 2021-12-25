from bs4 import BeautifulSoup
from selenium import webdriver

from scroll_to_bottom import scroll_to_bottom

def convert_url(url):
    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    driver.get(url)

    driver = scroll_to_bottom(driver)

    html = driver.page_source
    soup = BeautifulSoup(html)
    return soup, driver