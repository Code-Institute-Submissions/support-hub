from django.contrib import admin
from .models import Team, TicketCategory, Ticket


admin.site.register(Team)
admin.site.register(TicketCategory)
admin.site.register(Ticket)
