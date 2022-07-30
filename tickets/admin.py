"""Admin for tickets application"""


from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Comment, Team, Ticket, TicketCategory


class TicketAdmin(SummernoteModelAdmin):
    """Set fields to display on the change ticket page of the admin portal."""

    list_display = (
        "id",
        "title",
        "author",
        "assigned_technician",
        "assigned_team",
        "status",
    )
    # use django-summernote WYSIWYG editor for description field
    summernote_fields = "description"


class CommentAdmin(SummernoteModelAdmin):
    """Set fields to display on the change comment page of the admin portal."""

    list_display = (
        "id",
        "author",
        "ticket",
        "body_without_tags",
    )
    # use django-summernote WYSIWYG editor for body field
    summernote_fields = "body"


# register models with admin site so they can be managed
admin.site.register(Team)
admin.site.register(Comment, CommentAdmin)
admin.site.register(TicketCategory)
admin.site.register(Ticket, TicketAdmin)
