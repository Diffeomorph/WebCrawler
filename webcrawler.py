##### WEB CRAWLER
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import collections

class WebCrawler():
    
    def __init__(self, start_url):
        self.queue = collections.deque([start_url])
        #self.start_url = start_url
        self.visited = set()
        
    def crawl(self):
        while self.queue:
            cur = self.queue.popleft()
            print(cur)
            req = Request(cur)
            print(req)
            html_page = urlopen(req)
            soup = BeautifulSoup(html_page, "lxml")
            
            links = []
            for link in soup.findAll('a'):
                links.append(link.get('href'))
            
            print(links)