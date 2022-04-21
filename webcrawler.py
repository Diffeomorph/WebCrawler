##### WEB CRAWLER ######

from bs4 import BeautifulSoup
import requests
import requests.exceptions
import collections
from urllib.parse import urlsplit
import multiprocessing


class WebCrawler():
    """
    Web Crawler Class to crawl a given website and not visit external sites
    """
    
    def __init__(self, start_url):
        self.waiting_urls = collections.deque([(start_url, -1)]) # child, parent
        self.visited_urls = set()
        self.internal_urls = set([(start_url, -1),])
        self.external_urls = set()
        self.broken_urls = set()
        self.internal_urls
        
    def find_all_links(self, cur_url):
        new_waiting_urls = []
        new_internal_urls = []
        new_external_urls = []
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
    
    def flatten_list(self, listi):
        return [item for sublist in listi for item in sublist]
        
    def crawl(self):
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
        sorted_sitemap = sorted(list(self.internal_urls))
        return sorted_sitemap

# A class to store a binary tree node
class Node:
    def __init__(self, url):
        self.url = url
        self.children = []
        
# Function to build a tree from the given parent list
class Tree:
    def __init__(self):
        self.root = None
        self.number_of_nodes = 0
        
    def create_tree(self, parent_child_array):
        d = {}
     
        # create `n` new tree nodes, each having a value from 0 to `n-1`,
        # and store them in a dictionary
        for i, value in enumerate(parent_child_array):
            d[value[0]] = Node(value[0])
     
        # represents the root node of tree
        root_ = None
     
        # traverse the parent list and build the tree
        for i, value in enumerate(parent_child_array):
     
            # if the parent is -1, set the root to the current node having the
            # value `i` (stored in map[i])
            if value[1] == -1:
                root_ = d[value[0]]
            else:
                # get the parent for the current node
                ptr = d[value[1]]
                ptr.children.append(d[value[0]])
        
        self.root = root_        
        return
    
    # Function to print the
    # N-ary tree graphically
    def print_ntree(self, node, flag,depth,is_last):
        # Condition when node is None
        if node == None:
            return
           
        # Loop to print the depths of the
        # current node
        for i in range(1, depth):
            # Condition when the depth
            # is exploring
            if flag[i]:
                print("| ","", "", "", end = "")
               
            # Otherwise print
            # the blank spaces
            else:
                print(" ", "", "", "", end = "")
           
        # Condition when the current
        # node is the root node
        if depth == 0:
            print(node.url)
           
        # Condition when the node is
        # the last node of
        # the exploring depth
        elif is_last:
            print("+---", node.url)
               
            # No more childrens turn it
            # to the non-exploring depth
            flag[depth] = False
        else:
            print("+---", node.url)
       
        it = 0
        for i in node.children:
            it+=1
             
            # Recursive call for the
            # children nodes
            self.print_ntree(i, flag, depth + 1, it == (len(node.children) - 1))
        flag[depth] = True
     
        

if __name__ == "__main__":
    site_url = 'https://tomblomfield.com/'
    webc = WebCrawler(site_url)
    webc.crawl()
    
    tree = Tree()
    tree.create_tree(list(webc.internal_urls))
    #tree.print_ntree(tree.root, [True]*10**7, 0, False)
    