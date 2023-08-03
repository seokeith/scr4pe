from apify_client import ApifyClient
import pandas as pd
import streamlit as st

@st.cache(show_spinner=False, allow_output_mutation=True)
def scrape_google(search):

    # Define the Apify API URL and the actor's name
    APIFY_API_URL = 'https://api.apify.com/v2'
    ACTOR_NAME = 'apify/google-search-scraper'

    # Retrieve the Apify API key from Streamlit secrets
    APIFY_API_KEY = st.secrets["APIFY_API_KEY"]

    # Initialize the ApifyClient with your API token
    client = ApifyClient(APIFY_API_KEY)

    # Prepare the actor input
    run_input = {
        "csvFriendlyOutput": False,
        "customDataFunction": "async ({ input, $, request, response, html }) => {\n  return {\n    pageTitle: $('title').text(),\n  };\n};",
        "includeUnfilteredResults": False,
        "maxPagesPerQuery": 1,
        "mobileResults": False,
        "queries": search,
        "resultsPerPage": 10,
        "saveHtml": False,
        "saveHtmlToKeyValueStore": False
    }

    print(f"Running Google Search Scrape for {search}")
    # Run the actor and wait for it to finish
    run = client.actor(ACTOR_NAME).call(run_input=run_input)
    print(f"Finished Google Search Scrape for {search}")

    # Fetch the actor results from the run's dataset
    results = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        results.append(item)

    # Extract URLs from organic results
    organic_results = [item['organicResults'] for item in results]
    urls = [result['url'] for sublist in organic_results for result in sublist]

    # Create DataFrame
    df = pd.DataFrame(urls, columns=['url'])

    # Print the dataframe
    print(df)
    st.header("Scraped Data from SERP and SERP Links")
    st.table(df)  # Display the dataframe as a table in Streamlit
    return df

    # Get the search term from the user
search_term = st.text_input('Enter your search term:')

# If the user has entered a search term, scrape Google
if search_term:
    df = scrape_google(search_term)
