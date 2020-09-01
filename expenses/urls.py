from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='expenses'),
    path('add-expense', views.add_expense, name='add-expense'),
    path('grab-data', views.grab_data, name='grab-data'),
]
