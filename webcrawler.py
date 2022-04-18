##### WEB CRAWLER
from bs4 import BeautifulSoup
import requests
import requests.exceptions
import collections
from urllib.parse import urlsplit

class WebCrawler():
    
    def __init__(self, start_url):
        self.waiting_urls = collections.deque([start_url])
        self.visited_urls = set()
        self.internal_urls = set()
        self.external_urls = set()
        self.broken_urls = set()
        
    def crawl(self):
        while self.waiting_urls:
            cur_url = self.waiting_urls.popleft()
            self.visited_urls.add(cur_url)
            
            try:
                response = requests.get(cur_url)
            except:
                self.broken_urls.add(cur_url)
                continue
            
            parts = urlsplit(cur_url)
            base = "{0.netloc}".format(parts)
            strip_base = base.replace("www.", "")
            base_url = "{0.scheme}://{0.netloc}".format(parts)
            path = cur_url[:cur_url.rfind('/')+1] if '/' in parts.path else cur_url
            
            soup = BeautifulSoup(response.text, "lxml")
            
            new_urls = []
            for link in soup.find_all('a'):
                anchor = link.attrs["href"] if "href" in link.attrs else ''

                if anchor.startswith('/'):
                    local_link = base_url + anchor
                    self.internal_urls.add(local_link)
                    new_urls.append(local_link)
                elif strip_base in anchor:
                    self.internal_urls.add(anchor)
                    new_urls.append(anchor)
                elif not anchor.startswith('http'):
                    local_link = path + anchor
                    self.internal_urls.add(local_link)
                    new_urls.append(local_link)
                else:
                    self.external_urls.add(anchor)
            
            for i in new_urls:
                if i not in self.visited_urls:
                    self.waiting_urls.append(i)