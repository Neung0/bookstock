from urllib import parse
from selenium import webdriver
from bs4 import BeautifulSoup as BS
import requests
import re

# 책 재고 체크 위한 크롤링
# url = 서점의 링크, s = 지점명 Selector, t = 재고수량 Selector
def chk_stock(url, s, t):
    req = requests.get(url)
    soup = BS(req.text, 'html.parser')
    store = soup.select(s) # 지점명
    num = soup.select(t) # 재고수량
    stock = [store, num]
    return stock

# book_url 함수에서 받아온 url 이용,
# 각 서점에서 chk_stock 함수 실행
def search_book(url):
    # 교보문고
    if url[0] == '': kb = '재고없음'
    else:
        stock = chk_stock(url[0], 'th', 'a')
        kb = {}
        for i, j in zip(stock[0], stock[1]):
            i = i.text
            i = i.strip()
            if i == '':
                pass
            else:
                kb[i] = j.text
    # 영풍문고
    if url[1] == '': yp = '재고없음'
    else:
        stock = chk_stock(url[1], 'table.tb_store strong', 'table.tb_store span')
        yp = {}
        for i, j in zip(stock[0], stock[1]):
            yp[i.text] = j.text
    # 반디앤루니스
    if url[2] == '': bd = '재고없음'
    else:
        stock = chk_stock(url[2], '.commTable_s th', '.commTable_s a')
        bd = {}
        for i, j in zip(stock[0][1:], stock[1]):
            bd[i.text] = j.text

    bookStock = [kb, yp, bd]
    return bookStock

def book_info(soup):
    info = {}
    con = soup.find('div', {'class':'book_info'})
    inner = soup.select('.book_info_inner > div')[1]
    info['title'] = con.select_one('h2 > a').text
    info['img'] = con.select_one('.thumb_type img')['src']
    info['auth'] = inner.select('a')[0].text
    info['pub'] = inner.select('a')[1].text
    bID = soup.select_one('.book_info_inner')
    p = re.compile("\d{13}") # isbn은 숫자 13자리
    info['isbn'] = (p.findall(bID.text))[0]
    return info

# 각 서점의 url 크롤링
def book_url(soup):
    binfo = book_info(soup)
    try:
        kb = 'http://www.kyobobook.co.kr/prom/2013/general/StoreStockTable.jsp?barcode=' + binfo['isbn'] + '&ejkgb=KOR'
    except:
        kb = ''
    try:
        yp = soup.find('a', string='영풍문고')['href']
    except:
        yp = ''
    try:
        bd = soup.find('a', string='반디앤루니스')['href']
    except:
        bd = ''
    return [kb, yp, bd]

# 네이버 도서페이지에서 입력받은 책 검색
def search_engine(txt):
    # 네이버 도서에서 해당 책 검색하는 URL
    url = 'https://book.naver.com/search/search.nhn?sm=sta_hty.book&sug=&where=nexearch&query=' + txt
    driver.get(url)
    # 첫번째 검색된 책의 url 추출
    b_url = driver.find_element_by_xpath('//*[@id="searchBiblioList"]/li[1]/dl/dt/a').get_attribute('href')
    driver.get(b_url)
    soup = BS(driver.page_source, 'html.parser')
    return soup

if __name__ == "__main__":    
    driver = webdriver.Chrome(r'C:\Users\smddu\Documents\chromedriver\chromedriver.exe')
    txt = input('도서명을 입력하세요 : ')
    soup = search_engine(txt)
    bInfo = book_info(soup)
    url = book_url(soup)
    stock = search_book(url)
    print(bInfo)
    driver.close()