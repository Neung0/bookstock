from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.db.models import Count
from .models import Book, Author, Publisher, Url
import engine

def index(request):
    return render(request,'search/index.html')

def find_DB(request):
    t = request.POST.get('title')
    title_query = Book.objects.filter(title__contains=t).order_by('-title')[:5]
    #검색된 책이 이미 DB에 존재하는 경우 크롤링 과정 생략
    try:
        title_query[0] #조건 오류문
        context = {'title_query': title_query, 'input':t}
        return render(request, 'search/select.html', context)
    except:
        return HttpResponseRedirect(reverse('search:crawler', args=(t,)))

def crawler(request, t):
    soup = engine.search_engine(t)
    #잘못된 입력(soup)이 들어온 경우, 다시 검색
    if soup is False:
        return render(request,'search/nobook.html')
    b_info = engine.book_info(soup)
    b_url = engine.book_url(soup)
    # 작가, 출판사 존재유무 판단
    try :
        auth_toBe = Author.objects.get(name = b_info['auth'])
    except:
        auth_query = Author(name = b_info['auth'])
        auth_query.save()
    try :
        pub_toBe = Publisher.objects.get(company = b_info['pub'])
    except:
        pub_query = Publisher(company = b_info['pub'])
        pub_query.save()
    # 작가, 출판사 object를 가져와 book 테이블에 입력
    au = Author.objects.filter(name=b_info['auth'])[0]
    pu = Publisher.objects.filter(company=b_info['pub'])[0]
    book_query = Book(isbn = b_info['isbn'], title = b_info['title'], auth = au, pub = pu, image = b_info['img'], time = 0)
    book_query.save()
    # URL 입력
    bo = Book.objects.filter(isbn = b_info['isbn'])
    url_query = Url(book = bo[0], kb = b_url[0], yp = b_url[1], bd = b_url[2])
    url_query.save()
    isbn = bo[0].isbn
    return HttpResponseRedirect(reverse('search:result', args=(isbn,)))

def result(request, isbn):
    bo = Book.objects.get(isbn = isbn)
    url = Url.objects.get(book=bo)
    b_url = [url.kb, url.yp, url.bd]
    stock = engine.search_book(b_url)
    content = {'kb': stock[0], 'yp': stock[1], 'bd': stock[2]}
    return render(request, 'search/result.html', content)

def maptest(request):
    return render(request, 'search/maptest.html')