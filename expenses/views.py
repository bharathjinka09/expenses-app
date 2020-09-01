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

        final_lists = []

        article_elements = soup.find_all(class_="tocTitle")

        for article_element in article_elements:
            print(article_element.text)
            final_lists.append({"articles": article_element.text})

        author_elements = soup.find_all(class_="tocAuthors")

        for author_element in author_elements:
            print(author_element.text)
            final_lists.append({"authors": author_element.text})

        page_elements = soup.find_all(class_="tocPages")

        for page_element in page_elements:
            print(page_element.text)
            final_lists.append({"pages": page_element.text})

        context = {
            "title_data": title_data,
            "final_lists": final_lists,
        }
        print(final_lists)
        return render(request, "expenses/grab_data.html", context)

    except Exception as e:
        print(e)
        return render(request, "expenses/grab_data.html")
