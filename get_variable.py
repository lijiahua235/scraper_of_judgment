from scraper import crawl_judgments
from bs4 import BeautifulSoup

# can choose how many page want to be, define the first page to the last page
page_start = 1
page_end = 1
list_HTML_all_judgment = crawl_judgments(start_page=page_start, end_page=page_end)


#case_citation	String	Unique ID for retrieval and grouping	Easy
title_list = []
for item in list_HTML_all_judgment:
    html = item["html"]
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.get_text(strip=True)
    title_list.append(title)

print(f"The list of case_citation is {title_list}")

#for the rest two of the variables, it can not only use the basic html parser but also use the LLM-method to
#get the exact details
