from django.contrib import admin
from .models import Team, TicketCategory, Ticket
from django_summernote.admin import SummernoteModelAdmin


class TicketAdmin(SummernoteModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "assigned_technician",
        "assigned_team",
        "status",
    )
    summernote_fields = "description"


admin.site.register(Team)
admin.site.register(TicketCategory)
admin.site.register(Ticket, TicketAdmin)
