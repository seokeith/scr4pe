import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

def google_scrape(query):
    # Replace with your custom Google Search URL
    url = f"https://www.google.com/customsearch?&q={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    search_results = soup.find_all('div', class_='kCrYT')
    urls = []
    for result in search_results:
        link = result.find('a', href=True)
        if link:
            raw_link = link['href']
            clean_link = re.search('\/url\?q=(.*)\&sa', raw_link)
            if clean_link:
                urls.append(clean_link.group(1))
    return urls

st.title('Google URL Scraper')
search_term = st.text_input('Enter your search term:')
if st.button('Scrape'):
    if search_term:
        urls = google_scrape(search_term)
        st.write(urls)
    else:
        st.write('Please enter a search term.')
