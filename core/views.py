from django.shortcuts import render
from django.conf import settings
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

def me(request):
    photos = [
        {"src": f"{settings.STATIC_URL}me/19-signing.jpg", "alt": "VoySera, Zain, and OneCX signing"},
        {"src": f"{settings.STATIC_URL}me/01-park.jpg", "alt": "Zaid in the park"},
        {"src": f"{settings.STATIC_URL}me/02-ghutra-glasses.jpg", "alt": "Zaid in ghutra and glasses"},
        {"src": f"{settings.STATIC_URL}me/13-hills.jpg", "alt": "Zaid in the hills"},
        {"src": f"{settings.STATIC_URL}me/04-thobe.jpg", "alt": "Zaid in a thobe"},
        {"src": f"{settings.STATIC_URL}me/12-sword.jpg", "alt": "Zaid holding a sword"},
        {"src": f"{settings.STATIC_URL}me/06-shemagh.jpg", "alt": "Zaid in a shemagh"},
        {"src": f"{settings.STATIC_URL}me/10-dinner.jpg", "alt": "Dinner with friends"},
        {"src": f"{settings.STATIC_URL}me/08-ghutra.jpg", "alt": "Zaid in a white ghutra"},
        {"src": f"{settings.STATIC_URL}me/11-palms.jpg", "alt": "Evening with friends under the palms"},
        {"src": f"{settings.STATIC_URL}me/03-hotel.jpg", "alt": "Zaid in a hotel room"},
        {"src": f"{settings.STATIC_URL}me/09-portrait-dark.jpg", "alt": "Portrait of Zaid"},
        {"src": f"{settings.STATIC_URL}me/05-elevator.jpg", "alt": "Zaid in an elevator"},
        {"src": f"{settings.STATIC_URL}me/07-portrait.jpg", "alt": "Portrait of Zaid"},
        {"src": f"{settings.STATIC_URL}me/14-elevator-bag.jpg", "alt": "Zaid in an elevator with a bag"},
        {"src": f"{settings.STATIC_URL}me/15-friends.jpg", "alt": "Zaid with friends"},
        {"src": f"{settings.STATIC_URL}me/16-desk.jpg", "alt": "Zaid working at a desk"},
        {"src": f"{settings.STATIC_URL}me/17-mirror.jpg", "alt": "Mirror selfie"},
        {"src": f"{settings.STATIC_URL}me/18-thinking.jpg", "alt": "Zaid thinking at a laptop"},
    ]
    return render(request, 'me.html', {"photos": photos})