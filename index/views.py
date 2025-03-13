from django.shortcuts import render
from environment.models import Article
from volunteers.models import VolunteerActivity
from forum.models import Post
from user_center.models import User
def index_view(request):
    latest_articles = Article.objects.all().order_by('-created_at')[:5]
    volunteer_services = VolunteerActivity.objects.all().order_by('-created_at')[:5]
    forum_posts = Post.objects.all().order_by('-created_at')[:5]
    try:
        username = request.session.get('username')
        user = User.objects.get(Username=username)
        return render(request, 'home.html', {
            'latest_articles': latest_articles,
            'volunteer_services': volunteer_services,
            'forum_posts': forum_posts,
            'user': user,
        })
    except:
        return render(request, 'home.html', {
            'latest_articles': latest_articles,
            'volunteer_services': volunteer_services,
            'forum_posts': forum_posts,
        })

