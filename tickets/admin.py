from django.contrib import admin
from .models import Team, TicketCategory, Ticket


class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "assigned_technician",
        "assigned_team",
        "status",
    )


admin.site.register(Team)
admin.site.register(TicketCategory)
admin.site.register(Ticket, TicketAdmin)
