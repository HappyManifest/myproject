from user_center.models import User

def user_info(request):
    username = request.session.get('username')
    user = User.objects.get(Username=username) if username else None
    return {'user': user}
