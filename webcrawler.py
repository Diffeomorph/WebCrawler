##### WEB CRAWLER ######

from bs4 import BeautifulSoup
import requests
import requests.exceptions
import collections
from urllib.parse import urlsplit
import multiprocessing

class WebCrawler():
    
    def __init__(self, start_url):
        self.waiting_urls = collections.deque([start_url])
        self.visited_urls = set()
        self.internal_urls = set()
        self.external_urls = set()
        self.broken_urls = set()
        
    def find_all_links(self, cur_url):
        found_urls = []
        try:
            response = requests.get(cur_url)
        except:
            self.broken_urls.add(cur_url)
        
        parts = urlsplit(cur_url)
        base = "{0.netloc}".format(parts)
        strip_base = base.replace("www.", "")
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        path = cur_url[:cur_url.rfind('/')+1] if '/' in parts.path else cur_url
        
        soup = BeautifulSoup(response.text, "lxml")
        
        for link in soup.find_all('a'):
            anchor = link.attrs["href"] if "href" in link.attrs else ''

            if anchor.startswith('/'):
                local_link = base_url + anchor
                self.internal_urls.add(local_link)
                found_urls.add(local_link)
            elif not anchor.startswith('http'):
                local_link = path + anchor
                self.internal_urls.add(local_link)
                found_urls.add(local_link)
            elif strip_base in anchor[:30]: #must be found at start of url
                self.internal_urls.add(anchor)
                found_urls.add(anchor)
            
            else:
                self.external_urls.add(anchor)
                
        return found_urls
        
    def crawl(self):
        while self.waiting_urls:
            cur_url = self.waiting_urls.popleft()
            self.visited_urls.add(cur_url)
            new_urls = set()
            
            process_list = []
            for i in range(6): #cores
                p =  multiprocessing.Process(target= self.find_all_links)
                p.start()
                process_list.append(p)
            
            for process in process_list:
                process.join()
            
            print(process_list)
                    
            print(new_urls)
            print("------------------")
            
            for i in list(new_urls):
                if i not in self.visited_urls and not i in self.waiting_urls:
                    self.waiting_urls.append(i)
                    
    def get_sitemap(self):
        sorted_sitemap = sorted(list(self.internal_urls))
        return sorted_sitemap