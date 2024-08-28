import requests
from bs4 import BeautifulSoup

def search_duckduckgo(query):
    url = f"https://html.duckduckgo.com/html/?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for result in soup.find_all("a", class_="result__a", limit=6):
        title = result.text
        link = result['href']
        # Find the parent div to extract the snippet
        parent_div = result.find_parent("div", class_="result__body")
        snippet = parent_div.find("a", class_="result__snippet").text if parent_div else "No description available"
        results.append({
            "title": title,
            "link": link,
            "snippet": snippet
        })

    return results
