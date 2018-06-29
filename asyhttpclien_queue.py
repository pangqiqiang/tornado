#!/usr/bin/env python
#-*-coding:utf-8-*-

import time
from datetime import timedelta
try:
    from HTMLParser import HTMLParser
    from urlparse import urljoin, urldefrag
except ImportError:
    from html.parser import HTMLParser
    from urllib import urljoin, urldefrag

from tornado import httpclient, gen, ioloop, queues

base_url = 'http://www.tornadoweb.org/statble/'
concurrency = 10

@gen.coroutine
def get_links_from_url(url):
    """Downlaod the page at 'url' and parse it for links

    Return links have had the fragmet after '#' removed, and have been made
    absolute"""

    try:
        response = yield httpclient.AsyncHTTPClient().fetch(url)
        print('fetch %s' % url)

        html = response.body if isinstance(response.body, str) \
            else response.body.decode()
        urls = [urljoin(url, remove_fragment(new_url))
            for new_url in get_links(html)]
    except Exception as e:
        print('Exception: %s %s' % (e, url))
        #raise gen.Return([])
        return []
    #raise gen.Return(urls)
    return urls

def remove_fragment(url):
    pure_url, _ = urldefrag(url)
    return pure_url

def get_links(html):
    class URLSeeker(HTMLParser):
        def __init__(self):
            super(URLSeeker,self).__init__()
            self.urls = []
        def handle_starttag(self, tag, attrs):
            href = dict(attrs).get('href')
            if href and tag == 'a':
                self.urls.append(href)
    
    url_seeker = URLSeeker()
    url_seeker.feed(html)
    return url_seeker.urls

def main():
    q = queues.Queue()
    start = time.time()
    fetching, fetched = set(), set()
    
    @gen.coroutine
    def fetch_url():
        current_url = yield q.get()
        try:
            if current_url in fetching:
                return
            print('fetching %s' % current_url)
            fetching.add(current_url)
            urls = yield get_links_from_url(current_url)
            fetched.add(current_url)

            for new_url in urls:
                #only follow links beneath the base URL
                if new_url.startswith(base_url):
                    yield q.put(new_url)
        finally:
            q.task_done()

        @gen.coroutine
        def worker():
            while True:
                yield fetch_url()

        q.put(base_url)
        # Start workers, then wait for the work queue to be empty.
        for _ in range(concurrency):
            worker()
        yield q.join(timeout=timedelta(seconds=300))
        assert fetching == fetched
        print('Done in %d seconds, fetched %s URLs.' % (
        time.time() - start, len(fetched)))


if __name__ == '__main__':
    import logging
    logging.basicConfig()
    io_loop = ioloop.IOLoop.current()
    io_loop.run_sync(main)    

        