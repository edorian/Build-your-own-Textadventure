from django.contrib import admin
from website.adventure.models import Adventure, Location

class AdventureAdmin(admin.ModelAdmin):
    exclude = ("started_by_user", "completed_by_user")

admin.site.register(Adventure, AdventureAdmin)

admin.site.register(Location)
