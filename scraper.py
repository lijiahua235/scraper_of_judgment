import requests
from bs4 import BeautifulSoup
import time


BASE_URL = "https://www.elitigation.sg"
LIST_URL = "https://www.elitigation.sg/gd/Home/Index"

headers = {
    "User-Agent": "Mozilla/5.0"
}

#the judment list webpage url is
# https://www.elitigation.sg/gd/Home/Index?Filter=SUPCT
#                                           &YearOfDecision=All
#                                           &SortBy=Score
#                                           &CurrentPage=1028
#                                           &SortAscending=False
#                                           &PageSize=0   #no influence
#                                           &Verbose=False
#                                           &SearchQueryTime=0  #no influence
#                                           &SearchTotalHits=0  #no influence
#                                           &SearchMode=True  #no influence
#                                           &SpanMultiplePages=False  #no influence
def get_list_page(page_number):
    params = {
        "Filter": "SUPCT",
        "YearOfDecision": "All",
        "SortBy": "Score",
        "CurrentPage": page_number,
        "SortAscending": "False",
        "Verbose": "False"
    }

    resp = requests.get(LIST_URL, headers=headers, params=params)
    resp.raise_for_status()
    return resp.text


def extract_judgment_urls(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    urls = []

#each url of judment is inside the <a> as header
    for a in soup.select("a.h5.gd-heardertext"):
        # title = a.get_text(strip=True)
        href = a.get("href")
        if href:
            urls.append(BASE_URL + href)

    return urls


def get_judgment_content(url):
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.text


def crawl_judgments(start_page=1, end_page=3):
    all_data = []

    for page in range(start_page, end_page + 1):
        print(f"Searching the page {page} ...")

        html = get_list_page(page)
        urls = extract_judgment_urls(html)

        print(f" found {len(urls)} judgments")

        for url in urls:
            print(f"fetching the content of judgment: {url}")
            content = get_judgment_content(url)

            all_data.append({
                "url": url,
                "html": content
            })

            time.sleep(1)

    return all_data


if __name__ == "__main__":
    #can choose how many page want to be
    data = crawl_judgments(start_page=1, end_page=1)

    # 保存
    import json
    with open("judgments.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("🎉 succeed！save to judgments.json")