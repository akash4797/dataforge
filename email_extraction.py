import requests
from bs4 import BeautifulSoup
import re
import time

# Function to extract emails from a text
def extract_emails(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    return emails

# Function to perform a Google search and extract emails from the results
def search_email_google(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # Start a session to persist headers and cookies
    session = requests.Session()
    response = session.get(url, headers=headers)
    
    # Process the HTML response if it's as expected
    if response.status_code == 200 and "Google" in response.text:
        soup = BeautifulSoup(response.text, "html.parser")
        emails_found = set()  # To store unique emails
        
        # Find result containers (using the updated container class Google may use)
        result_containers = soup.find_all("div", class_="tF2Cxc", limit=5)
        
        for container in result_containers:
            link_tag = container.find("a")
            link = link_tag['href'] if link_tag else None
            
            if link:
                try:
                    # Fetch the webpage content for the result link
                    page = session.get(link, headers=headers)
                    page_content = page.text
                    
                    # Extract emails from the page content
                    emails = extract_emails(page_content)
                    emails_found.update(emails)
                    
                    # Sleep to avoid overwhelming the server
                    time.sleep(1)
                except Exception as e:
                    print(f"Failed to fetch {link}: {e}")
        
        # Return unique emails found
        return list(emails_found) if emails_found else "No emails found"
    
    else:
        print(f"Failed to retrieve search results for {query}. Status code: {response.status_code}")
        return []

# Function to process multiple company names
def search_emails_for_multiple_companies(company_names):
    results = {}

    for company_name in company_names:
        print(f"Searching emails for: {company_name}")
        emails = search_email_google(company_name)
        results[company_name] = emails
    
    return results