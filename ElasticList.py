#!/usr/bin/env ../venv/bin/python3.5

import sys
import logging
import asyncio
from aiohttp import ClientSession, TCPConnector, client_exceptions
import socket
from time import time, localtime, strftime


from setting import USER_AGENT, CONN_TIMEOUT, READ_TIMEOUT, IPV4_ONLY


sitelist = sys.argv[1]

my_list = """
"""

	


url_list = my_list.split('\n')[1:-1]
url_list = set(url_list)                    # eleminate ducplicate in case of
url_ltuple = list()


with open (sitelist) as sl:
    for line in sl:
        mainsite = line.rstrip()
        url_ltuple.append((0,"http://" + mainsite + ":9200/_cat/indices" ))
        



sites = list()


client_headers = {'User-agent': USER_AGENT,
            'Accept-Language': 'en-US,en;q=0.8',
            'Accept': '*/*','Accept-Encoding': 'gzip,deflate,sdch'
            }



class Site(object):
    def __init__(self, id, url):
        self.id = id
        self.url = url
        self.status = None
        self.headers = None
        self.state = None
        self.resp_time = None
        self.test_time = None


for id, url in url_ltuple:
    sites.append(Site(id, url))



def mutlidict2string(multidict):
    lines = list()
    for key in multidict:
        line = ''.join((key, ': ', str(multidict[key]), '\n'))
        lines.append(line)

    text = ''.join(lines)
    return text


async def gethead(site, session, start_time, retesting=False):

    try:
        async with session.get(site.url, allow_redirects=False) as response:
            site.status = str(response.status)
            html = await response.text()
            if (site.status == "200"):
                print (site.url + " == " + site.status)
                
                data = html.split("\n") 
                
                for item in data:
                   
                    print(site.url[:-13] + "/" + item.split()[2] + "/_search?q=*&pretty")
                    
                    #print(html.split()[2+i*9])
                    #
                  
            else:
                pass
    except asyncio.TimeoutError:
        pass
    except ValueError:
        pass
    except client_exceptions.ClientConnectionError:
        pass
    except client_exceptions.ClientResponseError:
        pass
    except:
        pass


async def bound_gethead(sem, site, session, retesting=False):

    async with sem:
        start_time = time()
        await gethead(site, session, start_time=start_time, retesting=retesting)


async def run(sites, retesting=False):

    if IPV4_ONLY:
        connector = TCPConnector(verify_ssl=False, family=socket.AF_INET)
    else:
        connector = TCPConnector(verify_ssl=False)

    sem = asyncio.Semaphore(100)

    tasks = []
    if not retesting:
        read_timeout = READ_TIMEOUT
        conn_timeout = CONN_TIMEOUT
    else:
        read_timeout = READ_TIMEOUT + READ_TIMEOUT/2
        conn_timeout = CONN_TIMEOUT + CONN_TIMEOUT/2

    async with ClientSession(connector=connector, read_timeout=read_timeout,
                             conn_timeout=conn_timeout, headers=client_headers) as session:
        for site_ in sites:

            task = asyncio.ensure_future(bound_gethead(sem, site_, session, retesting=retesting))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)


loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(sites=sites))
loop.run_until_complete(future)



