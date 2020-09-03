from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
from pprint import pprint
import requests
from .models import Book


@login_required(login_url="/authentication/login")
def index(request):
    return render(request, "expenses/index.html")


@login_required(login_url="/authentication/login")
def add_expense(request):
    return render(request, "expenses/add_expense.html")

# //*[@id="content"]/table[1]/tbody/tr[1]/td[1]/a
# //*[@id="content"]/table[2]/tbody/tr[1]/td[1]/a

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

        # title_element = soup.find("h3")
        title_element = soup.find(title)
        title_data = title_element.text

        final_lists = []
        # [{'articles':[]},{'authors':[]}]
        # article_elements = soup.find_all(class_="tocTitle")
        article_elements = soup.find_all(class_=article)

        for article_element in article_elements:
            # print(article_element.text)
            final_lists.append({"articles": article_element.text})
            
            links = article_element.a['href']
            final_lists.append({"links":links})
            
            # Book.objects.create(article=article_element.text)

        # author_elements = soup.find_all(class_="tocAuthors")
        author_elements = soup.find_all(class_=author)

        for author_element in author_elements:
            # print(author_element.text)
            final_lists.append({"authors": author_element.text.strip()})
            # Book.objects.create(author=author_element.text)

        # page_elements = soup.find_all(class_="tocPages")
        page_elements = soup.find_all(class_=pageno)

        for page_element in page_elements:
            # print(page_element.text)
            final_lists.append({"pages": page_element.text.strip()})
            # Book.objects.create(page_no=page_element.text)

        context = {
            "title_data": title_data,
            "final_lists": final_lists,
            "links": links,
        }
        # pprint(final_lists)
        return render(request, "expenses/grab_data.html", context)

    except Exception as e:
        print(e)
        return render(request, "expenses/grab_data.html")


@login_required(login_url="/authentication/login")
def detail_data(request, title):
    print(title, "title")
    id = 932
    url = f"http://journals.foundationspeak.com/index.php/ijmss/article/view/{id}"
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        title_element = soup.find("h3")
        title_data = title_element.text

        author_element = soup.find(id="authorString")
        author_data = author_element.text

        abstract_element = soup.find("div", id="articleAbstract")
        abstract_data = abstract_element.text[9:]

        subject_element = soup.find("div", id="articleSubject")
        subject_data = subject_element.text[9:]

        # //*[@id="articleAbstract"]/div/p/em[1]

        context = {
            "title": title,
            "title_data": title_data,
            "author_data": author_data,
            "abstract_data": abstract_data,
            "subject_data": subject_data,
        }
        return render(request, "expenses/detail_data.html", context)

    except Exception as e:
        return render(request, "expenses/detail_data.html")


import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
import re
from django.http import JsonResponse
from pprint import pprint

# Grabber Tool


# @login_required(login_url="/authentication/login")
# def GetArticleInformation(request):
# 	try:
# 		hn = []
# 		ArticleInfo = {}
# 		# res = requests.get('http://journals.foundationspeak.com/index.php/ijmss/issue/view/87/showToc')
# 		try:
# 			url = request.POST.get("url", "")
# 		except Exception as e:
# 			pass

# 		res = requests.get(url)
# 		return render(request, "expenses/grab_data.html", context)

# 	except HTTPError as e:
# 		print(e)
# 	except URLError:
# 		print("Server down or incorrect domain")
# 	else:
# 		# soup = BeautifulSoup(res.text, 'html.parser')
# 		soup = BeautifulSoup(res.text, "html5lib")

# 		# Journal Title
# 		journaltitle = soup.title
# 		journaltitlename = ((journaltitle.getText()).replace("\n", "")).replace(
# 			"\t", ""
# 		)
# 		hn.append({"JournalTitle": journaltitlename})

# 		title = request.POST.get("title", "")
# 		article = request.POST.get("article", "")
# 		author = request.POST.get("author", "")
# 		pageno = request.POST.get("pageno", "")
# 		abstract = request.POST.get("abstract", "")
# 		keyword = request.POST.get("keyword", "")

# 		# GetArticleInformation(TOCurl, ArticleTableName, TitleTableName, AuthorTableName, PageNoTableName, AbstractTableName, KeywordTableName, DOITableName)

# 		# GetArticleInformation(
# 		#     "https://journals.scholarpublishing.org/index.php/TMLAI/issue/view/287",
# 		#     "obj_article_summary",
# 		#     "title",
# 		#     "authors",
# 		#     "pages",
# 		#     "item abstract",
# 		#     "item keywords",
# 		#     "item doi",
# 		# )

