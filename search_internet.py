import requests
from bs4 import BeautifulSoup

def search_duckduckgo(query):
    url = f"https://html.duckduckgo.com/html/?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # Start a session to persist headers and cookies
    session = requests.Session()
    response = session.get(url, headers=headers)

    # print(response.text)
    

    # Process the HTML response if it's as expected
    if response.status_code == 200 and "DuckDuckGo" in response.text:
        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        for result in soup.find_all("a", class_="result__a", limit=6):
            title = result.text
            link = result['href']
            parent_div = result.find_parent("div", class_="result__body")
            snippet = parent_div.find("a", class_="result__snippet").text if parent_div else "No description available"
            results.append({
                "title": title,
                "link": link,
                "snippet": snippet
            })
        return results
    else:
        print("Unexpected response or content.")
        return []

def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # Start a session to persist headers and cookies
    session = requests.Session()
    response = session.get(url, headers=headers)
    
    # print(response.text)  # For debugging purposes
    
    # Process the HTML response if it's as expected
    if response.status_code == 200 and "Google" in response.text:
        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        
        # Find result container
        result_containers = soup.find_all("div", class_="tF2Cxc", limit=6)
        
        for container in result_containers:
            title_tag = container.find("h3")
            title = title_tag.text if title_tag else "No title available"
            
            link_tag = container.find("a")
            link = link_tag['href'] if link_tag else "No link available"
            
            snippet_tag = container.find("div", class_="yXK7lf")
            snippet = snippet_tag.text if snippet_tag else "No description available"
            
            results.append({
                "title": title,
                "link": link,
                "snippet": snippet
            })
        
        return results
    else:
        print("Unexpected response or content.")
        return []