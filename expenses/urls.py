from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="expenses"),
    path("add-expense", views.add_expense, name="add-expense"),
    path("grab-data", views.grab_data, name="grab-data"),
    path("detail-data/<str:title>", views.detail_data, name="detail-data"),
]

# GetArticleInformation(TOCurl, ArticleTableName, TitleTableName, AuthorTableName, PageNoTableName, AbstractTableName, KeywordTableName, DOITableName)