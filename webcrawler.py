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
        new_waiting_urls = []
        new_broken_urls = []
        try:
            response = requests.get(cur_url)
        except:
            new_broken_urls.append(cur_url)
        
        parts = urlsplit(cur_url)
        base = "{0.netloc}".format(parts)
        strip_base = base.replace("www.", "")
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        path = cur_url[:cur_url.rfind('/')+1] if '/' in parts.path else cur_url
        
        soup = BeautifulSoup(response.text, "lxml")
        
        new_internal_urls = []
        new_external_urls = []
        for link in soup.find_all('a'):
            anchor = link.attrs["href"] if "href" in link.attrs else ''

            if anchor.startswith('/'):
                local_link = base_url + anchor
                new_internal_urls.append(local_link)
                new_waiting_urls.append(local_link)
            elif not anchor.startswith('http'):
                local_link = path + anchor
                new_internal_urls.append(local_link)
                new_waiting_urls.append(local_link)
            elif strip_base in anchor[:30]: #must be found at start of url
                new_internal_urls.append(anchor)
                new_waiting_urls.append(anchor)
            
            else:
                new_external_urls.append(anchor)
                
        return [new_waiting_urls, new_internal_urls, new_external_urls, new_broken_urls]
    
    def flatten_links(self, links):
        return [item for sublist in links for item in sublist]
        
    def crawl(self):
        while self.waiting_urls:
            j = 0
            next_batch_urls = []
            while j < 6 and self.waiting_urls: 
                cur_url = self.waiting_urls.popleft()
                self.visited_urls.add(cur_url)
                next_batch_urls.append(cur_url)
                j += 1
             
            cpu_count = multiprocessing.cpu_count()
            number_of_cpus_to_use = max(1, cpu_count - 2)
            pool = multiprocessing.Pool(number_of_cpus_to_use)
            new_urls = pool.map(self.find_all_links, next_batch_urls)
            pool.close()
                                
            print(new_urls)
            print("------------------")
            
            all_new_waiting_urls = [x[0] for x in new_urls]
            all_new_internal_urls = [x[1] for x in new_urls]
            all_new_external_urls = [x[2] for x in new_urls]
            all_new_broken_urls = [x[3] for x in new_urls]
            
            new_waiting_urls = self.flatten_links(all_new_waiting_urls)
            new_internal_urls = self.flatten_links(all_new_internal_urls)
            new_external_urls = self.flatten_links(all_new_external_urls)
            new_broken_urls = self.flatten_links(all_new_broken_urls)
            
            for item1 in new_internal_urls:
                self.internal_urls.add(item1)
            for item2 in new_external_urls:
                self.external_urls.add(item2)
            for item3 in new_broken_urls:
                self.broken_urls.add(item3)
            
            for i in list(new_waiting_urls):
                if i not in self.visited_urls and not i in self.waiting_urls:
                    self.waiting_urls.append(i)
                    
    def get_sitemap(self):
        sorted_sitemap = sorted(list(self.internal_urls))
        return sorted_sitemap
    
if __name__ == "__main__":
    webc = WebCrawler('https://tomblomfield.com/')
    webc.crawl()