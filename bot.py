import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
 
# user agent to access the page
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582" ,
    "Accept-Language" : "en-US, en;q=0.5"
}
 
# what is being searched on amazon
search_query = 'security cameras'.replace(' ', '+')
# adds the amazon url with the search query
base_url = 'https://www.amazon.ca/s?k={0}'.format(search_query)
 
items = []
for i in range(1,11):
    print('Processing {0} ... ' .format(base_url, '&page={0}'.format(i)))
    response = requests.get(base_url + '&page={0}'.format(i) , headers=headers , verify = False)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find_all('div' , {'class': 's-result-item', 'data-component-type' : 's-search-result'})
    # retrieves the product name from the h2 element
    for result in results:
        product_name = result.h2.text
       
        #finds the rating of the product
        try:
            if result.find('div', 'a-row').span.a.span.text == 'Sponsored' :
                continue
            rating = result.find( 'i' , {'class' : 'a-icon'}).text
            rating_count = result.find( 'span' , {'class' : 'a-size-base'}).text
           
        
        except AttributeError:
            continue
       
        # find the price
        try:
            price_int = result.find( 'span' , {'class' : 'a-price-whole'}).text
            product_url = 'https://www.amazon.ca' + result.h2.a['href']
            items.append({product_name, rating, rating_count, price_int, product_url})
           
            
        except AttributeError:
            continue
   
 
       
df = pd.DataFrame(items, columns = ['Product', "Rating", "Rating Count" , "Price", "URL"])
df.to_csv('{0}.csv'.format(search_query), index = False )