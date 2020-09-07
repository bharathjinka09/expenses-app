from django.urls import include, path
from .import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
#
urlpatterns = [
    path("", views.edit, name="edit"),
    path("tree-data", views.tree_data, name="treedata"),
    path("model-editor", views.model_editor, name="modeleditor"),
]
