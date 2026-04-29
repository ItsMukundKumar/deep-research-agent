from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

tavily = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))

@tool
def web_search(query : str) -> str:
    """Use this tool to perform real-time web searches and retrieve up-to-date information. Return titles, URLs, and snippets."""
    
    search = tavily.search(query=query,max_results=5)
    
    result = []
    for r in search['results']:
        result.append(f'Title : {r['title']}\nURL : {r['url']}\n\t Snippet : {r['content'][:300]}\n')
        
    
    return '\n----\n'.join(result)

@tool
def scrape_url(url : str) -> str:
    """Use this tool to extract and clean text content from a specific webpage URL."""
    try:
        resp = requests.get(url=url,timeout= 10, headers={'User-Agent' : 'Mozilla/5.0'})
        soup = BeautifulSoup(resp.text,'html.parser')
        for tag in soup(['script','style','nav','footer']):
            tag.decompose()
        return soup.get_text(separator=' ', strip=True)[200:3500]
    except Exception as err:
        return f'Could not scrape URL: {str(err)}'
