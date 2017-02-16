from django.conf.urls import url
from . import views

app_name="myapp"

urlpatterns = [
    url(r'^$', views.addressbook),
    url(r'^add/', views.add),
    url(r'^upload/', views.upload),
    url(r'^continue/', views.continueProcessCSV),
    url(r'^truncate/', views.truncateTable),
]