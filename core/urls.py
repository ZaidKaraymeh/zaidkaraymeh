from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('blog', views.blog, name='blog'),
    path('blog/<str:title>', views.blog, name='blog_detail'),
]
