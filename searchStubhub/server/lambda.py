from bs4 import BeautifulSoup
from selenium import webdriver

def lambda_handler(event, context):
    args = event['queryStringParameters']
    if len(args) == 0:
        return {
            'statusCode': 400,
            'body': { 'message': 'No search params entered' }
        }
    query_string = 'q='
    if 'event' in args.keys():
        event = args['event']
        query_string = query_string + event
    if 'location' in args.keys():
        location = args['location']
        query_string = query_string + location
    if 'date' in args.keys():
        date = args['date']
        query_string = query_string + date

    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    driver.get(f'https://www.stubhub.com/find/s/?{query_string}')
    html = driver.page_source
    soup = BeautifulSoup(html)
    
    if 'result_num' in args.keys():
        result_num = int(args['result_num'])
    else:
        result_num = 0

    events = soup.findAll('div', class_='EventRedirection')
    if result_num > len(events):
        return {
        'statusCode': 400,
        'body': { 'message': "No more events found" }
        }
    if events[result_num] is None:
        return {
        'statusCode': 400,
        'body': { 'message': "No events found" }
        }
    
    event = events[result_num]
    link = event.find('a', href=True)
    href = link['href']
    url = f'https://www.stubhub.com{href}'
    driver.close()
    
    return {
        'statusCode': 200,
        'body': { 'url': url }
    }
