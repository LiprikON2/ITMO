from django.contrib import admin
from django.utils.translation import ugettext_lazy

from .models import *


# class ChoiceInline(admin.StackedInline):
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    # Filter options: “Any date”, “Today”, “Past 7 days”, “This month”, “This year”.
    list_filter = ['pub_date']
    # Search capability
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)


# Change admin template

admin.site.site_title = 'Admin'
admin.site.site_header = 'Administration'
admin.site.index_title = 'Polls app'
