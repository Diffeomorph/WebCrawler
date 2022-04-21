##### WEB CRAWLER TESTS

import unittest
import webcrawler as wc

class TestWebCrawler(unittest.TestCase):
    def test_find_all_links(self):
        webc_test = wc.WebCrawler('https://tomblomfield.com/')
        expected = [['https://tomblomfield.com/',
  'https://tomblomfield.com/about',
  'https://tomblomfield.com/archive',
  'https://tomblomfield.com/random',
  'https://tomblomfield.com/rss',
  'http://tomblomfield.com'],
 ['https://tomblomfield.com/',
  'https://tomblomfield.com/about',
  'https://tomblomfield.com/archive',
  'https://tomblomfield.com/random',
  'https://tomblomfield.com/rss',
  'http://tomblomfield.com'],
 ['https://href.li/?https://monzo.com',
  'https://href.li/?https://gocardless.com',
  'https://twitter.com/t_blom',
  'http://tomblomfield.disqus.com/?url=ref',
  'https://www.tumblr.com/'],
 []]
        
        self.assertEqual(webc_test.find_all_links('https://tomblomfield.com/about'), expected)
    
    
    def test_flatten_list(self):
        webc_test = wc.WebCrawler('None')
        self.assertEqual(webc_test.flatten_list([[3,4],[5,6,7],[6],[7],[1,1,1]]), [3,4,5,6,7,6,7,1,1,1])
        
    
    
if __name__ == '__main__':
    unittest.main()