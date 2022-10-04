# Assignment: Week-3
# Request-2: Python網頁爬取資料並儲存到檔案中 (Optional) 

import urllib.request as req
import bs4
import time

movie_titles = [] # create list for saving extracted titles

# cawler for one page
def get_one_page(url):
    # create Request object with headers (pretended as a human user)
    request = req.Request(url, headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    })
    # open url by Request object
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    # use BeautifulSoup to get html
    root = bs4.BeautifulSoup(data, "html.parser")
    return root    

# filter titles
def get_title(root):
    # find <div> with class="title" and get data as a list (titles)
    titles = root.find_all("div", class_ = "title")
    # filter titles
    for title in titles:
        if title.a != None and title.a.string[0] == "[": # exclude titles without link (a), and titles need to start from "["
            if "[好雷]" in title.a.string or "[普雷]" in title.a.string or "[負雷]" in title.a.string: # get only "[好雷]", "[普雷]", "[負雷]"
                movie_titles.append(title.a.string) # put titles into list (movie_titles)

# get previous page from html
def get_pre_page(root):
    links = root.find_all("div", class_="btn-group btn-group-paging") # <div> with class="btn-group btn-group-paging", including links for the previous page
    for link in links:
        pre_page = "https://www.ptt.cc" + link.select("a")[1].get("href") # the previous page is at index = 1
    return pre_page


# start from index.html
ptt_movie_url="https://www.ptt.cc/bbs/movie/index.html"
# crawl 10 pages
for i in range(0, 10):
    html_data = get_one_page(ptt_movie_url)
    get_title(html_data)
    ptt_movie_url = get_pre_page(html_data) # replace ptt_movie_url with the previous page
    time.sleep(1) # avoid request forbidden by ptt

# put titles into file by order with [好雷] -> [普雷] -> [負雷]
with open("movie.txt", "w", encoding = "utf-8") as file:
    for title in movie_titles:
        if "[好雷]" in title:
            file.write(title + "\n")
    for title in movie_titles:
        if "[普雷]" in title:
            file.write(title + "\n")
    for title in movie_titles:
        if "[負雷]" in title:
            file.write(title + "\n")