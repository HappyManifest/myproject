from django.http import HttpResponse,Http404
from user_center.views import check_login
from django.shortcuts import render, redirect,get_object_or_404
from .models import VolunteerActivity,VolunteerRegistration
from user_center.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.paginator import Paginator

def volunteer_activity_list(request):
    activities = VolunteerActivity.objects.all().order_by('-created_at')

    search_query = request.GET.get('q', '')
    if search_query:
        activities = activities.filter(title__icontains=search_query)

    sort_by = request.GET.get('sort', 'created_at')
    if sort_by == 'start_time':
        activities = activities.order_by('start_time')
    elif sort_by == 'end_time':
        activities = activities.order_by('end_time')
    else:
        activities = activities.order_by('-created_at')

    paginator = Paginator(activities, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'volunteers/activity_list.html', {
        'activities': page_obj,
    })

@check_login
def volunteer_activity_detail(request, activity_id) :
    activity = get_object_or_404(VolunteerActivity, id=activity_id)
    user = request.session['username']
    user = User.objects.get(Username=user)
    u=user.Username
    already_registered = VolunteerRegistration.objects.filter(user=user, activity=activity).exists()
    can_register = not already_registered and not activity.is_full()

    if request.method == 'POST' and can_register :
        VolunteerRegistration.objects.create(user=user, activity=activity)
        return redirect('volunteers:activity_list')
    registered_users = activity.get_registered_users()
    return render(request, 'volunteers/activity_detail.html', {
        'activity' : activity,
        'can_register' : can_register,
        'already_registered' : already_registered,
        'registered_users' : registered_users,
        'u':u,
    })
@check_login
def create_volunteer_activity(request) :
    user = request.session['username']
    user = User.objects.get(Username=user)
    if request.method == 'POST' :
        title = request.POST['title']
        description = request.POST['description']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        location = request.POST['location']
        total_volunteers = request.POST['total_volunteers']
        VolunteerActivity.objects.create(
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            location=location,
            total_volunteers=total_volunteers,
            organizer=user
        )
        return redirect('volunteers:activity_list')
    return render(request, 'volunteers/create_activity.html')

@check_login
def edit_activity(request, activity_id) :
    activity = get_object_or_404(VolunteerActivity, id=activity_id)
    if request.method == 'POST' :
        activity.title = request.POST['title']
        activity.description = request.POST['description']
        activity.start_time = request.POST['start_time']
        activity.end_time = request.POST['end_time']
        activity.location = request.POST['location']
        activity.total_volunteers = request.POST['total_volunteers']

        activity.save()

        messages.success(request, '活动更新成功！')
        return redirect('volunteers:activity_detail', activity_id=activity.id)

    context = {'activity' : activity}
    return render(request, 'volunteers/edit_activity.html', context)

@check_login
def delete_activity(request, activity_id) :
    activity = get_object_or_404(VolunteerActivity, id=activity_id)
    activity.delete()
    messages.success(request, '活动删除成功！')
    return redirect('volunteers:activity_list')