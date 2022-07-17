from django.contrib import admin
from .models import Team, TicketCategory, Ticket, Note
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


class NoteAdmin(SummernoteModelAdmin):
    list_display = (
        "id",
        "author",
        "ticket",
        "body_without_tags",
    )
    summernote_fields = "body"


admin.site.register(Team)
admin.site.register(Note, NoteAdmin)
admin.site.register(TicketCategory)
admin.site.register(Ticket, TicketAdmin)
