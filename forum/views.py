from django.shortcuts import render, get_object_or_404, redirect
from user_center.views import check_login
from user_center.models import User
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'forum/post_list.html', {'posts': page_obj})
def post_detail(request, post_id) :
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('-created_at')
    paginator = Paginator(comments, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    user = request.session['username']
    user=User.objects.get(Username=user)
    print(user)
    if request.method == 'POST' :
        comment_form = CommentForm(request.POST, request.FILES)
        print(comment_form)
        if comment_form.is_valid() :
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = user
            comment.save()
            return redirect('forum:post_detail', post_id=post.id)
        else :
            print("Form is not valid")
            print(comment_form.errors)
    else :
        comment_form = CommentForm()
    return render(request, 'forum/post_detail.html', {
        'post' : post,
        'comments' : page_obj,
        'comment_form' : comment_form,
    })
@check_login
def create_post(request):
    if request.method == 'POST':
        user = request.session['username']
        user = User.objects.get(Username=user)
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = user
            post.save()
            return redirect('/')
    else:
        form = PostForm()

    return render(request, 'forum/create_post.html', {'form': form})
