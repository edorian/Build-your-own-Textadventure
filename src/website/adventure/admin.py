from django.contrib import admin
from website.adventure.models import Adventure, Location, Graph, Rating

class GraphInline(admin.StackedInline):
    model = Graph

class AdventureAdmin(admin.ModelAdmin):
    exclude = ("started_by_user", "completed_by_user")
    inlines = [GraphInline]

admin.site.register(Adventure, AdventureAdmin)
admin.site.register(Location)
admin.site.register(Rating)
