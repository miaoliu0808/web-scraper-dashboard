import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_page_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"[-] 请求发生错误: {e}")
        return None

def extract_book_info(soup):
    extracted_data = [] 
    book_containers = soup.find_all("article", class_="product_pod")
    for book in book_containers:
        title_element = book.find("h3").find("a")
        title = title_element.get("title") if title_element else "N/A"
        price_element = book.find("p", class_="price_color")
        price = price_element.text.strip() if price_element else "N/A"
        extracted_data.append({"Title": title, "Price": price})
    return extracted_data

def get_next_page_url(soup, current_url):
    next_button = soup.find("li", class_="next")
    if next_button:
        next_page_link = next_button.find("a").get("href")
        return urljoin(current_url, next_page_link)
    return None

# [+] 核心重构：将散落的执行逻辑，封装成一个供 View 调用的主函数
def run_b2b_scraper(max_pages=3):
    """
    接收抓取页数，执行抓取，最后返回生成的 CSV 文件名。
    """
    start_url = "https://books.toscrape.com/"
    all_books_data = []
    current_url = start_url
    page_count = 1

    while current_url and page_count <= max_pages:
        soup_obj = fetch_page_data(current_url)
        if soup_obj:
            page_data = extract_book_info(soup_obj)
            all_books_data.extend(page_data)
            
            next_url = get_next_page_url(soup_obj, current_url)
            if next_url:
                current_url = next_url
                page_count += 1
                time.sleep(2) # 礼貌防封
            else:
                break
        else:
            break

    # 导出文件并返回文件名
    if all_books_data:
        df = pd.DataFrame(all_books_data)
        # [+] 专业细节：加入时间戳。Web 环境下可能有多个用户同时点击抓取，
        # 用时间戳命名可以防止文件相互覆盖冲突。
        timestamp = int(time.time())
        filename = f"scraped_data_{timestamp}.csv"
        
        df.to_csv(filename, index=False, encoding="utf-8-sig")
        return filename
    
    return None