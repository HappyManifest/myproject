from django.contrib import admin
from .models import VolunteerActivity,VolunteerRegistration
class VolunteerRegistrationInline(admin.TabularInline):
    model = VolunteerRegistration
    extra = 0

class VolunteerActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'start_time', 'end_time', 'location', 'total_volunteers', 'volunteers_registered', 'created_at')
    list_filter = ('organizer', 'start_time', 'end_time', 'location')
    search_fields = ('title', 'description', 'location')
    inlines = [VolunteerRegistrationInline]
    def volunteers_registered(self, obj):
        return obj.volunteerregistration_set.count()

admin.site.register(VolunteerActivity, VolunteerActivityAdmin)

class VolunteerRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity', 'registered_at')
    list_filter = ('activity', 'user')
    search_fields = ('user__username', 'activity__title')


