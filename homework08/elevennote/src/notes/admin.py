from django.contrib import admin

from .models import Note


class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'pub_date', 'was_published_recently')
    
    # Filter options: “Any date”, “Today”, “Past 7 days”, “This month”, “This year”.
    list_filter = ['pub_date']
    # Search capability
    search_fields = ['title', 'body']
    
admin.site.register(Note, NoteAdmin)


# Change admin template
admin.site.site_title = 'Elevennote'
admin.site.site_header = 'Administration'
admin.site.index_title = 'Elevennote app'
