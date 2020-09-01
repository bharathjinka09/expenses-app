from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
import requests


@login_required(login_url="/authentication/login")
def index(request):
    return render(request, "expenses/index.html")


@login_required(login_url="/authentication/login")
def add_expense(request):
    return render(request, "expenses/add_expense.html")


@login_required(login_url="/authentication/login")
def grab_data(request):

    url = request.POST.get("url", "")
    title = request.POST.get("title", "")
    article = request.POST.get("article", "")
    author = request.POST.get("author", "")
    pageno = request.POST.get("pageno", "")
    abstract = request.POST.get("abstract", "")
    keyword = request.POST.get("keyword", "")
    print(url, title, article, author, pageno, abstract, keyword)

    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        title_element = soup.find("h3")
        title_data = title_element.text

        article_element = soup.find(class_="tocTitle")
        article_data = article_element.text

        # data = soup.findAll("div", attrs={"class": "tocTitle"})
        # for div in data:
        #     links = div.findAll("a")
        #     for a in links:
        #         global article_link
        #         article_link = a["href"]

        author_element = soup.find(class_="tocAuthors")
        author_data = author_element.text

        page_element = soup.find(class_="tocPages")
        page_data = page_element.text

        context = {
            "title_data": title_data,
            "article_data": article_data,
            "author_data": author_data,
            "page_data": page_data,
            # "article_link": article_link,
        }
        return render(request, "expenses/grab_data.html", context)

    except Exception as e:
        print(e)
        return render(request, "expenses/grab_data.html")
