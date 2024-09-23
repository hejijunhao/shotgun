from django.contrib import admin, messages
from .models import Table, Restaurant, OpeningSchedule, Reservation, Guest, Administrator, Session

admin.site.register(Table)
admin.site.register(Restaurant)
# admin.site.register(Reservation)
admin.site.register(Administrator)
admin.site.register(Guest)
admin.site.register(Session)

@admin.register(OpeningSchedule)
class OpeningScheduleAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'day', 'active',)
    list_editable = ('active',)  # Allow editing 'active' in list view
    filter_horizontal = ('sessions',) 

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('guest', 'party_size', 'start_datetime', 'end_datetime', 'duration', 'get_tables')
    readonly_fields = ('end_datetime',)
    fields = ('guest', 'party_size', 'start_datetime', 'duration', 'end_datetime', 'tables')

    def get_tables(self, obj):
        return ", ".join([str(table.number) for table in obj.tables.all()])
    get_tables.short_description = 'Tables'

    def save_model(self, request, obj, form, change):
        obj.save()
        if getattr(obj, 'max_capacity_utilized', False):
            self.message_user(
                request,
                "Note: Maximum capacity is utilized for the selected table.",
                level=messages.WARNING
            )