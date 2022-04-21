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
        
    def test_crawl(self):
        webc_test = wc.WebCrawler('https://tomblomfield.com/')
        webc_test.crawl()
        expected = list({'http://tomblomfield.com',
 'http://tomblomfield.com/',
 'http://tomblomfield.com/about',
 'http://tomblomfield.com/archive',
 'http://tomblomfield.com/day/2012/01/07',
 'http://tomblomfield.com/day/2012/02/05',
 'http://tomblomfield.com/day/2012/02/13',
 'http://tomblomfield.com/day/2012/04/01',
 'http://tomblomfield.com/day/2012/04/20',
 'http://tomblomfield.com/day/2012/11/08',
 'http://tomblomfield.com/day/2013/05/28',
 'http://tomblomfield.com/day/2013/09/20',
 'http://tomblomfield.com/day/2013/09/22',
 'http://tomblomfield.com/day/2013/09/26',
 'http://tomblomfield.com/day/2013/09/29',
 'http://tomblomfield.com/day/2014/03/29',
 'http://tomblomfield.com/day/2014/07/10',
 'http://tomblomfield.com/day/2014/09/12',
 'http://tomblomfield.com/day/2015/11/08',
 'http://tomblomfield.com/day/2015/12/13',
 'http://tomblomfield.com/day/2016/01/14',
 'http://tomblomfield.com/day/2018/06/10',
 'http://tomblomfield.com/day/2021/09/11',
 'http://tomblomfield.com/page/1',
 'http://tomblomfield.com/page/2',
 'http://tomblomfield.com/page/3',
 'http://tomblomfield.com/post/16697498005/automating-customer-service-at-a-startup',
 'http://tomblomfield.com/post/17092502705/automate-everything',
 'http://tomblomfield.com/post/17571449233/home-brew-customer-phone-support',
 'http://tomblomfield.com/post/97304410500/apple-is-propping-up-a-fundamentally-broken-payments',
 'http://tomblomfield.com/random',
 'https://tomblomfield.com/',
 'https://tomblomfield.com/about',
 'https://tomblomfield.com/archive',
 'https://tomblomfield.com/day/2012/01/07',
 'https://tomblomfield.com/day/2012/02/05',
 'https://tomblomfield.com/day/2012/02/13',
 'https://tomblomfield.com/day/2012/04/01',
 'https://tomblomfield.com/day/2012/04/20',
 'https://tomblomfield.com/day/2012/11/08',
 'https://tomblomfield.com/day/2013/05/28',
 'https://tomblomfield.com/day/2013/09/20',
 'https://tomblomfield.com/day/2013/09/22',
 'https://tomblomfield.com/day/2013/09/26',
 'https://tomblomfield.com/day/2013/09/29',
 'https://tomblomfield.com/day/2014/03/29',
 'https://tomblomfield.com/day/2014/07/10',
 'https://tomblomfield.com/day/2014/09/12',
 'https://tomblomfield.com/day/2015/11/08',
 'https://tomblomfield.com/day/2015/12/13',
 'https://tomblomfield.com/day/2016/01/14',
 'https://tomblomfield.com/day/2018/06/10',
 'https://tomblomfield.com/day/2021/09/11',
 'https://tomblomfield.com/page/1',
 'https://tomblomfield.com/page/2',
 'https://tomblomfield.com/page/3',
 'https://tomblomfield.com/post/132810390155',
 'https://tomblomfield.com/post/132810390155/getting-shit-done',
 'https://tomblomfield.com/post/132810390155/getting-shit-done#disqus_thread',
 'https://tomblomfield.com/post/135120600360',
 'https://tomblomfield.com/post/135120600360/five-unbreakable-rules-for-startups',
 'https://tomblomfield.com/post/135120600360/five-unbreakable-rules-for-startups#disqus_thread',
 'https://tomblomfield.com/post/136759441870',
 'https://tomblomfield.com/post/136759441870/so-you-want-to-join-a-startup',
 'https://tomblomfield.com/post/136759441870/so-you-want-to-join-a-startup#disqus_thread',
 'https://tomblomfield.com/post/15450705336',
 'https://tomblomfield.com/post/15450705336/syntax-highlighting-on-tumblr',
 'https://tomblomfield.com/post/15450705336/syntax-highlighting-on-tumblr#disqus_thread',
 'https://tomblomfield.com/post/15451580714',
 'https://tomblomfield.com/post/15451580714/some-of-the-most-thoughtful-startup-related',
 'https://tomblomfield.com/post/15451580714/some-of-the-most-thoughtful-startup-related#disqus_thread',
 'https://tomblomfield.com/post/15456184827',
 'https://tomblomfield.com/post/15456184827/i-hate-meetings',
 'https://tomblomfield.com/post/15456184827/i-hate-meetings#disqus_thread',
 'https://tomblomfield.com/post/15459124407',
 'https://tomblomfield.com/post/15459124407/technical-interviews',
 'https://tomblomfield.com/post/15459124407/technical-interviews#disqus_thread',
 'https://tomblomfield.com/post/16697498005',
 'https://tomblomfield.com/post/16697498005/automating-customer-service-at-a-startup',
 'https://tomblomfield.com/post/16697498005/automating-customer-service-at-a-startup#disqus_thread',
 'https://tomblomfield.com/post/17092502705',
 'https://tomblomfield.com/post/17092502705/automate-everything',
 'https://tomblomfield.com/post/17092502705/automate-everything#disqus_thread',
 'https://tomblomfield.com/post/174754284255',
 'https://tomblomfield.com/post/174754284255/unit-economics',
 'https://tomblomfield.com/post/174754284255/unit-economics#disqus_thread',
 'https://tomblomfield.com/post/17571449233',
 'https://tomblomfield.com/post/17571449233/home-brew-customer-phone-support',
 'https://tomblomfield.com/post/17571449233/home-brew-customer-phone-support#disqus_thread',
 'https://tomblomfield.com/post/20285854071',
 'https://tomblomfield.com/post/20285854071/dont-write-tests-the-hidden-cost-of-tdd',
 'https://tomblomfield.com/post/20285854071/dont-write-tests-the-hidden-cost-of-tdd#disqus_thread',
 'https://tomblomfield.com/post/21440604403',
 'https://tomblomfield.com/post/21440604403/peter-nixey-cook-something-or-get-out-of-the',
 'https://tomblomfield.com/post/21440604403/peter-nixey-cook-something-or-get-out-of-the#disqus_thread',
 'https://tomblomfield.com/post/33506878578',
 'https://tomblomfield.com/post/33506878578/making-something-people-want-the-gocardless',
 'https://tomblomfield.com/post/33506878578/making-something-people-want-the-gocardless#disqus_thread',
 'https://tomblomfield.com/post/51547590294',
 'https://tomblomfield.com/post/51547590294/advice',
 'https://tomblomfield.com/post/51547590294/advice#disqus_thread',
 'https://tomblomfield.com/post/61760552398',
 'https://tomblomfield.com/post/61760552398/startup-series-part-1-interviewing-engineers',
 'https://tomblomfield.com/post/61760552398/startup-series-part-1-interviewing-engineers#disqus_thread',
 'https://tomblomfield.com/post/61958629156',
 'https://tomblomfield.com/post/61958629156/startup-series-part-2-attracting-great-engineers',
 'https://tomblomfield.com/post/61958629156/startup-series-part-2-attracting-great-engineers#disqus_thread',
 'https://tomblomfield.com/post/62342949294',
 'https://tomblomfield.com/post/62342949294/startup-series-part-3-you-make-what-you-measure',
 'https://tomblomfield.com/post/62342949294/startup-series-part-3-you-make-what-you-measure#disqus_thread',
 'https://tomblomfield.com/post/62619282797',
 'https://tomblomfield.com/post/62619282797/startup-series-part-4-deadlines',
 'https://tomblomfield.com/post/62619282797/startup-series-part-4-deadlines#disqus_thread',
 'https://tomblomfield.com/post/662033487432466432',
 'https://tomblomfield.com/post/662033487432466432/how-to-raise-investment',
 'https://tomblomfield.com/post/662033487432466432/how-to-raise-investment#disqus_thread',
 'https://tomblomfield.com/post/81105143223',
 'https://tomblomfield.com/post/81105143223/customer-churn-can-kill-your-startup',
 'https://tomblomfield.com/post/81105143223/customer-churn-can-kill-your-startup#disqus_thread',
 'https://tomblomfield.com/post/81111938563',
 'https://tomblomfield.com/post/81111938563/growth',
 'https://tomblomfield.com/post/81111938563/growth#disqus_thread',
 'https://tomblomfield.com/post/97304410500',
 'https://tomblomfield.com/post/97304410500/apple-is-propping-up-a-fundamentally-broken',
 'https://tomblomfield.com/post/97304410500/apple-is-propping-up-a-fundamentally-broken#disqus_thread',
 'https://tomblomfield.com/random',
 'https://tomblomfield.com/rss'})
        
        self.assertEqual(webc_test.visited_urls, expected)
        
    def test_get_sitemap(self):
        webc_test = wc.WebCrawler('https://tomblomfield.com/')
        webc_test.crawl()
        res = webc_test.get_sitemap()
        expected = []
        
        self.assertEqual(res, expected)
        
        
    
if __name__ == '__main__':
    unittest.main()