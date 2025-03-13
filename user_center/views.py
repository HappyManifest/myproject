from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect,get_object_or_404
import requests,random
from .models import User
from environment.models import Article
import hashlib
from PIL import Image,ImageDraw,ImageFile,ImageFont
from django.conf import settings
import six
import re
from six import BytesIO
from django.core.mail import send_mail
from volunteers.models import VolunteerActivity
from forum.models import Post
def check_login(fn):
    def wrap(request,*args,**kwargs):
        if 'username' not in request.session or 'uid' not in request.session:
            c_username = request.POST.get('username')
            c_uid = request.POST.get('uid')
            if not c_uid or not c_username:
                return HttpResponseRedirect('/user_center/login')
            else:
                request.session['username'] = c_username
                request.session['uid'] = c_uid
        return fn(request,*args,**kwargs)
    return wrap
def verify_code(request):
    bgcolor = (224,224,224)
    width = 100
    height = 34
    im = Image.new('RGB', (width, height), bgcolor)
    draw = ImageDraw.Draw(im)
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    str1 = 'abcdefghijklmnopqrstuvwsyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    font = ImageFont.truetype('arial.ttf', 23)
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    del draw
    request.session['verifycode'] = rand_str
    buf = BytesIO()
    im.save(buf, 'png')
    return HttpResponse(buf.getvalue(), 'image/png')
def url_reverse(request):
    return render(request,'url_reverse.html')
def register_view(request):
    if request.method=='GET':
        return render(request,'user_center/email1.html')
    elif request.method=='POST':
        str1 = 'abcdefghijklmnopqrstuvwsyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        # 随机选取4个值作为验证码
        rand_str = ''
        for i in range(0, 4) :
            rand_str += str1[random.randrange(0, len(str1))]
        request.session['captcha'] = rand_str
        email=request.POST.get('email','')
        request.session['email']=email
        send_mail(subject='阁下的邮箱验证码', message=rand_str, from_email='3203904957@qq.com',recipient_list=[email])
        context={'user':None}
        print(rand_str)
        return render(request,'user_center/register.html',context=context)

def register_final(request):
    global context
    if request.method=='POST':
        captcha=request.POST.get('captcha')
        print(captcha)
        if captcha==request.session['captcha']:
            Username = request.POST['username']
            #Schoolnumber = request.POST['schoolnumber']
            password1 = request.POST['password']
            password2 = request.POST['password_confirm']
            phone = request.POST['phone']
            if password1 != password2 :
                return HttpResponse('密码错了')
            old_users = User.objects.filter(Username=Username)
            #old_schoolnumber = User.objects.filter(Schoolnumber=Schoolnumber)
            password_hash = hashlib.md5(password1.encode())
            password_hash1 = password_hash.hexdigest()
            if old_users or len(phone)!=11:
                return HttpResponse('不对捏')
            try :
                user = User.objects.create(Username=Username, Password=password_hash1,
                                           Email=request.session['email'], Phone=phone)
                request.session['Username'] = Username
                request.session['id'] = user.id
                context = {'user' : Username}
                return redirect('/user_center/login')
            except Exception as e :
                print('--create user error as %s' % (e))
                return render(request, 'user_center/login.html', context=context)
        else:
            print('???')
            return HttpResponse('验证码不对')
    else:
        return render(request,'user_center/register.html')
def login_view(request):
    if request.method=='GET':
        if request.session.get('username') and request.session.get('uid'):
            return HttpResponseRedirect('/')
        c_username=request.POST.get('username')
        c_uid=request.POST.get('uid')
        if c_username and c_uid:
            request.session['username']=c_username
            request.session['uid']=c_uid
            return HttpResponseRedirect('/')
        return render(request,'user_center/login.html')
    elif request.method=='POST':
        Username=request.POST['username']
        Password=request.POST['password']
    try:
        user=User.objects.get(Username=Username)
    except Exception as e:
        print('--login error is %s'%(e))
        return render(request,'error.html')
    password_hash=hashlib.md5()
    password_hash.update(Password.encode())
    if password_hash.hexdigest()!=user.Password:
        return render(request,'error.html')
    request.session['username']=Username
    request.session['uid']=user.id
    request.session['email']=user.Email
    resp=HttpResponse('登陆成功')
    if 'remember' in request.POST:
        resp.set_cookie('username',Username,3600*24*3)
        resp.set_cookie('uid',user.id,3600*24*3)
    latest_articles = Article.objects.all().order_by('-created_at')[:5]
    volunteer_services = VolunteerActivity.objects.all().order_by('-created_at')[:5]
    forum_posts = Post.objects.all().order_by('-created_at')[:5]
    context = {'user' : user,'latest_articles': latest_articles,
            'volunteer_services': volunteer_services,
            'forum_posts': forum_posts,}
    return render(request, 'home.html', context=context)
def home(request):
    username = request.session.get('username')

    if username:
        user = User.objects.get(Username=username)
    else:
        user = None

    context = {'user': user}
    return render(request, 'home.html', context)
def logout_view(request):
    if 'username' in request.session:
        del request.session['username']
    if 'uid' in request.session:
        del request.session['uid']
    resp=HttpResponseRedirect('/')
    if 'username' in request.COOKIES:
        resp.delete_cookie('username')
    if 'uid' in request.COOKIES:
        resp.delete_cookie('uid')
    return resp
