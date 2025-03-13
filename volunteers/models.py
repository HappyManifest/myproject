from django.db import models
from user_center.models import User # 假设User模型是从Django自带的User模型继承的

class VolunteerActivity(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    total_volunteers = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    organizer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    def volunteers_registered(self):
        return self.volunteerregistration_set.count()

    def get_registered_users(self) :
        return self.volunteerregistration_set.all().values_list('user__Username', flat=True)
    def is_full(self):
        return self.volunteers_registered() >= self.total_volunteers

class VolunteerRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(VolunteerActivity, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'activity')

    def __str__(self):
        return f'{self.user.username}报名参加{self.activity.title}'

