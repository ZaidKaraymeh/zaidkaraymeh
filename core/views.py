from django.shortcuts import render
from .models import *
# Create your views here.

def home(request):
    blogs = Blog.objects.values("id", 'user', 'title', 'summary', 'created_at').order_by('-created_at')[:4]

    context = {
        'blogs':blogs
    }
    #print(blogs)
    return render(request, 'home.html', context)

def blog(request, title=''):

    if title:
        blog = Blog.objects.get(title=title)
        context = {
            'blog':blog
        }
        return render(request, 'blog_detail.html', context)


    blogs = Blog.objects.all().order_by('-created_at')
    context = {
        'blogs':blogs
    }

    return render(request, 'blog.html', context)