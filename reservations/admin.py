from django.contrib import admin
from .models import Table, Restaurant, OpeningSchedule, Reservation, Guest, Administrator, Session

admin.site.register(Table)
admin.site.register(Restaurant)
admin.site.register(Reservation)
admin.site.register(Administrator)
admin.site.register(Guest)
admin.site.register(Session)

@admin.register(OpeningSchedule)
class OpeningScheduleAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'day', 'active',)
    list_editable = ('active',)  # Allow editing 'active' in list view
    filter_horizontal = ('sessions',)  # Add this line