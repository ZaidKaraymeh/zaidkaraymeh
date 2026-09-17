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

# (kind, filename, alt text, object-position used when the 4:5 card crops it)
ME_MEDIA = [
    ("image", "19-signing.jpg", "Voysera, Zain, and OneCX signing", "center center"),
    ("video", "20-shooting.mp4", "Clay shooting by the river", "center 72%"),
    ("image", "02-ghutra-glasses.jpg", "Zaid in ghutra and glasses", "center 40%"),
    ("image", "23-battlestation.jpg", "Desk setup at night", "center center"),
    ("image", "13-hills.jpg", "Zaid in the hills", "center 28%"),
    ("image", "27-cat-face.jpg", "Close-up of the cat", "center 35%"),
    ("image", "12-sword.jpg", "Zaid holding a sword", "center 20%"),
    ("image", "10-dinner.jpg", "Dinner with friends", "center center"),
    ("image", "04-thobe.jpg", "Zaid in a thobe", "center 30%"),
    ("video", "21-cat-roll.mp4", "The cat rolling around", "center 45%"),
    ("image", "22-keyboard.jpg", "Keyboard on the desk", "center center"),
    ("image", "06-shemagh.jpg", "Zaid in a shemagh", "center 40%"),
    ("image", "11-palms.jpg", "Evening with friends under the palms", "center 45%"),
    ("image", "25-cat-plant.jpg", "The cat digging in a plant pot", "center 45%"),
    ("image", "01-park.jpg", "Zaid in the park", "center 25%"),
    ("image", "15-friends.jpg", "Zaid with friends", "center center"),
    ("image", "17-mirror.jpg", "Mirror selfie", "center 25%"),
    ("image", "24-cat-lounging.jpg", "The cat lounging on the table", "center center"),
    ("image", "08-ghutra.jpg", "Zaid in a white ghutra", "center 40%"),
    ("image", "03-hotel.jpg", "Zaid in a hotel room", "center 22%"),
    ("image", "26-cat-sleeping.jpg", "The cat asleep on a blanket", "center 40%"),
    ("image", "16-desk.jpg", "Zaid working at a desk", "center center"),
    ("image", "09-portrait-dark.jpg", "Portrait of Zaid", "center 40%"),
    ("image", "05-elevator.jpg", "Zaid in an elevator", "center 30%"),
    ("image", "18-thinking.jpg", "Zaid thinking at a laptop", "center 30%"),
    ("image", "14-elevator-bag.jpg", "Zaid in an elevator with a bag", "center 20%"),
    ("image", "07-portrait.jpg", "Portrait of Zaid", "center 28%"),
]


def me(request):
    static_url = settings.STATIC_URL
    media = []
    for kind, name, alt, pos in ME_MEDIA:
        if kind == 'video':
            poster = name.rsplit('.', 1)[0] + '.jpg'
            media.append({
                'kind': 'video',
                'src': f'{static_url}me/video/{name}',
                'thumb': f'{static_url}me/posters/{poster}',
                'alt': alt,
                'pos': pos,
            })
        else:
            media.append({
                'kind': 'image',
                'src': f'{static_url}me/{name}',
                'thumb': f'{static_url}me/thumbs/{name}',
                'alt': alt,
                'pos': pos,
            })
    return render(request, 'me.html', {'media': media})