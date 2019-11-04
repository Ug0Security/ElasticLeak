my_list = """
"""

url_list = my_list.split('\n')[1:-1]
url_list = set(url_list)                    # eleminate ducplicate in case of
url_ltuple = list()

i = 0
for url in url_list:
    url_ltuple.append((i, url))
    i += 1
