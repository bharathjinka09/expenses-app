from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='/authentication/login')
def index(request):
    return render(request, 'expenses/index.html')


@login_required(login_url='/authentication/login')
def add_expense(request):
    return render(request, 'expenses/add_expense.html')


@login_required(login_url='/authentication/login')
def grab_data(request):

    url = request.POST.get('url', '')
    title = request.POST.get('title', '')
    article = request.POST.get('article', '')
    author = request.POST.get('author', '')
    pageno = request.POST.get('pageno', '')

    abstract = request.POST.get('abstract', '')
    keyword = request.POST.get('keyword', '')
    print(url, title, article, author, pageno, abstract, keyword)
    return render(request, 'expenses/grab_data.html')
