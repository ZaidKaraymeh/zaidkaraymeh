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

ME_PHOTOS = [
    ("19-signing.jpg", "VoySera, Zain, and OneCX signing", "center center"),
    ("01-park.jpg", "Zaid in the park", "center 25%"),
    ("02-ghutra-glasses.jpg", "Zaid in ghutra and glasses", "center 40%"),
    ("13-hills.jpg", "Zaid in the hills", "center 28%"),
    ("04-thobe.jpg", "Zaid in a thobe", "center 30%"),
    ("12-sword.jpg", "Zaid holding a sword", "center 20%"),
    ("06-shemagh.jpg", "Zaid in a shemagh", "center 40%"),
    ("10-dinner.jpg", "Dinner with friends", "center center"),
    ("08-ghutra.jpg", "Zaid in a white ghutra", "center 40%"),
    ("11-palms.jpg", "Evening with friends under the palms", "center 45%"),
    ("03-hotel.jpg", "Zaid in a hotel room", "center 22%"),
    ("09-portrait-dark.jpg", "Portrait of Zaid", "center 40%"),
    ("05-elevator.jpg", "Zaid in an elevator", "center 30%"),
    ("07-portrait.jpg", "Portrait of Zaid", "center 28%"),
    ("14-elevator-bag.jpg", "Zaid in an elevator with a bag", "center 20%"),
    ("15-friends.jpg", "Zaid with friends", "center center"),
    ("16-desk.jpg", "Zaid working at a desk", "center center"),
    ("17-mirror.jpg", "Mirror selfie", "center 25%"),
    ("18-thinking.jpg", "Zaid thinking at a laptop", "center 30%"),
]


def me(request):
    photos = [
        {
            "src": f"{settings.STATIC_URL}me/{name}",
            "thumb": f"{settings.STATIC_URL}me/thumbs/{name}",
            "alt": alt,
            "pos": pos,
        }
        for name, alt, pos in ME_PHOTOS
    ]
    return render(request, 'me.html', {"photos": photos})