def change_password2(request):
    if request.method == 'GET':
        return render(request, 'user_center/change_password2.html')
    elif request.method == 'POST':
        str1 = 'abcdefghijklmnopqrstuvwsyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        rand_str = ''.join(random.sample(str1, 4))
        request.session['captcha'] = rand_str
        email = request.POST.get('email', '')
        request.session['email'] = email
        send_mail(
            subject='邮箱验证码',
            message=f'您的验证码是：{rand_str}',
            from_email='3203904957@qq.com',
            recipient_list=[email]
        )
        print(rand_str,email,'9')
        context = {'message': '验证码已发送到您的邮箱，请查收'}
        return redirect('change_password')
def change_password(request):
    try:
        if request.method == 'POST':
            stored_captcha = request.session.get('captcha')
            email = request.session.get('email')
            input_captcha = request.POST.get('captcha1')
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')
            if input_captcha != stored_captcha:
                return render(request, 'user_center/change_password.html', {'message': '验证码错误'})
            if password != password_confirm:
                return render(request, 'user_center/change_password.html', {'message': '两次密码输入不一致'})
            user = User.objects.get(Email=email)
            password_hash = hashlib.md5(password.encode())
            user.Password = password_hash.hexdigest()
            user.save()

            return redirect('login')
        elif request.method == 'GET':
            return render(request, 'user_center/change_password.html')
    except User.DoesNotExist:
        return render(request, 'error.html', {'message': '用户不存在'})
    except Exception as e:
        print(e)
        return render(request, 'user_center/login.html')

@check_login
def send_email(request):
    email = request.POST.get('email', '')
    return HttpResponse('')

@check_login
def personal_zone(request) :
    user = request.session['username']
    user = User.objects.get(Username=user)
    if request.method == 'POST' and 'delete_post_id' in request.POST :
        post_id = request.POST['delete_post_id']
        post = Post.objects.get(id=post_id, author=user)
        post.delete()
        return redirect('/user_center/personal_zone')

    published_activities = VolunteerActivity.objects.filter(organizer=user)
    posts = Post.objects.filter(author=user).order_by('-created_at')
    participated_activities = VolunteerActivity.objects.filter(volunteerregistration__user=user)

    context = {
        'user' : user,
        'published_activities' : published_activities,
        'participated_activities' : participated_activities,
        'posts' : posts
    }

    return render(request, 'user_center/personal_zone.html', context)

def personal_zone2(request,username):
    user = get_object_or_404(User, Username=username)
    # 查询用户发布和参与的活动
    published_activities = VolunteerActivity.objects.filter(organizer=user)
    participated_activities = VolunteerActivity.objects.filter(volunteerregistration__user=user)
    posts = Post.objects.filter(author=user).order_by('-created_at')
    context = {
        'user' : user,
        'published_activities' : published_activities,
        'participated_activities' : participated_activities,
        'posts':posts
    }
    return render(request, 'user_center/personal_zone2.html', context)
@check_login
def send(request):
    if request.method=='GET':
        return render(request,'send_email2.html')
    elif request.method=='POST':
        str1 = 'abcdefghijklmnopqrstuvwsyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        rand_str = ''
        for i in range(0, 4) :
            rand_str += str1[random.randrange(0, len(str1))]
        request.session['rand_str1'] = rand_str
        email=request.POST.get('email','')
        request.session['email']=email
        send_mail(subject='阁下的邮箱验证码', message=rand_str, from_email='3203904957@qq.com',recipient_list=[email])
        context={'user':None}
        return render(request,'user_center/change_pwd.html',context=context)
@check_login
def edit_profile(request):
    username = request.session.get('username')
    try:
        user = User.objects.get(Username=username)
    except User.DoesNotExist:
        return render(request, 'error.html', {'message': '用户不存在'})

    if request.method == 'POST':
        new_username = request.POST.get('username', user.Username)
        new_phone = request.POST.get('phone', user.Phone)
        new_email = request.POST.get('email', user.Email)
        new_head = request.FILES.get('head')
        if len(new_phone) != 11:
            return HttpResponse('手机号必须为 11 位数字')
        if User.objects.exclude(pk=user.pk).filter(Username=new_username).exists():
            return HttpResponse('用户名已存在')
        if User.objects.exclude(pk=user.pk).filter(Email=new_email).exists():
            return HttpResponse('邮箱已存在')


        user.Username = new_username
        user.Phone = new_phone
        user.Email = new_email
        if new_head:
            user.Head = new_head
        user.save()


        request.session['username'] = user.Username
        latest_articles = Article.objects.all().order_by('-created_at')[:5]
        volunteer_services = VolunteerActivity.objects.all().order_by('-created_at')[:5]
        forum_posts = Post.objects.all().order_by('-created_at')[:5]
        context = {'user': user, 'latest_articles': latest_articles,
                   'volunteer_services': volunteer_services,
                   'forum_posts': forum_posts, }
        return render(request,'home.html',context=context)


    context = {'user': user}
    return render(request, 'user_center/edit_profile.html', context)