# 		# Article Title
# 		# title = soup.select('.' + ArticleTableName)
# 		# Author = soup.select('.' + AuthorTableName)
# 		# Authortags = soup.findAll("td", {"class": "tocAuthors"})
# 		Authortags = soup.findAll("div", {"class": AuthorTableName})
# 		title = soup.findAll("div", {"class": TitleTableName})
# 		PageNoData = soup.findAll("div", {"class": PageNoTableName})
# 		# urlTags = soup.findAll("a", {"class": TitleTableName})
# 		# urlTags = soup.findAll("a", {"class": TitleTableName})

# 		for idx, item in enumerate(title):
# 			for one_a_tag in title[idx].findAll("a"):  # 'a' tags are for links
# 				href = one_a_tag["href"]
# 				# print(idx)
# 			# titleName = replace(title[idx].getText(),'\n', '')
# 			# titleName = ((title[idx].getText()).replace('\n', '').replace('\t',''))
# 			# href = ((urlTags[idx].getText().replace('\n', '').replace('\t', '')))
# 			# href = item.get('href', None)
# 			titleName = title[idx].getText().replace("\n", "").replace("\t", "")
# 			try:
# 				AuthorName = (
# 					Authortags[idx].getText().replace("\n", "").replace("\t", "")
# 				)
# 			except Exception as e:
# 				pass

# 			try:
# 				PageNo = PageNoData[idx].getText().replace("\n", "").replace("\t", "")
# 			except Exception as e:
# 				pass
# 			# AuthorName = ((PageNoData[idx].getText()).replace('\n', '').replace('\t', ''))

# 			res_2 = requests.get(href)
# 			soup_details = BeautifulSoup(res_2.text, "html5lib")
# 			AbstractDescription = soup_details("div", {"class": AbstractTableName})
# 			# DOIName1 = ""
# 			# if DOITableName != "":
# 			#     DOI = soup_details("div", {"class": DOITableName})
# 			#     # print(DOI)
# 			#     DOIName = re.findall(r'<a href="https://doi.org/.*', str(DOI))
# 			#     # print('DOIName')
# 			#     # print(DOIName)
# 			#     for DOI1 in DOIName:
# 			#         DOIName1 = DOI1.replace('<a href="https://doi.org/', "").replace(
# 			#             '">', ""
# 			#         )
# 			# print(DOIName1)

# 			# Dummy To test
# 			# print('Soupdetails')
# 			# print(soup_details)
# 			# print(AbstractTableName)
# 			# print('Abstract')
# 			# print(AbstractDescription)

# 			Abstract = (
# 				(str(AbstractDescription[0].text).replace("Abstract", "", 1))
# 				.replace("\n", "")
# 				.replace("\t", "")
# 			)
# 			Keyword = soup_details("div", {"class": KeywordTableName})
# 			KeywordDescription = (
# 				(str(Keyword[0].text).replace("Keywords", "", 1))
# 				.replace("\n", "")
# 				.replace("\t", "")
# 			)

# 			# Regular Expression
# 			# patteren = re.compile(r'<div><p><em>([a-zA-z0-9]*)+(<br />)')
# 			# patteren = re.compile(r'([a-zA-z0-9]*)')
# 			# x = patteren.findall(str(AbstractDescription[0].text))
# 			# print(str(AbstractDescription[0].text))

# 			hn.append(
# 				{
# 					"Articletitle": titleName,
# 					# "DOI": DOIName1,
# 					"Page": PageNo,
# 					"link": href,
# 					"Author": AuthorName,
# 					"Abstract": Abstract,
# 					"Keywords": KeywordDescription,
# 				}
# 			)

# 		pprint(hn)
# 		context = {
# 			"articles": hn,
# 		}
# 		# GetArticleInformation(
# 		#     "https://journals.scholarpublishing.org/index.php/TMLAI/issue/view/287",
# 		#     "obj_article_summary",
# 		#     "title",
# 		#     "authors",
# 		#     "pages",
# 		#     "item abstract",
# 		#     "item keywords",
# 		#     "item doi",
# 		# )

# 		return render(request, "expenses/grab_data.html", context)
# return JsonResponse(hn, safe=False)

# print(hn[2])


# GetArticleInformation(TOCurl, ArticleTableName, TitleTableName, AuthorTableName, PageNoTableName, AbstractTableName, KeywordTableName, DOITableName)


# GetArticleInformation(
#     "https://journals.scholarpublishing.org/index.php/TMLAI/issue/view/287",
#     "obj_article_summary",
#     "title",
#     "authors",
#     "pages",
#     "item abstract",
#     "item keywords",
#     "item doi",
# )
