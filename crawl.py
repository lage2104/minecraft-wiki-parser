import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import random

from queue import Queue
from threading import Thread 

def crawl(q , result):
    while not q.empty():
        # fetch work from queue
        work = q.get()
        try:
            session = requests.Session()
            retry = Retry(connect=10, backoff_factor=random.randint(5,10))
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            response = session.get(work[1])
            result[work[0]] = response
        except:
            result[work[0]] = {}
            pass
        #Signal that task has been executed
        q.task_done()
    return True


def fetch_url_contents(urls):
    """
    Function to fetch a list of urls parallel
    :param urls: list
    :return: list with responses
    """
    # ref https://www.shanelynn.ie/using-python-threading-for-multiple-results-queue/
    # Set up queue to hold all urls
    q = Queue(maxsize=0)
    # Use threads (max 50 or one for each url)
    num_threads = min(50,len(urls))

    # List for results
    results = [None] * len(urls)

    # Load queue
    # index and url as tuple
    for i in range(len(urls)):
        # put index and url from index in queue
        q.put((i,urls[i]))

    # Start worker threads with queue processing
    for i in range(num_threads):
        worker = Thread(target=crawl,args=(q,results))
        # Set worker as deamon.
        # allows main program to exit
        worker.setDaemon(True)
        worker.start()
    
    q.join()
    return results