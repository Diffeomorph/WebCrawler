##### WEB CRAWLER ######

from bs4 import BeautifulSoup
import requests
import requests.exceptions
import collections
from urllib.parse import urlsplit
import multiprocessing
import dynamic_nary_tree as dnt


class WebCrawler():
    """
    Web Crawler Class to crawl a given website and not visit external sites
    """
    
    def __init__(self, start_url):
        self.waiting_urls = collections.deque([(start_url, -1)]) #urls waiting to be search in (child, parent) format
        self.visited_urls = set()
        self.internal_urls = set([(start_url, -1),])
        self.external_urls = set()
        self.broken_urls = set()
        
    def find_all_links(self, cur_url):
        """
        Parameters
        ----------
        cur_url : the page to be searched for links

        Returns
        -------
        list of lists of waiting_urls (to be searched), internal_urls, external_urls, broken_urls

        """
        new_waiting_urls = []
        new_internal_urls = []
        new_external_urls = []
        new_broken_urls = []
        
        try:
            response = requests.get(cur_url)
        except requests.exceptions.RequestException as e:
            print(e)
            new_broken_urls.append(cur_url)
                
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
    
    def flatten_list(self, list_of_lists):
        """
        Returns
        -------
        A single list containing the elements of the given list of lists, ie a flattened list of lists.
        """
        return [item for sublist in list_of_lists for item in sublist]
        
    def crawl(self):
        """
        Crawls the given site using a BFS algorithm, and does so using multiprocessing.
        """
        cpu_count = multiprocessing.cpu_count()
        number_of_cpus_to_use = max(1, cpu_count - 2)
        
        while self.waiting_urls:
            j = 0
            next_batch_urls = []
            while j < number_of_cpus_to_use and self.waiting_urls: 
                (cur_url, parent) = self.waiting_urls.popleft()
                self.visited_urls.add(cur_url)
                next_batch_urls.append(cur_url)
                j += 1
            
            # use pool of workers to process multiple links from above simultaneously
            pool = multiprocessing.Pool(number_of_cpus_to_use)
            new_urls = pool.map(self.find_all_links, next_batch_urls)
            pool.close()
                                
            print(new_urls)
            print("------------------")
            
            all_new_waiting_urls = [x[0] for x in new_urls]
            all_new_internal_urls = [x[1] for x in new_urls]
            all_new_external_urls = [x[2] for x in new_urls]
            all_new_broken_urls = [x[3] for x in new_urls]
            
            new_waiting_urls = self.flatten_list(all_new_waiting_urls)
            new_internal_urls = self.flatten_list(all_new_internal_urls)
            new_external_urls = self.flatten_list(all_new_external_urls)
            new_broken_urls = self.flatten_list(all_new_broken_urls)
            
            for i in new_internal_urls:
                self.internal_urls.add((i,cur_url))
            for j in new_external_urls:
                self.external_urls.add(j)
            for k in new_broken_urls:
                self.broken_urls.add(k)
            
            for url in list(new_waiting_urls):
                if url not in self.visited_urls and not url in self.waiting_urls:
                    self.waiting_urls.append((url,cur_url))
                    
    def get_sitemap(self):
        """
        Returns
        -------
        ans : list of urls in lexographical order that the given site contains

        """
        urls = set()
        for x,y in self.internal_urls:
            if x != -1:
                urls.add(x)
            if y != -1:
                urls.add(y)
        ans = sorted(list(urls))
        return ans


if __name__ == "__main__":
    site_url = 'https://tomblomfield.com/'
    webc = WebCrawler(site_url)
    webc.crawl()
    
    tree = dnt.DynamicNaryTree()
    tree.create_tree(list(webc.internal_urls))
    #tree.print_ntree(tree.root, [True]*10**7, 0, False)
    