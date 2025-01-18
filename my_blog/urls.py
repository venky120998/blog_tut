from django.urls import path
from my_blog import views

app_name = 'my_blog'

urlpatterns = [path(route="", view=views.index, name='index'),
               path(route="post/<str:slug>", view=views.detail, name='detail'),
               path(route="old_url", view=views.old_url_redirect, name='old_page'),
               path(route="new_page_url", view=views.new_url_page, name='new_page'),
               path(route="contact", view=views.contact, name='contact'),
               path(route="about", view=views.about, name='about'),
               path(route="register", view=views.register_view, name='register_url')]