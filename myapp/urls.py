from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.addressbook),
    url(r'^add/', views.add),
    url(r'^upload/', views.upload),
]